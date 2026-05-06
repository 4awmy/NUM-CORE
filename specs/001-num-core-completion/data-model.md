# Data Model: NUM-CORE Complete Solver Suite

**Phase**: 1 — Design
**Date**: 2026-04-29

## Core Entities

### NumericalStep *(existing — extend)*
Single iteration record produced by any solver.

| Field | Type | Description |
|-------|------|-------------|
| `step_idx` | `int` | Iteration number (0-indexed) |
| `value` | `float` | Current approximation (root, x_i, etc.) |
| `error` | `Optional[float]` | Absolute error vs previous step |
| `details` | `Dict[str, Any]` | Method-specific extras (f(x), derivative, etc.) |

**Validation**: `error >= 0`; `step_idx >= 0`

**State transitions**: `running → converged | diverged | max_iterations_reached`

---

### SimulationData *(existing — extend)*
Complete result of a solver run, returned by `solve()`.

| Field | Type | Description |
|-------|------|-------------|
| `title` | `str` | Human-readable solver + problem description |
| `x_data` | `List[float]` | Iteration numbers (for plot x-axis) |
| `y_data` | `List[float]` | Error values per iteration (for plot y-axis) |
| `metadata` | `Dict[str, Any]` | Root/solution, converged, diverged, iterations, method |

**Key metadata fields** (standardized across all solvers):

| Key | Type | Description |
|-----|------|-------------|
| `"solution"` | `float` or `List[float]` | Final answer (root or solution vector) |
| `"converged"` | `bool` | Whether tolerance was reached |
| `"diverged"` | `bool` | Whether divergence was detected (5-step rule) |
| `"iterations"` | `int` | Total iterations performed |
| `"method"` | `str` | Solver name (e.g., `"newton_raphson"`) |
| `"tolerance"` | `float` | Convergence tolerance used |

---

### Problem *(conceptual — lives in caller code)*
Represents a user-configured solver run. Not persisted.

| Field | Type | Description |
|-------|------|-------------|
| `solver_type` | `str` | `"newton_raphson"`, `"jacobi"`, `"interpolation"`, etc. |
| `func_str` | `Optional[str]` | Function expression string (root finding) |
| `matrix` | `Optional[List[List[float]]]` | Coefficient matrix A (linear systems) |
| `b_vector` | `Optional[List[float]]` | RHS vector b |
| `data_points` | `Optional[List[tuple[float,float]]]` | (x,y) pairs (calculus) |
| `initial_guess` | `Optional[float]` | Starting point (root finders) |
| `tolerance` | `float` | Default: `1e-6` |
| `max_iterations` | `int` | Default: `100` |

---

### IterationStep *(CSV export model)*
Row in exported CSV. Derived from `NumericalStep` + method context.

**Root Finder columns**: `iteration, x_n, f(x_n), f'(x_n), error, converged`
**Linear System columns**: `iteration, x1, x2, ..., xn, error, converged`
**Calculus / Integration columns**: `interval, method, area_estimate, error`

---

### DataPoint *(calculus only)*
A single (x, y) experimental measurement.

| Field | Type | Constraint |
|-------|------|-----------|
| `x` | `float` | Must be unique per problem |
| `y` | `float` | Any real value |

**Validation**: No duplicate x values; minimum 2 points for interpolation.

---

## Entity Relationships

```
Problem
  ├── runs → Solver (one of: NewtonRaphson, SimpleIteration, GaussSeidel, Jacobi,
  │                           InterpolationSolver, IntegrationSolver)
  └── produces → SimulationData
                    ├── contains → List[NumericalStep]
                    └── exported_as → List[IterationStep] → CSV file
```

## State Machine: Solver Lifecycle

```
IDLE ──[solve() called]──→ RUNNING
  RUNNING ──[error < tol]──────────→ CONVERGED
  RUNNING ──[error grows 5 steps]──→ DIVERGED (early break)
  RUNNING ──[i >= max_iters]───────→ MAX_ITERATIONS_REACHED
```

All terminal states set `SimulationData.metadata["converged"]` and `["diverged"]` accordingly.
