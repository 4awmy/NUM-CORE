# Contract: Solver Protocol Interface

**Feature**: `002-enhanced-gui-solvers` | **File**: `numcore_engine/interfaces.py`

## Solver Protocol (frozen — DO NOT CHANGE)

All solver classes MUST implement this Protocol exactly:

```python
class Solver(Protocol):
    def solve(self, **kwargs: Any) -> SimulationData: ...
    def get_steps(self) -> List[NumericalStep]: ...
    def validate_input(self, **kwargs: Any) -> bool: ...
```

## Per-Solver Input Contracts

### Chapter 1 — Root Finding

| Solver | Required kwargs | Optional kwargs |
|--------|----------------|-----------------|
| `BisectionSolver` | `func: str`, `a: float`, `b: float` | `tol: float=1e-6`, `max_iter: int=100` |
| `SecantSolver` | `func: str`, `x0: float`, `x1: float` | `tol: float=1e-6`, `max_iter: int=100` |
| `NewtonRaphsonSolver` | `func: str`, `x0: float` | `tol: float=1e-6`, `max_iter: int=100` |
| `SimpleIterationSolver` | `g_func: str`, `x0: float` | `tol: float=1e-6`, `max_iter: int=100` |

### Chapter 2 — Linear Systems

| Solver | Required kwargs | Optional kwargs |
|--------|----------------|-----------------|
| `JacobiSolver` | `A: list[list[float]]`, `b: list[float]` | `x0: list[float]=None`, `tol: float=1e-6`, `max_iter: int=100` |
| `GaussSeidelSolver` | `A: list[list[float]]`, `b: list[float]` | `x0: list[float]=None`, `tol: float=1e-6`, `max_iter: int=100` |

### Chapter 3 — Interpolation

| Solver | Required kwargs | Optional kwargs |
|--------|----------------|-----------------|
| `LagrangeInterpolationSolver` | `x_points: list[float]`, `y_points: list[float]` | `eval_x: float=None` |
| `NewtonForwardDifferenceSolver` | `x_points: list[float]`, `y_points: list[float]` | `eval_x: float=None` |
| `NewtonBackwardDifferenceSolver` | `x_points: list[float]`, `y_points: list[float]` | `eval_x: float=None` |
| `NewtonForwardDividedDifferenceSolver` | `x_points: list[float]`, `y_points: list[float]` | `eval_x: float=None` |
| `NewtonBackwardDividedDifferenceSolver` | `x_points: list[float]`, `y_points: list[float]` | `eval_x: float=None` |

### Chapter 4 — Integration

| Solver | Required kwargs | Optional kwargs |
|--------|----------------|-----------------|
| `CompositeTrapezoidalSolver` | `func: str`, `a: float`, `b: float`, `n: int` | — |
| `CompositeMidpointSolver` | `func: str`, `a: float`, `b: float`, `n: int` | — |
| `CompositeSimpsonsOneThirdSolver` | `func: str`, `a: float`, `b: float`, `n: int` | — |
| `CompositeSimpsonsThreeEighthsSolver` | `func: str`, `a: float`, `b: float`, `n: int` | — |

## Output Contract

All solvers return `SimulationData` with:
- `solution`: root (float) or solution vector (list[float]) or integral value (float)
- `converged`: True if tolerance reached within max_iter
- `metadata["diverged"]`: True if 5+ consecutive growing errors (iterative solvers only)
- `metadata["computation_time_ms"]`: float — wall-clock ms
