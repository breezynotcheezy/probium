from __future__ import annotations
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict

class Candidate(BaseModel):
    media_type: str
    extension: Optional[str] = None
    confidence: float = Field(ge=0, le=1)
    breakdown: Dict[str, float] | None = None

class Result(BaseModel):
    """Unified return object for every engine.

    Engines can populate only *candidates*; framework fills the rest.
    """
    engine: str = ""
    bytes_analyzed: int = 0
    elapsed_ms: float = 0.0
    candidates: List[Candidate]
    error: str | None = None
    hash: str | None = None


class DetectionResult(BaseModel):
    file_name: str
    detected_type: str

    
    confidence_score: float = Field(ge=0, le=100)
    detection_method: str
    timestamp: str
    errors: List[str] = []
    warnings: List[str] = []
    analysis_time: float | None = None
    file_size: int | None = None
    mime_type: str | None = None
    extension: str | None = None
