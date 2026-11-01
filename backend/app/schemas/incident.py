from pydantic import BaseModel, Field
from typing import Literal


class LogAnalysisRequest(BaseModel):
    log_text: str = Field(min_length=20, max_length=20000)


class LogAnalysisResponse(BaseModel):
    severity: Literal["low", "medium", "high", "critical", "unknown"]
    category: str
    summary: str
    likely_root_cause: str
    possible_causes: list[str]
    recommended_actions: list[str]
    evidence: list[str]
    confidence: Literal["low", "medium", "high"]
