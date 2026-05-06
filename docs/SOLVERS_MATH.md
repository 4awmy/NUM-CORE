# NUM-CORE: Mathematical Reference for All Solvers

This document explains the mathematics behind every solver in `numcore_engine/solvers/`.

---

## 1. Root Finders (`root_finder.py`)

All root finders solve for `x` such that `f(x) = 0`.

---

### 1.1 Bisection Method

**Class**: `BisectionSolver`

**Idea**: If `f(a)` and `f(b)` have opposite signs, a root must exist between them (Intermediate Value Theorem). Repeatedly halve the interval.

**Algorithm**:
```
Require: f(a) · f(b) < 0

Loop:
  c = (a + b) / 2
  if f(a) · f(c) < 0:
      b = c          ← root is in left half
  else:
      a = c          ← root is in right half
  error = |b - a| / 2
  stop when error < tolerance
```

**Convergence**: Linear — halves the error each step. Needs roughly `log₂((b-a)/ε)` iterations to reach tolerance `ε`.

**Strengths**: Guaranteed to converge if the bracket is valid.
**Weakness**: Slow compared to Newton-Raphson.

**What each `NumericalStep` stores**: `{a, b, f(a), f(b), c, f(c)}`

---

### 1.2 Newton-Raphson Method

**Class**: `NewtonRaphsonSolver`

**Idea**: Draw a tangent line to `f(x)` at the current guess and find where it hits the x-axis. That intersection is the next guess.

**Formula**:
```
x_{n+1} = x_n - f(x_n) / f'(x_n)
```

**Derivative**: Computed symbolically using SymPy (`sympy.diff`). Falls back to central-difference numerical differentiation if symbolic differentiation fails:
```
f'(x) ≈ [f(x+h) - f(x-h)] / (2h)    with h = 1e-7
```

**Convergence**: Quadratic near the root — the number of correct decimal digits roughly doubles each iteration. Very fast, but sensitive to initial guess.

**Failure modes**:
- `f'(x) ≈ 0` → division by near-zero, step is skipped
- Poor initial guess → can diverge or find a different root

**Divergence detection** (shared with Secant and Simple Iteration):
> If the error increases for 5 consecutive iterations, `diverged = True` and the loop exits.

**What each `NumericalStep` stores**: `{x_n, f(x), f'(x)}`

---

### 1.3 Secant Method

**Class**: `SecantSolver`

**Idea**: Like Newton-Raphson, but avoids computing `f'` analytically. It approximates the derivative using two previous points.

**Formula**:
```
x_{n+1} = x_n - f(x_n) · (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))
```

This is a finite-difference approximation of Newton's tangent, using slope between `(x_{n-1}, f(x_{n-1}))` and `(x_n, f(x_n))`.

**Requires**: Two initial guesses `x0` and `x1` (they do not need to bracket the root).

**Convergence**: Superlinear — order ≈ 1.618 (golden ratio). Faster than Bisection, slightly slower than Newton-Raphson, but requires no derivative.

**Guard**: If `|f(x_n) - f(x_{n-1})| < 1e-12`, the method stops to avoid division by zero.

**What each `NumericalStep` stores**: `{x0, x1, f(x0), f(x1), x2 (next guess)}`

---

### 1.4 Simple Iteration (Fixed-Point)

**Class**: `SimpleIterationSolver`

**Idea**: Rearrange `f(x) = 0` into the form `x = g(x)`. Then iterate:
```
x_{n+1} = g(x_n)
```

The user provides `g(x)` directly (not `f(x)`).

**Convergence condition**: The method converges if and only if `|g'(x)| < 1` near the root. The solver checks this before iterating:
```python
dg = SymbolicParser.get_derivative(expression)
if abs(dg(x0)) >= 1:
    convergence_check_passed = False  # warning stored in metadata
```

**Convergence speed**: Linear, proportional to `|g'(x)|`. Smaller `|g'|` means faster convergence.

**What each `NumericalStep` stores**: `{x_n, g(x)}`

---

## 2. Network Solver / Linear Systems (`network_solver.py`)

Solves the system `Ax = b` where `A` is an `n×n` matrix and `b` is a length-`n` vector.

---

### 2.1 Diagonal Dominance Pre-processing

Both Jacobi and Gauss-Seidel require (or strongly prefer) a **Strictly Diagonally Dominant** (SDD) matrix:
```
|A[i,i]| > Σ_{j≠i} |A[i,j]|   for every row i
```

