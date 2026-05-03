# Contract: Comparison Runner Interface

**Feature**: `002-enhanced-gui-solvers` | **File**: `numcore_engine/comparison.py`

## ComparisonRunner

```python
class ComparisonRunner:
    def run(
        self,
        solvers: List[Solver],
        problem: Dict[str, Any],
        chapter: int,
        problem_type: str,
    ) -> ComparisonResult: ...
```

- `solvers`: List of instantiated Solver objects. Each must implement the Solver Protocol.
- `problem`: Dict of all input parameters (superset of all solver needs). Each solver calls `validate_input(**problem)` and uses only its relevant keys.
- `chapter`: 1–4
- `problem_type`: `"root_finding"` | `"linear_system"` | `"interpolation"` | `"integration"`

## Chapter Convenience Wrappers

```python
def chapter_1_compare(func: str, a: float, b: float, x0: float, x1: float,
                       tol: float = 1e-6, max_iter: int = 100) -> ComparisonResult:
    """Run all 4 root finders on the same problem."""

def chapter_2_compare(A: list, b_vec: list, tol: float = 1e-6,
                       max_iter: int = 100) -> ComparisonResult:
    """Run Jacobi and Gauss-Seidel on the same linear system."""

def chapter_3_compare(x_points: list, y_points: list,
                       eval_x: float = None) -> ComparisonResult:
    """Run all 5 interpolation methods on the same dataset."""

def chapter_4_compare(func: str, a: float, b: float,
                       n: int) -> ComparisonResult:
    """Run all 4 integration rules on the same problem."""
```

## Best Method Selection Rule

- Among all `SimulationData` where `converged=True`: select the one with minimum `iterations`.
- If all diverged: `best_method = None`.
- Ties: prefer the method listed first in `solvers` list (deterministic order).
