import ast
from app.schemas.complexity import ComplexityRequest, ComplexityReport


class ComplexityVisitor(ast.NodeVisitor):
    """Walks the Python Abstract Syntax Tree (AST) to measure loops and recursion."""

    def __init__(self):
        self.max_loop_depth = 0
        self.current_loop_depth = 0
        self.function_names = set()
        self.recursive_calls = set()
        self.allocations = set()

    def visit_FunctionDef(self, node):
        self.function_names.add(node.name)
        self.generic_visit(node)

    def visit_For(self, node):
        self.current_loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.current_loop_depth)
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_While(self, node):
        self.current_loop_depth += 1
        self.max_loop_depth = max(self.max_loop_depth, self.current_loop_depth)
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.function_names:
                self.recursive_calls.add(node.func.id)
            if node.func.id in {"list", "dict", "set"}:
                self.allocations.add(node.func.id)
        self.generic_visit(node)

    def visit_Dict(self, node):
        self.allocations.add("dict")
        self.generic_visit(node)

    def visit_List(self, node):
        self.allocations.add("list")
        self.generic_visit(node)

    def visit_Set(self, node):
        self.allocations.add("set")
        self.generic_visit(node)


class ComplexityAnalyzer:
    """Analyzes candidate code Big-O time and space complexity."""

    @staticmethod
    def analyze(request: ComplexityRequest) -> ComplexityReport:
        try:
            tree = ast.parse(request.code)
        except SyntaxError as e:
            return ComplexityReport(
                max_loop_depth=0,
                has_recursion=False,
                allocated_structures=[],
                estimated_time_complexity="Syntax Error",
                estimated_space_complexity="Syntax Error",
                explanation=f"Code has syntax errors: {str(e)}",
            )

        visitor = ComplexityVisitor()
        visitor.visit(tree)

        depth = visitor.max_loop_depth
        has_rec = len(visitor.recursive_calls) > 0
        allocations = sorted(list(visitor.allocations))

        # Time Complexity estimation
        if has_rec:
            time_est = "O(2^N) or O(N log N) [Recursive]"
            time_expl = "Detected recursive function calls."
        elif depth == 0:
            time_est = "O(1)"
            time_expl = "Constant time: No loops or recursion detected."
        elif depth == 1:
            time_est = "O(N)"
            time_expl = "Linear time: Single loop pass over input."
        elif depth == 2:
            time_est = "O(N^2)"
            time_expl = "Quadratic time: Nested loops detected (loop inside loop)."
        else:
            time_est = f"O(N^{depth})"
            time_expl = f"Detected {depth} levels of nested loops."

        # Space Complexity estimation
        if allocations or has_rec:
            space_est = "O(N)"
            space_expl = f"Allocates dynamic data structures: {', '.join(allocations) if allocations else 'recursion stack'}."
        else:
            space_est = "O(1)"
            space_expl = "Operates in-place with no additional dynamic memory allocations."

        return ComplexityReport(
            max_loop_depth=depth,
            has_recursion=has_rec,
            allocated_structures=allocations,
            estimated_time_complexity=time_est,
            estimated_space_complexity=space_est,
            explanation=f"{time_expl} {space_expl}",
        )