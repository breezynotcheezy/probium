from __future__ import annotations
import string
import chardet
import numpy as np
from typing import List, Dict, Optional, Tuple
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel
import torch
import torch.nn as nn
from tree_sitter import Language, Parser
import re
from concurrent.futures import ThreadPoolExecutor
from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

class MultiModalClassifier(nn.Module):
    def __init__(self, transformer_dim: int, num_classes: int):
        super().__init__()
        
        # Transformer feature dimension
        self.transformer_dim = transformer_dim
        
        # Statistical features dimension (entropy, char ratios, etc.)
        self.stats_dim = 10
        
        # Syntactic features dimension (AST patterns)
        self.syntax_dim = 50
        
        # Neural network layers for each modality
        self.transformer_layer = nn.Linear(transformer_dim, 256)
        self.stats_layer = nn.Linear(self.stats_dim, 64)
        self.syntax_layer = nn.Linear(self.syntax_dim, 128)
        
        # Attention mechanism for modality fusion
        self.attention = nn.MultiheadAttention(embed_dim=256, num_heads=4)
        
        # Feature fusion layers
        self.fusion_layer = nn.Sequential(
            nn.Linear(256 + 64 + 128, 512),
            nn.LayerNorm(512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, 256),
            nn.LayerNorm(256),
            nn.ReLU(),
            nn.Dropout(0.2)
        )
        
        # Output layer
        self.classifier = nn.Linear(256, num_classes)
        
        # Confidence estimation layer
        self.confidence_layer = nn.Sequential(
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, 
                transformer_features: torch.Tensor,
                statistical_features: torch.Tensor,
                syntactic_features: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        
        # Process transformer features
        trans_hidden = self.transformer_layer(transformer_features)
        
        # Process statistical features
        stats_hidden = self.stats_layer(statistical_features)
        
        # Process syntactic features
        syntax_hidden = self.syntax_layer(syntactic_features)
        
        # Apply self-attention to transformer features
        trans_hidden, _ = self.attention(trans_hidden, trans_hidden, trans_hidden)
        
        # Concatenate all features
        combined = torch.cat([
            trans_hidden,
            stats_hidden.unsqueeze(1).expand(-1, trans_hidden.size(1), -1),
            syntax_hidden.unsqueeze(1).expand(-1, trans_hidden.size(1), -1)
        ], dim=-1)
        
        # Fuse features
        fused = self.fusion_layer(combined)
        
        # Get classification logits
        logits = self.classifier(fused.mean(dim=1))
        
        # Estimate confidence
        confidence = self.confidence_layer(fused.mean(dim=1))
        
        return logits, confidence

@register
class TextEngineV2(EngineBase):
    name = "text_v2"
    cost = 2.0  # Higher cost due to ML model usage
    
    def __init__(self):
        super().__init__()
        # Initialize base transformer model
        self.model_name = "microsoft/codebert-base"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.base_model = AutoModel.from_pretrained(self.model_name)
        
        # Initialize multi-modal classifier
        self.classifier = MultiModalClassifier(
            transformer_dim=self.base_model.config.hidden_size,
            num_classes=200  # Number of file types to classify
        )
        self.classifier.eval()
        
        # Initialize Tree-sitter parser
        self.parser = Parser()
        # TODO: Load necessary tree-sitter grammars
        
        # Thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Compile regex patterns
        self.shebang_pattern = re.compile(r'^#!.*?/([^/\s]+)$', re.MULTILINE)
        self.embedded_patterns = {
            'jsx': re.compile(r'<[A-Z][A-Za-z0-9]*|{.*?}'),
            'php': re.compile(r'<\?php|\?>'),
            'yaml_md': re.compile(r'^---\s*$.*?^---\s*$', re.MULTILINE | re.DOTALL)
        }

    def normalize_text(self, payload: bytes) -> Tuple[str, float]:
        """Normalize text content with encoding detection and noise removal."""
        # Detect encoding
        encoding_result = chardet.detect(payload)
        encoding = encoding_result['encoding'] or 'utf-8'
        confidence = encoding_result['confidence']
        
        try:
            # Decode with detected encoding
            text = payload.decode(encoding)
            
            # Strip noise
            text = self._strip_noise(text)
            
            return text, confidence
        except UnicodeDecodeError:
            # Fallback to utf-8 if detection fails
            try:
                text = payload.decode('utf-8')
                text = self._strip_noise(text)
                return text, 0.5
            except UnicodeDecodeError:
                return "", 0.0

    def _strip_noise(self, text: str) -> str:
        """Remove noise from text while preserving important content."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common boilerplate
        text = re.sub(r'Copyright.*?\n', '', text)
        text = re.sub(r'License.*?\n', '', text)
        
        # Remove code comments (basic implementation)
        text = re.sub(r'//.*?\n|/\*.*?\*/', '', text, flags=re.DOTALL)
        
        return text.strip()

    def check_text_quality(self, text: str) -> Tuple[float, float]:
        """Calculate text quality metrics."""
        if not text:
            return 0.0, 0.0
            
        # Calculate byte entropy
        byte_freq = np.zeros(256)
        for char in text.encode('utf-8'):
            byte_freq[char] += 1
        byte_freq = byte_freq / len(text)
        entropy = -np.sum(byte_freq[byte_freq > 0] * np.log2(byte_freq[byte_freq > 0]))
        
        # Calculate printable ratio
        printable = set(string.printable)
        printable_count = sum(1 for c in text if c in printable)
        printable_ratio = printable_count / len(text)
        
        return entropy, printable_ratio

    def detect_embedded_content(self, text: str) -> Dict[str, float]:
        """Detect embedded content types and their confidence scores."""
        embedded = {}
        
        for lang, pattern in self.embedded_patterns.items():
            matches = pattern.findall(text)
            if matches:
                # Calculate confidence based on match density
                confidence = min(len(matches) / len(text.splitlines()), 0.95)
                embedded[lang] = confidence
                
        return embedded

    def extract_statistical_features(self, text: str) -> torch.Tensor:
        """Extract statistical features from text."""
        if not text:
            return torch.zeros(10)
            
        # 1. Entropy calculation
        byte_freq = np.zeros(256)
        text_bytes = text.encode('utf-8')
        for char in text_bytes:
            byte_freq[char] += 1
        byte_freq = byte_freq / len(text_bytes)
        entropy = -np.sum(byte_freq[byte_freq > 0] * np.log2(byte_freq[byte_freq > 0]))
        
        # 2. Character type ratios
        total_chars = len(text)
        alpha_ratio = sum(c.isalpha() for c in text) / total_chars
        digit_ratio = sum(c.isdigit() for c in text) / total_chars
        space_ratio = sum(c.isspace() for c in text) / total_chars
        punct_ratio = sum(c in string.punctuation for c in text) / total_chars
        
        # 3. Line statistics
        lines = text.splitlines()
        avg_line_length = np.mean([len(line) for line in lines]) if lines else 0
        line_length_std = np.std([len(line) for line in lines]) if lines else 0
        
        # 4. Special patterns
        bracket_balance = sum(1 for c in text if c in '([{') - sum(1 for c in text if c in ')]}')
        quote_count = sum(1 for c in text if c in '"\'')
        
        # 5. Whitespace patterns
        leading_space_ratio = sum(1 for line in lines if line.startswith(' ')) / len(lines) if lines else 0
        
        features = torch.tensor([
            entropy,
            alpha_ratio,
            digit_ratio,
            space_ratio,
            punct_ratio,
            avg_line_length / 100,  # Normalized
            line_length_std / 100,  # Normalized
            abs(bracket_balance) / 100,  # Normalized
            quote_count / total_chars,
            leading_space_ratio
        ], dtype=torch.float32)
        
        return features

    def extract_syntactic_features(self, text: str) -> torch.Tensor:
        """Extract syntactic features using tree-sitter."""
        try:
            tree = self.parser.parse(bytes(text, "utf8"))
            
            # Initialize feature vector
            features = torch.zeros(50)
            
            # Extract AST patterns
            cursor = tree.walk()
            node_types = {}
            depths = []
            current_depth = 0
            
            def visit_node():
                nonlocal current_depth
                node_type = cursor.node.type
                node_types[node_type] = node_types.get(node_type, 0) + 1
                depths.append(current_depth)
                
                current_depth += 1
                if cursor.goto_first_child():
                    visit_node()
                    while cursor.goto_next_sibling():
                        visit_node()
                    cursor.goto_parent()
                current_depth -= 1
            
            visit_node()
            
            # Convert patterns to features
            # 1. Node type distribution (first 20 features)
            sorted_types = sorted(node_types.items(), key=lambda x: x[1], reverse=True)
            for i, (_, count) in enumerate(sorted_types[:20]):
                features[i] = count / sum(node_types.values())
            
            # 2. Tree statistics (next 10 features)
            features[20] = len(depths) / 1000  # Normalized node count
            features[21] = max(depths) / 50  # Normalized max depth
            features[22] = np.mean(depths) / 20  # Normalized average depth
            features[23] = np.std(depths) / 10  # Normalized depth standard deviation
            features[24] = len(node_types) / 100  # Normalized unique node type count
            
            # 3. Structural patterns (next 20 features)
            # (Implementation depends on specific language grammars)
            
            return features
            
        except Exception:
            return torch.zeros(50)

    async def sniff(self, payload: bytes) -> Result:
        """Enhanced classification method using multi-modal analysis."""
        # Step 1: Text normalization and quality check
        text, encoding_conf = self.normalize_text(payload)
        if not text:
            return Result(candidates=[])
            
        entropy, printable_ratio = self.check_text_quality(text)
        if entropy < 0.5 or printable_ratio < 0.8:
            return Result(candidates=[])

        # Step 2: Feature extraction
        with torch.no_grad():
            # 2.1: Transformer features
            inputs = self.tokenizer(text[:512], return_tensors="pt", truncation=True)
            transformer_outputs = self.base_model(**inputs)
            transformer_features = transformer_outputs.last_hidden_state
            
            # 2.2: Statistical features
            statistical_features = self.extract_statistical_features(text)
            
            # 2.3: Syntactic features
            syntactic_features = self.extract_syntactic_features(text)
            
            # Step 3: Multi-modal classification
            logits, confidence = self.classifier(
                transformer_features,
                statistical_features.unsqueeze(0),
                syntactic_features.unsqueeze(0)
            )
            
            # Get top-5 predictions
            probs = torch.softmax(logits, dim=1)
            values, indices = torch.topk(probs[0], 5)
            
            # Step 4: Additional context analysis
            embedded_types = self.detect_embedded_content(text)
            shebang_match = self.shebang_pattern.search(text)
            
            # Create candidates
            candidates = []
            for conf, idx in zip(values, indices):
                lang_type = self.classifier.config.id2label[idx.item()]
                
                # Confidence adjustment
                final_conf = conf.item() * confidence.item()
                
                # Boost confidence based on context
                if shebang_match and shebang_match.group(1) == lang_type:
                    final_conf = min(final_conf + 0.1, 0.99)
                    
                if lang_type in embedded_types:
                    final_conf = min(final_conf + 0.05, 0.99)
                
                cand = Candidate(
                    media_type=f"text/{lang_type}",
                    extension=lang_type,
                    confidence=final_conf,
                    breakdown={
                        "ml_confidence": conf.item(),
                        "model_confidence": confidence.item(),
                        "encoding_confidence": encoding_conf,
                        "entropy": entropy,
                        "printable_ratio": printable_ratio,
                        "embedded_types": embedded_types,
                        "statistical_features": statistical_features.tolist(),
                        "has_syntax_tree": bool(syntactic_features.sum())
                    }
                )
                candidates.append(cand)
            
        return Result(candidates=candidates)

    def __del__(self):
        """Cleanup resources."""
        self.executor.shutdown(wait=False) 