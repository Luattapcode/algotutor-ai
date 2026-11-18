from fastapi import APIRouter
from app.schemas.evaluation import EvaluationRequest, EvaluationResponse
from app.engines.evaluator import CommunicationEvaluator
from app.services.llm_service import GeminiService

router = APIRouter(prefix="/api/evaluation", tags=["Evaluation"])


@router.post("/verbal", response_model=EvaluationResponse)
def evaluate_explanation(request: EvaluationRequest) -> EvaluationResponse:
    """Fast rule-based rubric evaluation."""
    return CommunicationEvaluator.evaluate(request)


@router.post("/verbal-ai")
def evaluate_explanation_ai(request: EvaluationRequest):
    """Deep AI evaluation powered by Gemini for detailed English coaching and Native Phrasing."""
    ai_feedback = GeminiService.evaluate_explanation_with_ai(
        problem_title=request.problem_title,
        explanation=request.explanation_text,
    )
    return {
        "problem_title": request.problem_title,
        "raw_explanation": request.explanation_text,
        "interviewer_coaching": ai_feedback,
    }