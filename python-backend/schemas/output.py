from pydantic import BaseModel, Field
from typing import List

class IncidentSummary(BaseModel):
    root_cause: str = Field(description="Primary root cause of the incident")
    impact: str = Field(description="Impact on users or systems")
    recommended_actions: List[str] = Field(description="Step‑by‑step remediation actions")
    confidence_score: float = Field(ge=0, le=1, description="Confidence in the analysis")