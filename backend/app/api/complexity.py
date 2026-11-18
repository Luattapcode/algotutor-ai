from fastapi import APIRouter
from app.schemas.complexity import ComplexityRequest, ComplexityReport
from app.engines.complexity_analyzer import ComplexityAnalyzer

router = APIRouter(prefix="/api/complexity", tags=["Complexity"])


@router.post("/analyze", response_model=ComplexityReport)
def analyze_code_complexity(request: ComplexityRequest) -> ComplexityReport:
    """Analyze submitted Python code for time (Big-O) and space complexity using AST."""
    return ComplexityAnalyzer.analyze(request)