Before solving, the engine attempts row-swapping to maximize diagonal dominance:

```
For each column i:
  Find the row j (not yet placed) where |A[j,i]| is largest
  Move that row to position i
```

The result `sdd_reordered` (bool) and `sdd_check` (list of booleans per row) are stored in `SimulationData.metadata` so the GUI can display a warning.

---

### 2.2 Jacobi Method

**Class**: `JacobiSolver`

**Idea**: Solve each equation for its diagonal variable using only values from the *previous* iteration. All updates happen simultaneously after each full sweep.

**Formula** (for row `i`):
```
x_new[i] = (b[i] - Σ_{j≠i} A[i,j] · x_old[j]) / A[i,i]
```

Key: `x_old` is used for **all** `j`, including those already updated this sweep.

After computing all `x_new[i]`, replace `x = x_new` and repeat.

**Convergence**: Measured by `‖x_new - x_old‖_∞` (max absolute change across all variables).

---

### 2.3 Gauss-Seidel Method

**Class**: `GaussSeidelSolver`

**Idea**: Same as Jacobi, but uses the most recently updated values immediately — within the same sweep.

**Formula** (for row `i`):
```
x[i] = (b[i] - Σ_{j<i} A[i,j]·x[j]    ← already updated this sweep
                - Σ_{j>i} A[i,j]·x_old[j]) / A[i,i]
```

In code (`network_solver.py:105`):
```python
sum_j = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x_old[i+1:])
x[i] = (b[i] - sum_j) / A[i, i]
```

**Why Gauss-Seidel is faster**: Information from the newly updated `x[0], x[1], ...` is immediately used when computing `x[i]`, reducing the number of iterations needed compared to Jacobi.

**Convergence**: Same `‖·‖_∞` error metric. Typically converges in half the iterations of Jacobi for well-conditioned systems.

**Divergence detection** (both methods): 5 consecutive iterations where `error > prev_error` → `diverged = True`.

---

## 3. Calculus Engine (`calculus_engine.py`)

---

### 3.1 Numerical Differentiation

**Class**: `NumericalDifferentiationSolver`

Three finite-difference schemes, all approximating `f'(x)`:

| Method | Formula | Error Order |
|---|---|---|
| Forward | `[f(x+h) - f(x)] / h` | O(h) |
| Backward | `[f(x) - f(x-h)] / h` | O(h) |
| Central | `[f(x+h) - f(x-h)] / (2h)` | O(h²) ← default |

Central difference is used internally by Newton-Raphson and Simple Iteration as a fallback when symbolic differentiation fails, with `h = 1e-7`.

---

### 3.2 Trapezoidal Rule

**Class**: `TrapezoidalSolver`

Approximates the integral by fitting a straight line (trapezoid) between each pair of adjacent points.

**Formula**:
```
∫ f(x) dx ≈ (h/2) · [y₀ + 2y₁ + 2y₂ + ... + 2y_{n-1} + yₙ]
```

**Weights**: `1, 2, 2, ..., 2, 1`

**Error**: O(h²) — proportional to the square of the step size.

Accepts either a callable `f` with bounds `a, b, n`, or pre-computed `x_points`/`y_points`.

---

### 3.3 Simpson's 1/3 Rule

**Class**: `SimpsonOneThirdSolver`

Approximates each pair of sub-intervals with a quadratic (parabola). Requires `n` to be **even**.

**Formula**:
```
∫ f(x) dx ≈ (h/3) · [y₀ + 4y₁ + 2y₂ + 4y₃ + 2y₄ + ... + 4y_{n-1} + yₙ]
```

**Weights**: `1, 4, 2, 4, 2, ..., 4, 1`

**Error**: O(h⁴) — much more accurate than Trapezoidal for smooth functions.

---

### 3.4 Simpson's 3/8 Rule

**Class**: `SimpsonThreeEighthsSolver`

Uses groups of 3 sub-intervals fit by a cubic polynomial. Requires `n` to be a **multiple of 3**.

**Formula**:
```
∫ f(x) dx ≈ (3h/8) · [y₀ + 3y₁ + 3y₂ + 2y₃ + 3y₄ + 3y₅ + 2y₆ + ... + yₙ]
```

**Weights**: `1, 3, 3, 2, 3, 3, 2, ..., 1`

**Error**: O(h⁴), same order as Simpson's 1/3 but useful when `n mod 3 = 0`.

---

### 3.5 Gaussian Quadrature

