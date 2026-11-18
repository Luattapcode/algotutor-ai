# 🚀 AlgoTutor AI — Intelligent Big Tech Mock Interview Platform

An intelligent, full-stack mock technical interview platform simulating a Big Tech interviewer. Bridges the gap between LeetCode algorithmic problem-solving and real technical interview expectations.

## 🌟 Core Features
- **Socratic Progressive Hint State Machine:** 4-tier monotonic hints (Clarification ➔ Intuition ➔ Data Structure ➔ Pseudocode) with strict anti-spoiler prompt guardrails.
- **Static AST Complexity Profiler:** Evaluates loop nesting depth and recursion using Python's `ast.NodeVisitor` for Big-O time and space analysis.
- **100-Point English Articulation Rubric:** Grades candidates' "thinking out loud" verbal intuition, CS vocabulary, and provides native speaker rewrites.
- **Dynamic LeetCode Integration:** Asynchronously queries LeetCode's GraphQL engine to ingest 3,000+ problems and starter code.
- **Resilient AI Architecture:** Google Gemini API with multi-model fallback (`3.8-flash`, `2.0-flash`, `1.5-flash`) for zero downtime.

## 🛠️ Tech Stack
- **Backend:** FastAPI, Python 3.12/3.14, Pydantic, HTTPX, Google GenAI SDK.
- **Frontend:** Next.js 16, React 19, TypeScript, Monaco Editor, Tailwind CSS.
- **DevOps:** Docker, Docker Compose.