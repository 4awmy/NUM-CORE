# Contract: Solver Interface

**Type**: Python Protocol
**File**: `numcore_engine/interfaces.py`
**Stability**: Frozen (do not change)

## Protocol Definition

All solver classes MUST implement the `Solver` Protocol:

```python
class Solver(Protocol):
    def solve(self, **kwargs: Any) -> SimulationData: ...
    def get_steps(self) -> List[NumericalStep]: ...
    def validate_input(self, **kwargs: Any) -> bool: ...
```

## Solver Implementations & Contracts

### NewtonRaphsonSolver
```
solve(func_str: str, x0: float, tol: float = 1e-6, max_iter: int = 100)
  → SimulationData with metadata keys:
      solution: float, converged: bool, diverged: bool,
      iterations: int, method: "newton_raphson"
```

### SimpleIterationSolver
```
solve(func_str: str, x0: float, tol: float = 1e-6, max_iter: int = 100)
  → SimulationData with same metadata shape as NewtonRaphson
      method: "simple_iteration"
```

### GaussSeidelSolver
```
solve(A: List[List[float]], b: List[float], x0: Optional[List[float]] = None,
      tol: float = 1e-6, max_iter: int = 100)
  → SimulationData with metadata keys:
      solution: List[float], converged: bool, diverged: bool,
      iterations: int, method: "gauss_seidel",
      reordered: bool (True if diagonal dominance required row swap)
```

### JacobiSolver *(NEW)*
```
solve(A: List[List[float]], b: List[float], x0: Optional[List[float]] = None,
      tol: float = 1e-6, max_iter: int = 100)
  → SimulationData with same metadata shape as GaussSeidel
      method: "jacobi"
```

### InterpolationSolver
```
solve(x_points: List[float], y_points: List[float])
  → SimulationData with metadata keys:
      coefficients: List[float], polynomial_str: str,
      method: "newton_divided_difference"
```

### IntegrationSolver
```
solve(x_points: List[float], y_points: List[float],
      method: str = "trapezoidal")  # or "simpsons"
  → SimulationData with metadata keys:
      integral: float, method: "trapezoidal" | "simpsons"
```

## Divergence Detection Contract

All iterative solvers (Newton-Raphson, Simple Iteration, Gauss-Seidel, Jacobi) MUST:
1. Track rolling error window of last 5 steps
2. If all 5 errors are monotonically increasing → set `metadata["diverged"] = True`, break
3. Set `metadata["converged"] = False` when diverged
