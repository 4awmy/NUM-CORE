## Problem
`PlotManager` exists and is embedded, but only renders mock/static charts.
No real solver step data flows to the plots.

## Tasks

### New PlotManager methods (`numcore_gui/visualization.py`)
- [ ] `plot_convergence_log(steps, title, tol)` — error vs iteration on log-Y scale
      with a dashed horizontal line at the tolerance threshold
- [ ] `plot_comparison(steps_a, steps_b, label_a, label_b)` — two error curves, one plot
- [ ] `plot_solution_bar(variable_labels, values)` — bar chart of solution vector
- [ ] `plot_interpolation(x_pts, y_pts, poly_x, poly_y)` — scatter + polynomial curve
- [ ] `plot_integration(x_pts, y_pts)` — curve + shaded area under it

### Per-page integration
- [ ] Root Finder: plot error vs iteration (log scale) after solve
- [ ] Network Solver (single): plot error vs iteration OR solution bar chart
- [ ] Network Solver (compare mode): overlay Jacobi and G-S error curves on same axes
- [ ] Calculus / Interpolation: scatter + polynomial overlay
- [ ] Calculus / Integration: curve + filled area

## Files to Edit
- `numcore_gui/visualization.py`
- `numcore_gui/pages/root_finder_page.py`
- `numcore_gui/pages/network_solver_page.py`
- `numcore_gui/pages/calculus_page.py`