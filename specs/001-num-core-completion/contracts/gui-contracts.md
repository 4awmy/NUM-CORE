# Contract: GUI Page Contracts

**Type**: UI widget contract
**Files**: `numcore_gui/pages/*.py`, `numcore_gui/dashboard.py`, `numcore_gui/visualization.py`

## Dashboard Layout Contract

- Window size: 1280x800 minimum
- Theme: Dark default (CTk `set_appearance_mode("dark")`)
- Sidebar navigation:
  - **Solver Pages**: `Chapter 1 | Chapter 2 | Chapter 3 | Chapter 4`
  - **Scientific Applications**: `Ch 1 Apps | Ch 2 Apps | Ch 3 Apps | Ch 4 Apps`
- Status bar: bottom strip showing last action and solver status
- No mission-themed labels anywhere

## Chapter 1 Page Contract (Bisection Method)

**Inputs**:
| Widget | Type | Placeholder |
|--------|------|-------------|
| Function field | CTkEntry | `e.g. x**2 - 4` |
| Left bound (a) | CTkEntry | `e.g. 0.0` |
| Right bound (b) | CTkEntry | `e.g. 3.0` |
| Tolerance | CTkEntry | `1e-6` |
| Max iterations | CTkEntry | `100` |

**Solve button** → validates f(a)*f(b) < 0 → calls solver → updates Result Panel + Plot

**Result Panel** (below inputs):
```
Root: 2.000000
Iterations: 20
Converged: Yes
f(a)*f(b): Opposite signs ✓
```

**Plot**: Error vs iteration on log-Y scale + tolerance threshold dashed line

## Chapter 2 Page Contract (Linear Systems: Jacobi & Gauss-Seidel)

**Inputs**:
| Widget | Type | Placeholder |
|--------|------|-------------|
| Matrix A | CTkTextbox | `[[2,1],[1,3]]` |
| Vector b | CTkEntry | `[5,7]` |
| Tolerance | CTkEntry | `1e-6` |
| Max iterations | CTkEntry | `100` |
| Method selector | CTkOptionMenu | `Jacobi / Gauss-Seidel / Compare Both` |

**Solve button** → checks diagonal dominance → calls solver → updates Result Panel + Plot

**Result Panel**:
```
Solution: x1=1.2000, x2=1.6000
Iterations: 13
Converged: Yes
Diagonal Dominance: Yes
```

**Plot**: Error decay curve (single) or overlaid Jacobi vs G-S comparison

## Chapter 3 Page Contract (Interpolation: Newton's Divided Difference)

**Inputs**:
| Widget | Type | Placeholder |
|--------|------|-------------|
| x points | CTkEntry | `[0, 1, 2, 3]` |
| y points | CTkEntry | `[0, 1, 4, 9]` |

**Solve button** → validates min 2 points + unique x values → calls solver → updates Result Panel + Plot

**Result Panel**:
```
Polynomial: f(x) = 0.0x³ + 1.0x² + 0.0x + 0.0
Coefficients: [0.0, 1.0, 0.0, 0.0]
Points Used: 4
```

**Plot**: Scatter plot + polynomial curve overlay

## Chapter 4 Page Contract (Integration: Trapezoidal Rule)

**Inputs**:
| Widget | Type | Placeholder |
|--------|------|-------------|
| x points | CTkEntry | `[0, 1, 2, 3]` |
| y points | CTkEntry | `[0, 1, 4, 9]` |
| Method selector | CTkOptionMenu | `Trapezoidal / Simpson's` |

**Solve button** → validates input → calls solver → updates Result Panel + Plot

**Result Panel**:
```
Integral (Trapezoidal): 15.5
Method: Composite Trapezoidal
Intervals: 3
```

**Plot**: Curve with filled area under it (fill_between)

## PlotManager Method Contracts

```python
# All methods: clear current axes, draw, call canvas.draw()

plot_convergence_log(steps: List[NumericalStep], title: str, tol: float)
  # Error vs iteration, log-Y, dashed horizontal tolerance line

plot_comparison(steps_a, steps_b, label_a: str, label_b: str)
  # Two error curves on same axes, different colors

plot_solution_bar(labels: List[str], values: List[float])
  # Bar chart of solution vector [x1, x2, ..., xn]

plot_interpolation(x_pts, y_pts, poly_x, poly_y)
  # Scatter plot + smooth polynomial curve overlay

plot_integration(x_pts, y_pts)
  # Line curve + filled area under it (fill_between)
```

## Scientific Applications Pages Contract

Three new pages (NEW files in `pages/`):

### Root Finder Applications Page (`root_finder_app.py`)
**Layout**:
- Title: "Scientific Applications — Root Finding"
- Real-world problem: "Beam Thickness Optimization" or similar engineering problem
- Problem description + mathematical formula
- Pre-filled solver inputs (function, initial guess, tolerance)
- "Solve Example" button → runs solver, shows result + convergence plot
- "Try It Yourself" expandable section with input fields to modify problem

### Network Solver Applications Page (`network_solver_app.py`)
**Layout**:
- Title: "Scientific Applications — Linear Systems"
- Real-world problem: "Circuit Analysis" or "Pipe Network Flow"
- System of equations visualization (matrix A, vector b)
- Pre-filled values for example system
- "Solve Example" button → shows solution vector + comparison (Jacobi vs G-S if applicable)
- Interactive section to modify matrix/vector and re-solve

### Calculus Applications Page (`calculus_app.py`)
**Layout**:
- Title: "Scientific Applications — Calculus"
- Real-world problem: "Interpolation: Temperature vs Pressure" and "Integration: Work Calculation"
- Two tabs: Interpolation Example | Integration Example
- Pre-filled data points for each
- Plots showing polynomial curve or integral area
- "Try It Yourself" to add/modify data points live
