from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.hints import router as hints_router
from app.api.complexity import router as complexity_router
from app.api.evaluation import router as evaluation_router
from app.services.leetcode_service import LeetCodeService
from fastapi import HTTPException

app = FastAPI(
    title="AlgoTutor AI Backend",
    description="Intelligent Big Tech Mock Interview Platform",
    version="1.0.0",
)

# Allow Frontend (localhost:3000) to communicate with Backend (localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[*],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(hints_router)
app.include_router(complexity_router)
app.include_router(evaluation_router)


@app.get("/")
def health_check():
    return {"status": "healthy", "service": "AlgoTutor AI API"}

@app.get("/api/leetcode/{title_slug}")
async def get_leetcode_problem(title_slug: str):
    """Fetch any problem dynamically from LeetCode by its slug (e.g. 'two-sum', 'lru-cache')."""
    problem = await LeetCodeService.fetch_problem(title_slug)
    if not problem:
        raise HTTPException(
            status_code=404, 
            detail=f"Problem '{title_slug}' not found on LeetCode or rate-limited."
        )
    return problem