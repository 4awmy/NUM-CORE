# Quickstart Guide: Enhanced NUM-CORE v2

**Feature**: `002-enhanced-gui-solvers` | **Date**: 2026-05-03

## Prerequisites

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Launch application
python main.py          # Shows startup menu
python main.py --gui    # Launch GUI directly
python main.py --tui    # Launch TUI directly
```

## Solving a Root-Finding Problem (GUI)

1. Launch: `python main.py --gui`
2. Click **Chapter 1 — Root Finding** in the sidebar
3. In the equation field, type: `x^3 - 7*x^2 + 14*x - 6`
   - A formatted preview renders below the field within 300ms
4. Select method: **Bisection** | Secant | Newton-Raphson | Simple Iteration
5. Fill inputs: `a = 0`, `b = 1`, `tol = 1e-6`
6. Click **Solve** → results table appears with lecturer-format columns
7. Click **Compare All Methods** → all 4 methods run simultaneously; best method highlighted

## Solving a Linear System (GUI)

1. Navigate to **Chapter 2 — Linear Systems**
2. Enter matrix A: `[[3,-1,1],[3,6,2],[3,3,7]]`
3. Enter vector b: `[1,0,4]`
4. Select **Gauss-Seidel** or **Compare Both**
5. Click **Solve** → SDD verification shown first, then iteration table

## Interpolating Data (GUI)

1. Navigate to **Chapter 3 — Interpolation**
2. Enter x points: `[1.0, 1.3, 1.6, 1.9, 2.2]`
3. Enter y points (e.g., cos x): `[0.765, 0.620, 0.455, 0.282, 0.110]`
4. Select **Newton Divided Difference**
5. Click **Solve** → divided difference table + polynomial formula shown

## Numerical Integration (GUI)

1. Navigate to **Chapter 4 — Integration**
2. Enter function: `x * ln(x)`
3. Enter: `a = 1`, `b = 2`, `n = 4`
4. Select **Composite Simpson's 1/3**
5. Click **Solve** → step size h, x/y table, weighted-sum formula, and result shown

## Running Tests

```bash
# Unit tests (all solvers)
uv run pytest tests/unit/ -v

# Contract tests (Protocol compliance)
uv run pytest tests/contract/ -v

# All tests with coverage
uv run pytest --cov=numcore_engine --cov-report=term-missing
```

## Equation Input Syntax

| Intent | Type this |
|--------|-----------|
| x² | `x^2` or `x**2` |
| sin(x) | `sin(x)` |
| eˣ | `exp(x)` |
| ln(x) | `ln(x)` |
| √x | `sqrt(x)` |
| π | `pi` |

## CSV Export

After any solve, click **Export CSV** → file saved as `results_<method>_<timestamp>.csv` in the working directory.