**Class**: `GaussianQuadratureSolver`

Instead of evenly-spaced points, evaluates `f` at optimally chosen nodes that maximize accuracy for a given number of evaluations.

**2-point**:
```
nodes:   t = ±1/√3
weights: w = 1, 1
∫₋₁¹ f(t) dt ≈ f(-1/√3) + f(1/√3)
```

**3-point**:
```
nodes:   t = -√0.6, 0, +√0.6
weights: w = 5/9, 8/9, 5/9
∫₋₁¹ f(t) dt ≈ (5/9)f(-√0.6) + (8/9)f(0) + (5/9)f(+√0.6)
```

**Transformation to [a, b]**:
```
x = (b-a)/2 · t + (b+a)/2
∫ₐᵇ f(x) dx ≈ (b-a)/2 · Σ wᵢ · f(xᵢ)
```

**Accuracy**: A `k`-point rule is exact for polynomials up to degree `2k-1`. Two points handles cubics exactly.

---

### 3.6 Lagrange Interpolation

**Class**: `LagrangeInterpolationSolver`

Builds a polynomial passing exactly through all `n` given data points.

**Formula**:
```
P(x) = Σᵢ yᵢ · Lᵢ(x)

where Lᵢ(x) = Π_{j≠i} (x - xⱼ) / (xᵢ - xⱼ)
```

Each `Lᵢ(x)` is a basis polynomial that equals 1 at `xᵢ` and 0 at all other nodes.

---

### 3.7 Newton's Divided Difference

**Class**: `NewtonDividedDifferenceSolver`

Builds the same interpolating polynomial as Lagrange but using a more computationally stable triangular table.

**Divided difference table**:
```
table[i, 0] = y[i]
table[i, j] = (table[i+1, j-1] - table[i, j-1]) / (x[i+j] - x[i])
```

**Polynomial** (using first row of table as coefficients):
```
P(x) = c₀ + c₁(x-x₀) + c₂(x-x₀)(x-x₁) + c₃(x-x₀)(x-x₁)(x-x₂) + ...
where cᵢ = table[0, i]
```

**Advantage over Lagrange**: Adding a new data point only requires extending the table by one column — no need to recompute from scratch.

---

### 3.8 Newton Forward Difference Table

**Class**: `NewtonDifferenceTableSolver`

Specialized version for **equally-spaced** `x` points. Uses forward differences instead of divided differences.

**Table construction**:
```
Δ⁰yᵢ = yᵢ
Δʲyᵢ = Δʲ⁻¹y_{i+1} - Δʲ⁻¹yᵢ
```

The table is stored in `SimulationData.metadata["difference_table"]` and displayed in the GUI step table with column headers `Δ¹y`, `Δ²y`, etc.

---

### 3.9 Cubic Spline Interpolation

**Class**: `CubicSplineSolver`

Instead of one high-degree polynomial through all points (which can oscillate badly), fits a separate cubic on each interval `[xᵢ, x_{i+1}]`:
```
Sᵢ(x) = aᵢ + bᵢ(x-xᵢ) + cᵢ(x-xᵢ)² + dᵢ(x-xᵢ)³
```

**Natural spline conditions** (forces second derivative = 0 at endpoints) produces a tridiagonal linear system for the `cᵢ` coefficients, solved with the Thomas algorithm.

**Then**:
```
dᵢ = (c_{i+1} - cᵢ) / (3h)
bᵢ = (y_{i+1} - yᵢ)/h - h(c_{i+1} + 2cᵢ)/3
aᵢ = yᵢ
```

**Advantage**: Smooth, no oscillation, `C²` continuity across all knots.
**Minimum**: Requires at least 3 data points.

---

## 4. Shared Data Structures (`models.py`)

```python
@dataclass(frozen=True)
class NumericalStep:
    step_idx: int              # iteration number (0-based)
    value:    float            # primary output (current x approximation or error)
    error:    Optional[float]  # convergence error at this step
    details:  Dict[str, Any]   # solver-specific dict (a, b, f(a), f(b), etc.)

@dataclass(frozen=True)
class SimulationData:
    title:    str              # display name e.g. "Newton-Raphson Convergence"
    x_data:   List[float]      # x-axis values for plotting
    y_data:   List[float]      # y-axis values for plotting
    metadata: Dict[str, Any]   # root, iterations, converged, diverged, etc.
```

Both are **frozen dataclasses** — immutable after creation, safe to pass between layers without accidental mutation.
