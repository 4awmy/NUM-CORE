# Data Model: Enhanced GUI, Auto-Solver Comparison, and Course-Complete Solver Suite

**Feature**: `002-enhanced-gui-solvers` | **Date**: 2026-05-03

---

## Core Entities

### `NumericalStep` (existing — extend)

Single iteration record. Extend `data` dict to include method-specific keys.

| Field | Type | Description |
|-------|------|-------------|
| `iteration` | `int` | Iteration number (1-based) |
| `x_value` | `float` | Current approximation |
| `error` | `float` | Absolute error this iteration |
| `data` | `dict[str, Any]` | Method-specific columns (see per-method schemas below) |

**Method-specific `data` schemas**:

| Method | Keys in `data` |
|--------|---------------|
| Bisection | `a`, `b`, `c`, `f_a`, `f_b`, `f_c`, `error` (= \|b-a\|/2) |
| Secant | `x0`, `x1`, `f_x0`, `f_x1` |
| Newton-Raphson | `x_n`, `f_xn`, `f_prime_xn` |
| Simple Iteration | `x_n`, `g_xn` |
| Jacobi / Gauss-Seidel | `x_vector` (list of floats), `residual` |

---

### `SimulationData` (existing — extend)

Output of a single solver run.

| Field | Type | Description |
|-------|------|-------------|
| `method_name` | `str` | Human-readable method label |
| `solution` | `float \| list[float]` | Root (scalar) or solution vector (list) |
| `iterations` | `int` | Total iterations executed |
| `converged` | `bool` | Whether solver converged within tolerance |
| `steps` | `list[NumericalStep]` | Full iteration history |
| `metadata` | `dict[str, Any]` | Method-specific extra data (see below) |

**New metadata keys**:

| Key | Type | Set by | Description |
|-----|------|--------|-------------|
| `diverged` | `bool` | All iterative solvers | True if 5+ consecutive growing errors |
| `convergence_check_value` | `float` | SimpleIterationSolver | \|g′(x₀)\| |
| `convergence_check_passed` | `bool` | SimpleIterationSolver | True if \|g′(x₀)\| < 1 |
| `x0_check_passed` | `bool` | NewtonRaphsonSolver | True if f(x₀)·f″(x₀) > 0 |
| `sdd_check` | `list[dict]` | Jacobi, GaussSeidel | Per-row: `{"row": i, "lhs": float, "rhs": float, "passed": bool}` |
| `sdd_reordered` | `bool` | Jacobi, GaussSeidel | True if rows were reordered |
| `update_type` | `str` | Jacobi, GaussSeidel | `"simultaneous"` or `"successive"` |
| `dd_table` | `list[list[float]]` | Newton Divided Diff solvers | Full 2D divided difference table |
| `polynomial_str` | `str` | All interpolation solvers | Human-readable polynomial formula |
| `h` | `float` | All integration solvers | Step size h = (b-a)/n |
| `xy_table` | `list[dict]` | All integration solvers | `[{"x": float, "y": float, "weight": float}]` |
| `weighted_sum_str` | `str` | All integration solvers | Expanded formula string for display |
| `n_even_check` | `bool` | SimpsonsOneThirdSolver | True if n is even |
| `n_mod3_check` | `bool` | SimpsonsThreeEighthsSolver | True if n % 3 == 0 |
| `computation_time_ms` | `float` | All solvers | Wall-clock time in milliseconds |

---

### `ComparisonResult` (NEW)

Output of running multiple solvers on the same input.

| Field | Type | Description |
|-------|------|-------------|
| `chapter` | `int` | Chapter number (1–4) |
| `problem_type` | `str` | E.g., `"root_finding"`, `"linear_system"`, `"interpolation"`, `"integration"` |
| `input_params` | `dict[str, Any]` | All input parameters provided (superset) |
| `results` | `list[SimulationData]` | One result per solver, in order |
| `best_method` | `str \| None` | `method_name` of the solver with fewest iterations among converged; `None` if all diverged |
| `timestamp` | `str` | ISO datetime of the comparison run |

---

### `EquationInput` (conceptual — widget state)

Not a stored entity; represents the state of the equation input widget at any time.

| Field | Type | Description |
|-------|------|-------------|
| `raw_text` | `str` | What the user typed (e.g., `"x^2 + sin(x)"`) |
| `normalized` | `str` | Python-safe expression (e.g., `"x**2 + sin(x)"`) |
| `display_latex` | `str` | MathText string for preview (e.g., `"$x^{2} + \\sin(x)$"`) |
| `is_valid` | `bool` | Whether the expression parses correctly |
| `error_message` | `str \| None` | Hint string if invalid |

---

## Validation Rules

| Entity | Field | Rule |
|--------|-------|------|
| EquationInput | `raw_text` | Must parse to a valid Python expression after `^`→`**` normalization |
| BisectionSolver | `a, b` | f(a)·f(b) < 0 required before solving |
| SimpleIterationSolver | `g(x)` | Must be a valid callable expression; convergence check run automatically |
| Newton Divided Difference | `x_points` | All x values must be unique |
| CompositeSimpsonsOneThird | `n` | n must be even (≥2) |
| CompositeSimpsonsThreeEighths | `n` | n must be divisible by 3 (≥3) |
| Linear solvers | Matrix A | Square matrix required; warn if singular (det ≈ 0) |

---

## State Transitions — Solver Lifecycle

```
IDLE → VALIDATING_INPUT → RUNNING → CONVERGED
                       ↓          → DIVERGED
                       → VALIDATION_ERROR
```

| State | Display | Action |
|-------|---------|--------|
| `IDLE` | Empty result panel; Solve button enabled | Awaiting user input |
| `VALIDATING_INPUT` | Inline error labels shown/cleared | Parser + bounds checks run |
| `RUNNING` | Progress indicator; Solve button disabled | Solver iterating |
| `CONVERGED` | Results table + plot shown; green status | |
| `DIVERGED` | Results table with divergence warning; amber status | |
| `VALIDATION_ERROR` | Inline error near relevant field; red text | User must correct input |
