import httpx
from typing import Optional, Dict, Any


LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"

# The official GraphQL query LeetCode uses for problem details
QUESTION_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId
    title
    titleSlug
    difficulty
    content
    categoryTitle
    codeSnippets {
      lang
      langSlug
      code
    }
    sampleTestCase
  }
}
"""


class LeetCodeService:
    """Fetches real algorithmic problems dynamically from LeetCode's GraphQL engine."""

    @staticmethod
    async def fetch_problem(title_slug: str) -> Optional[Dict[str, Any]]:
        headers = {
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        }

        payload = {
            "query": QUESTION_QUERY,
            "variables": {"titleSlug": title_slug.strip().lower()},
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(LEETCODE_GRAPHQL_URL, json=payload, headers=headers)
                if res.status_code != 200:
                    return None

                data = res.json()
                question = data.get("data", {}).get("question")
                if not question:
                    return None

                # Extract Python 3 starter code
                python_starter = ""
                for snippet in question.get("codeSnippets", []):
                    if snippet.get("langSlug") == "python3":
                        python_starter = snippet.get("code")
                        break

                return {
                    "id": question.get("titleSlug"),
                    "frontend_id": question.get("questionFrontendId"),
                    "title": f"{question.get('questionFrontendId')}. {question.get('title')}",
                    "difficulty": question.get("difficulty"),
                    "category": question.get("categoryTitle", "Algorithms"),
                    "content_html": question.get("content"),
                    "starter_code": python_starter or "def solution():\n    pass\n",
                    "sample_test_case": question.get("sampleTestCase"),
                }
        except Exception as e:
            print(f"[ERROR] Failed to fetch from LeetCode: {e}")
            return None