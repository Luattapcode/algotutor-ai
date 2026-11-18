from fastapi import APIRouter
from app.schemas.hint import HintRequest, HintResponse
from app.engines.hint_engine import HintEngine

# Create an APIRouter instance
router = APIRouter(prefix="/api/hints", tags=["Hints"])


@router.post("/next", response_model=HintResponse)
def get_next_hint(request: HintRequest) -> HintResponse:
    """
    Request the next progressive hint tier.
    Enforces anti-spoiler state transitions:
    Level 1 (Clarification) -> Level 2 (Intuition) -> Level 3 (Data Structure) -> Level 4 (Pseudocode)
    """
    return HintEngine.get_next_hint(request)