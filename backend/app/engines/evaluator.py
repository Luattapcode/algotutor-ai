from app.schemas.evaluation import EvaluationRequest, EvaluationResponse, DimensionScore

# Technical CS vocabulary expected in top-tier interview explanations
TECHNICAL_KEYWORDS = {
    "hash map", "hash table", "dictionary", "constant time", "o(1)", "o(n)",
    "linear time", "space complexity", "time complexity", "complement",
    "two pointers", "lookup", "iterate", "array", "indices", "index"
}

# Edge case indicators
EDGE_CASE_KEYWORDS = {
    "empty", "null", "none", "negative", "duplicate", "single element",
    "no solution", "bounds", "overflow", "edge case"
}


class CommunicationEvaluator:
    """Evaluates candidates' technical explanations and English articulation."""

    @staticmethod
    def evaluate(request: EvaluationRequest) -> EvaluationResponse:
        text = request.explanation_text.strip().lower()

        # 1. Technical Vocabulary (Max 25 pts)
        matched_tech = [kw for kw in TECHNICAL_KEYWORDS if kw in text]
        vocab_score = min(25, max(5, len(matched_tech) * 5))
        vocab_fb = (
            f"Great technical vocabulary: {', '.join(matched_tech[:3])}."
            if matched_tech
            else "Try using more precise terminology like 'hash map', 'complement', or 'constant time lookup'."
        )

        # 2. Edge Cases (Max 20 pts)
        matched_edge = [kw for kw in EDGE_CASE_KEYWORDS if kw in text]
        edge_score = 20 if len(matched_edge) >= 2 else (10 if len(matched_edge) == 1 else 5)
        edge_fb = (
            f"Good job mentioning edge conditions like: {', '.join(matched_edge)}."
            if matched_edge
            else "You didn't mention edge cases. Always ask: What if the array is empty or has duplicates?"
        )

        # 3. Algorithmic Correctness (Max 30 pts)
        has_hashmap = any(w in text for w in ["hash", "dict", "map", "seen"])
        has_complement = any(w in text for w in ["complement", "target -", "difference", "minus"])

        if has_hashmap and has_complement:
            algo_score = 30
            algo_fb = "Optimal O(N) single-pass hash map approach clearly identified!"
        elif has_hashmap or "two pointer" in text:
            algo_score = 22
            algo_fb = "Good direction! Make sure to explicitly state how you calculate target - num."
        elif "two loop" in text or "nested" in text or "check all" in text:
            algo_score = 15
            algo_fb = "You described the O(N^2) brute-force. Interviewers expect you to optimize to O(N)."
        else:
            algo_score = 10
            algo_fb = "Approach was vague. State your data structures and step-by-step logic clearly."

        # 4. English Delivery & Grammar (Max 25 pts)
        word_count = len(request.explanation_text.split())
        if word_count < 10:
            english_score = 8
            english_fb = "Your explanation was too brief. Real interviewers expect a complete paragraph."
        else:
            english_score = 22
            english_fb = "Clear and structured flow. Keep sentences active and concise."

        # Calculate Total & Verdict
        total = algo_score + vocab_score + edge_score + english_score

        if total >= 85:
            verdict = "Strong Hire"
        elif total >= 70:
            verdict = "Hire"
        elif total >= 55:
            verdict = "Lean Hire"
        else:
            verdict = "Needs Improvement"

        native_rewrite = [
            (
                "Native Phrasing: 'To solve Two Sum in linear time, I will iterate through the array "
                "while maintaining a hash map of visited numbers and their indices. For each element x, "
                "I check if the complement (target - x) exists in the map. If it does, I return both indices; "
                "otherwise, I insert x into the map. This achieves O(N) time and O(N) space.'"
            )
        ]

        return EvaluationResponse(
            total_score=total,
            verdict=verdict,
            algorithmic_correctness=DimensionScore(score=algo_score, max_score=30, feedback=algo_fb),
            technical_vocabulary=DimensionScore(score=vocab_score, max_score=25, feedback=vocab_fb),
            edge_cases=DimensionScore(score=edge_score, max_score=20, feedback=edge_fb),
            english_delivery=DimensionScore(score=english_score, max_score=25, feedback=english_fb),
            native_speaker_rewrites=native_rewrite,
        )