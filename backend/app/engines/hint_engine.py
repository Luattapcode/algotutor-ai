from app.schemas.hint import HintTier, HintRequest, HintResponse
from app.services.llm_service import GeminiService


class HintEngine:
    """Core progressive hint engine enforcing anti-spoiler state transitions."""

    @staticmethod
    def get_next_hint(request: HintRequest) -> HintResponse:
        current_tier = request.current_tier

        # If user already reached max tier
        if current_tier >= HintTier.PSEUDOCODE:
            return HintResponse(
                tier=HintTier.PSEUDOCODE,
                tier_name=HintTier.PSEUDOCODE.name,
                hint_message="You have unlocked all hint tiers! Give it your best shot and write the code.",
                next_tier_available=False,
            )

        # Transition to next tier (1 -> 2 -> 3 -> 4)
        next_tier = HintTier(current_tier + 1)

        # Call the live AI Gemini Service with Anti-Spoiler Guardrails!
        hint_msg = GeminiService.generate_socratic_hint(
            problem_id=request.problem_id,
            current_code=request.current_code,
            tier=next_tier,
        )

        return HintResponse(
            tier=next_tier,
            tier_name=next_tier.name,
            hint_message=hint_msg,
            next_tier_available=(next_tier < HintTier.PSEUDOCODE),
        )