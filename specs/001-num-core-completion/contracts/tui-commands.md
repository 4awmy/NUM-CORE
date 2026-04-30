# Contract: TUI Command Schema

**Type**: CLI interaction schema
**File**: `numcore_cli/terminal.py`

## Main Menu

```
NUM-CORE v2.0
1. Root Finding
2. Linear Systems
3. Calculus
4. Exit
```

## Root Finding Submenu

```
1. Newton-Raphson
2. Simple Iteration
3. Compare Both Methods
4. Back
```

**Inputs** (all methods):
- Function expression (Python syntax, e.g. `x**2 - 4`)
- Initial guess x₀ (float)
- Tolerance (default: 1e-6)
- Max iterations (default: 100)

**Output**: Rich table with columns `[Iter, x_n, f(x_n), error]`
**After solve**: Divergence warning panel if `diverged=True`; CSV export prompt

## Linear Systems Submenu

```
1. Gauss-Seidel
2. Jacobi
3. Compare Both Methods
4. Back
```

**Inputs**:
- Matrix A (Python list syntax, e.g. `[[2,1],[1,3]]`)
- Vector b (Python list syntax, e.g. `[5, 7]`)
- Tolerance (default: 1e-6)
- Max iterations (default: 100)

**Output**: Rich table with columns `[Iter, x1, x2, ..., xn, error]`
**Comparison output**: Side-by-side Rich table with columns `[Metric, Jacobi, Gauss-Seidel, Winner]`

## Calculus Submenu

```
1. Interpolation (Newton's Divided Difference)
2. Integration (Trapezoidal / Simpson's)
3. Back
```

**Inputs**:
- x_points and y_points (Python list syntax)
- Integration method (trapezoidal or simpsons)

**Output**: Polynomial coefficients table; integral result panel

## CSV Export Contract

```
Export results to CSV? (y/n) [n]: y
Enter filename [results_<method>_<timestamp>.csv]:
✓ Saved: results_newton_raphson_20260429_231500.csv
```

- Columns match displayed Rich table for each method
- Default filename uses method name + timestamp
- Uses UTF-8, comma-separated, with header row
