from __future__ import annotations
import string
import chardet
import numpy as np
from typing import List, Dict, Optional, Tuple
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel
import torch
import torch.nn as nn
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import random
from functools import lru_cache
from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

# Use CUDA if available, otherwise CPU
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define supported file types
SUPPORTED_TYPES = [
    "python", "javascript", "typescript", "java", "cpp", "php", "ruby", "go", "rust",
    "html", "css", "json", "yaml", "markdown", "xml", "svg", "sql", "shell", "dockerfile",
    "ini", "toml", "properties", "csv", "tsv", "log", "text"
]

# Maximum text size for full processing
MAX_TEXT_SIZE = 100_000  # 100KB

# Cache size for embeddings
EMBEDDING_CACHE_SIZE = 1000

class MultiModalClassifier(nn.Module):
    def __init__(self, transformer_dim: int, num_classes: int = len(SUPPORTED_TYPES)):
        super().__init__()
        
        # Transformer feature dimension
        self.transformer_dim = transformer_dim
        
        # Statistical features dimension (entropy, char ratios, etc.)
        self.stats_dim = 10
        
        # Neural network layers for each modality
        self.transformer_layer = nn.Linear(transformer_dim, 256)
        self.stats_layer = nn.Linear(self.stats_dim, 64)
        
        # Attention mechanism for modality fusion
        self.attention = nn.MultiheadAttention(embed_dim=256, num_heads=4)
        
        # Feature fusion layers
        self.fusion_layer = nn.Sequential(
            nn.Linear(256 + 64, 512),
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
        
        # Label mapping
        self.id2label = {i: label for i, label in enumerate(SUPPORTED_TYPES)}
        self.label2id = {label: i for i, label in enumerate(SUPPORTED_TYPES)}
        
        # Move model to appropriate device
        self.to(DEVICE)

    def forward(self, 
                transformer_features: torch.Tensor,
                statistical_features: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        
        # Move inputs to appropriate device
        transformer_features = transformer_features.to(DEVICE)
        statistical_features = statistical_features.to(DEVICE)
        
        # Process transformer features
        trans_hidden = self.transformer_layer(transformer_features)
        
        # Process statistical features
        stats_hidden = self.stats_layer(statistical_features)
        
        # Apply self-attention to transformer features
        trans_hidden, _ = self.attention(trans_hidden, trans_hidden, trans_hidden)
        
        # Concatenate all features
        combined = torch.cat([
            trans_hidden,
            stats_hidden.unsqueeze(1).expand(-1, trans_hidden.size(1), -1)
        ], dim=-1)
        
        # Fuse features
        fused = self.fusion_layer(combined)
        
        # Get classification logits
        logits = self.classifier(fused.mean(dim=1))
        
        # Estimate confidence
        confidence = self.confidence_layer(fused.mean(dim=1))
        
        return logits, confidence

#@register
class TextEngineV2(EngineBase):
    name = "text_v2"
    cost = 1.0  # Lower cost to ensure it's preferred over other engines
    
    def __init__(self):
        super().__init__()
        # Initialize base transformer model
        self.model_name = "microsoft/codebert-base"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.base_model = AutoModel.from_pretrained(self.model_name)
        
        # Move base model to appropriate device
        self.base_model.to(DEVICE)
        
        # Initialize multi-modal classifier
        self.classifier = MultiModalClassifier(
            transformer_dim=self.base_model.config.hidden_size,
            num_classes=len(SUPPORTED_TYPES)
        )
        self.classifier.eval()
        
        # Thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Compile regex patterns
        self.shebang_pattern = re.compile(r'^#!.*?/([^/\s]+)$', re.MULTILINE)
        self.embedded_patterns = {
            'jsx': re.compile(r'<[A-Z][A-Za-z0-9]*|{.*?}'),
            'php': re.compile(r'<\?php|\?>'),
            'yaml_md': re.compile(r'^---\s*$.*?^---\s*$', re.MULTILINE | re.DOTALL),
            'svg': re.compile(r'<svg[^>]*>|xmlns:svg=|</svg>')
        }
        
        # Enhanced file type patterns with weights
        self.file_patterns = {
            "svg": [
                (r'<svg[^>]*>', 1.0),  # Root element
                (r'xmlns:svg="http://www\.w3\.org/2000/svg"', 1.0),  # Namespace
                (r'<path[^>]*d="[^"]*"', 0.8),  # Path with d attribute
                (r'<circle[^>]*r="[^"]*"', 0.7),  # Circle with radius
                (r'<rect[^>]*width="[^"]*"', 0.7),  # Rectangle with dimensions
                (r'<g[^>]*transform="[^"]*"', 0.6),  # Group with transform
                (r'<polygon[^>]*points="[^"]*"', 0.7),  # Polygon with points
                (r'<text[^>]*>[^<]*</text>', 0.5),  # Text element
                (r'<defs>', 0.4),  # Definitions section
                (r'<style[^>]*>[^<]*</style>', 0.4),  # Style section
                (r'<linearGradient|<radialGradient', 0.4),  # Gradients
                (r'<mask|<clipPath', 0.4),  # Masking/clipping
                (r'<animate|<animateTransform', 0.3),  # Animation
                (r'stroke="[^"]*"|fill="[^"]*"', 0.5),  # Common attributes
                (r'viewBox="[^"]*"', 0.8)  # ViewBox attribute
            ],
            "xml": [
                (r'<\?xml\s+version="[^"]*"\s+encoding="[^"]*"\?>', 1.0),
                (r'xmlns="[^"]*"', 0.8),
                (r'<[a-zA-Z0-9]+:[a-zA-Z0-9]+', 0.6),
                (r'</[a-zA-Z0-9]+:[a-zA-Z0-9]+>', 0.6),
                (r'<!DOCTYPE[^>]*>', 0.7),
                (r'<!\[CDATA\[.*?\]\]>', 0.7),
                (r'<!--.*?-->', 0.3)
            ]
        }

    def smart_sample_text(self, text: str, max_size: int = MAX_TEXT_SIZE) -> str:
        """Intelligently sample text for large files."""
        if len(text) <= max_size:
            return text
            
        lines = text.splitlines()
        if not lines:
            return ""
            
        # Always include first and last ~10% of lines
        head_size = max(1, len(lines) // 10)
        tail_size = max(1, len(lines) // 10)
        
        # Sample from middle ensuring we get complete code blocks
        middle_lines = lines[head_size:-tail_size]
        if not middle_lines:
            return "\n".join(lines[:head_size] + lines[-tail_size:])
            
        # Try to find complete code blocks or meaningful chunks
        chunks = []
        current_chunk = []
        block_start = False
        
        for line in middle_lines:
            # Check for block markers
            if re.match(r'^[\s]*(class|def|function|if|for|while|try|with)', line):
                block_start = True
            elif block_start and line.strip() and not line.startswith(' '):
                block_start = False
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = []
                
            if block_start or not current_chunk:
                current_chunk.append(line)
                
        if current_chunk:
            chunks.append(current_chunk)
            
        # Randomly sample chunks to fit size limit
        sampled_chunks = []
        remaining_size = max_size - len("\n".join(lines[:head_size] + lines[-tail_size:]))
        random.shuffle(chunks)
        
        for chunk in chunks:
            chunk_text = "\n".join(chunk)
            if len(chunk_text) <= remaining_size:
                sampled_chunks.append(chunk_text)
                remaining_size -= len(chunk_text)
            if remaining_size <= 0:
                break
                
        # Combine all parts
        return "\n".join([
            "\n".join(lines[:head_size]),
            "\n".join(sampled_chunks),
            "\n".join(lines[-tail_size:])
        ])

    @lru_cache(maxsize=EMBEDDING_CACHE_SIZE)
    def get_transformer_features(self, text_hash: str, text: str) -> torch.Tensor:
        """Get transformer features with caching."""
        with torch.no_grad():
            inputs = self.tokenizer(text[:512], return_tensors="pt", truncation=True)
            outputs = self.base_model(**inputs)
            return outputs.last_hidden_state

    def normalize_text(self, payload: bytes) -> Tuple[str, float]:
        """Normalize text content with enhanced encoding detection."""
        # Try UTF-8 first (most common)
        try:
            text = payload.decode('utf-8')
            return text, 1.0
        except UnicodeDecodeError:
            pass
            
        # Try other common encodings
        for encoding in ['utf-16', 'utf-32', 'ascii', 'iso-8859-1', 'cp1252']:
            try:
                text = payload.decode(encoding)
                return text, 0.9
            except UnicodeDecodeError:
                continue
                
        # Fall back to chardet
        encoding_result = chardet.detect(payload)
        encoding = encoding_result['encoding'] or 'utf-8'
        confidence = encoding_result['confidence']
        
        try:
            text = payload.decode(encoding)
            text = self._strip_noise(text)
            return text, confidence
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
        """Check text quality using entropy and printable character ratio."""
        if not text:
            return 0.0, 0.0
            
        # Calculate entropy
        byte_freq = np.zeros(256)
        text_bytes = text.encode('utf-8')
        for char in text_bytes:
            byte_freq[char] += 1
        byte_freq = byte_freq / len(text_bytes)
        entropy = -np.sum(byte_freq[byte_freq > 0] * np.log2(byte_freq[byte_freq > 0]))
        
        # Calculate printable character ratio
        printable_chars = sum(1 for c in text if c.isprintable() or c.isspace())
        printable_ratio = printable_chars / len(text)
        
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

    def _guess_language(self, text: str) -> Dict[str, float]:
        """Enhanced language detection with weighted pattern matching."""
        patterns = {
            "python": [
                (r"^(from\s+[\w.]+\s+import|\s*import\s+[\w.]+)", 0.8),
                (r"def\s+\w+\s*\([^)]*\)\s*:", 0.9),
                (r"class\s+\w+(\s*\([^)]*\))?\s*:", 0.9),
                (r":\s*$", 0.3),
                (r"^\s*@\w+", 0.7),
                (r"if\s+__name__\s*==\s*['\"]__main__['\"]", 1.0)
            ],
            "javascript": [
                (r"(const|let|var)\s+\w+\s*=", 0.7),
                (r"function\s+\w+\s*\(.*\)", 0.8),
                (r"^\s*import\s+.*from\s+['\"]", 0.8),
                (r"export\s+(default\s+)?(class|function|const|let)", 0.9),
                (r"document\.|window\.", 1.0),
                (r"addEventListener\(", 0.8),
                (r"Promise\.", 0.8)
            ],
            "typescript": [
                (r":\s*(string|number|boolean|any)\b", 0.8),
                (r"interface\s+\w+\s*{", 0.9),
                (r"type\s+\w+\s*=", 0.9),
                (r"(public|private|protected)\s+\w+", 0.8),
                (r"<[^>]+>", 0.4),
                (r"implements\s+\w+", 0.9),
                (r"@\w+Decorator", 0.8)
            ]
        }
        # ... Add more language patterns ...
        
        scores = {lang: 0.0 for lang in patterns}
        for lang, pattern_list in patterns.items():
            for pattern, weight in pattern_list:
                matches = len(re.findall(pattern, text, re.MULTILINE))
                if matches:
                    scores[lang] += min(matches * weight, weight)
                    
        # Normalize scores
        max_score = max(scores.values(), default=0)
        if max_score > 0:
            scores = {lang: score/max_score for lang, score in scores.items()}
            
        return scores

    def sniff(self, payload: bytes) -> Result:
        """Enhanced classification method using multi-modal analysis."""
        # Step 1: Text normalization and quality check
        text, encoding_conf = self.normalize_text(payload)
        if not text:
            return Result(candidates=[])
            
        entropy, printable_ratio = self.check_text_quality(text)
        if entropy < 0.5 or printable_ratio < 0.8:
            return Result(candidates=[])

        # Smart sampling for large texts
        text = self.smart_sample_text(text)
        text_hash = str(hash(text))

        # Step 2: Feature extraction
        with torch.no_grad():
            # 2.1: Transformer features with caching
            transformer_features = self.get_transformer_features(text_hash, text)
            
            # 2.2: Statistical features
            statistical_features = self.extract_statistical_features(text)
            
            # Step 3: Multi-modal classification
            logits, confidence = self.classifier(
                transformer_features,
                statistical_features.unsqueeze(0)
            )
            
            # Get top-5 predictions
            probs = torch.softmax(logits, dim=1)
            values, indices = torch.topk(probs[0], 5)
            
            # Step 4: Additional context analysis
            embedded_types = self.detect_embedded_content(text)
            shebang_match = self.shebang_pattern.search(text)
            language_scores = self._guess_language(text)
            
            # Check for specific file patterns with weights
            file_type_scores = {}
            for file_type, patterns in self.file_patterns.items():
                score = 0.0
                total_weight = 0.0
                for pattern, weight in patterns:
                    matches = len(re.findall(pattern, text, re.MULTILINE))
                    if matches:
                        score += min(matches * weight, weight)
                    total_weight += weight
                if score > 0:
                    file_type_scores[file_type] = score / total_weight
            
            # Create candidates
            candidates = []
            for conf, idx in zip(values, indices):
                lang_type = self.classifier.id2label[idx.item()]
                
                # Base confidence from model
                final_conf = conf.item() * confidence.item()
                
                # Boost confidence based on context
                if shebang_match and shebang_match.group(1) == lang_type:
                    final_conf = min(final_conf + 0.1, 0.99)
                    
                if lang_type in embedded_types:
                    final_conf = min(final_conf + embedded_types[lang_type] * 0.1, 0.99)
                
                # Boost confidence based on language patterns
                if lang_type in language_scores:
                    pattern_conf = language_scores[lang_type]
                    final_conf = min(final_conf + pattern_conf * 0.2, 0.99)
                
                # Boost confidence based on file type patterns
                if lang_type in file_type_scores:
                    pattern_conf = file_type_scores[lang_type]
                    final_conf = min(final_conf + pattern_conf * 0.3, 0.99)
                
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
                        "language_scores": language_scores,
                        "file_type_scores": file_type_scores,
                        "statistical_features": statistical_features.tolist()
                    }
                )
                candidates.append(cand)
            
        return Result(candidates=candidates)

    def __del__(self):
        """Cleanup resources."""
        self.executor.shutdown(wait=False) 