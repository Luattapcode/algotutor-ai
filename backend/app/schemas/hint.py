from enum import Enum
from pydantic import BaseModel

# 1. Define the 4 Progressive Hint Tiers
class HintTier(int, Enum):
    CLARIFICATION = 1    # Checking inputs, edge cases
    INTUITION = 2        # High-level approach
    DATA_STRUCTURE = 3   # The optimal data structure
    PSEUDOCODE = 4       # Step-by-step logic (no raw code)

# 2. What the client sends when requesting a hint
class HintRequest(BaseModel):
    problem_id: str
    current_code: str
    current_tier: int = 0  # 0 means no hint requested yet

# 3. What our AI engine responds with
class HintResponse(BaseModel):
    tier: HintTier
    tier_name: str
    hint_message: str
    next_tier_available: bool