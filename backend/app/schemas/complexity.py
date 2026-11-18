from pydantic import BaseModel
from typing import List


class ComplexityRequest(BaseModel):
    code: str


class ComplexityReport(BaseModel):
    max_loop_depth: int
    has_recursion: bool
    allocated_structures: List[str]
    estimated_time_complexity: str
    estimated_space_complexity: str
    explanation: str