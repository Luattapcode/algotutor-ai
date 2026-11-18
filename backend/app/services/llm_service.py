import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from app.schemas.hint import HintTier

# Load environment variables from .env
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)
load_dotenv()


def get_gemini_client():
    load_dotenv(dotenv_path=env_path, override=True)
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return None
    return genai.Client(api_key=key.strip())


SYSTEM_PROMPT = """
You are a Principal Software Engineer at Google conducting a technical interview.
Your goal is to guide the candidate using the Socratic method without ever spoiling the answer.

CRITICAL GUARDRAIL RULES:
1. NEVER output solution code (no Python, C++, Java, or syntax).
2. NEVER reveal the complete end-to-end approach all at once.
3. Keep your response concise (2-4 sentences max).
4. Adapt your tone to be encouraging, professional, and intellectually stimulating.
"""

TIER_INSTRUCTIONS = {
    HintTier.CLARIFICATION: (
        "Focus ONLY on problem constraints, edge cases, and clarifications. "
        "Ask the candidate about empty inputs, duplicates, or negative bounds."
    ),
    HintTier.INTUITION: (
        "Guide the candidate toward the high-level intuition. "
        "Ask a leading question to help them see the mathematical pattern (e.g. complement = target - num)."
    ),
    HintTier.DATA_STRUCTURE: (
        "Ask which data structure would allow fast O(1) lookups for seen numbers."
    ),
    HintTier.PSEUDOCODE: (
        "Provide step-by-step logical bullet points (pseudocode logic, NO actual code)."
    ),
}

# The model Google assigned to your account
MODELS_TO_TRY = [
    "gemini-3.8-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]


class GeminiService:
    """Interacts with Google Gemini with automatic retry and clear error logging."""

    @staticmethod
    def generate_socratic_hint(problem_id: str, current_code: str, tier: HintTier) -> str:
        client = get_gemini_client()
        if not client:
            return "API Key not configured. Please check .env file."

        prompt = f"""
{SYSTEM_PROMPT}

Candidate is working on problem: '{problem_id}'.
Their current code draft:

CURRENT TASK: Provide a Tier {tier.value} ({tier.name}) hint.
DIRECTIVE FOR THIS TIER:
{TIER_INSTRUCTIONS[tier]}
"""
        last_error = None
        for m in MODELS_TO_TRY:
            for attempt in range(2):  # Try twice with backoff if busy
                try:
                    res = client.models.generate_content(model=m, contents=prompt)
                    if res and res.text:
                        return res.text.strip()
                except Exception as e:
                    last_error = e
                    print(f"[DEBUG Gemini] Model {m} (attempt {attempt + 1}) failed: {e}")
                    time.sleep(1)  # Wait 1s before retry

        # If all fail, display the real reason so we can debug!
        return f"AI Hint temporarily unavailable ({last_error}). Please try again in 5 seconds."

    @staticmethod
    def evaluate_explanation_with_ai(problem_title: str, explanation: str) -> str:
        client = get_gemini_client()
        if not client:
            return "API Key not configured."

        prompt = f"""
You are an expert Big Tech interviewer and technical communication coach.
Evaluate this candidate's "thinking out loud" explanation for: '{problem_title}'.

CANDIDATE'S EXPLANATION:
"{explanation}"

EVALUATE ACROSS 4 DIMENSIONS:
1. Algorithmic Correctness (Max 30 pts)
2. Technical Vocabulary (Max 25 pts)
3. Edge Case Coverage (Max 20 pts)
4. English Fluency & Natural Delivery (Max 25 pts)

YOUR TASK:
Provide:
- A Total Score (0-100) and Verdict (Strong Hire / Hire / Lean Hire / Needs Improvement).
- Specific, friendly English grammar and phrasing corrections.
- A "Native Speaker Rewrite": The exact 2-3 sentences a native Google engineer would say.

Keep your response structured, concise, and constructive.
"""
        last_error = None
        for m in MODELS_TO_TRY:
            try:
                res = client.models.generate_content(model=m, contents=prompt)
                if res and res.text:
                    return res.text.strip()
            except Exception as e:
                last_error = e
                print(f"[DEBUG Gemini Eval] {m} failed: {e}")
                continue

        return f"Could not evaluate with AI ({last_error})."