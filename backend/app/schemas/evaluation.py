from pydantic import BaseModel, Field
from typing import List


class DimensionScore(BaseModel):
    score: int = Field(..., ge=0, description="Points awarded")
    max_score: int
    feedback: str = Field(..., description="Actionable feedback for improvement")


class EvaluationRequest(BaseModel):
    problem_id: str
    problem_title: str
    explanation_text: str  # The candidate's spoken or typed explanation


class EvaluationResponse(BaseModel):
    total_score: int = Field(..., ge=0, le=100)
    verdict: str  # "Strong Hire", "Hire", "Lean Hire", "Needs Improvement"
    algorithmic_correctness: DimensionScore
    technical_vocabulary: DimensionScore
    edge_cases: DimensionScore
    english_delivery: DimensionScore
    native_speaker_rewrites: List[str] = Field(
        ...,
        description="How a native Big Tech engineer would explain this exact approach",
    )