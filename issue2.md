## Problem

All three GUI pages call fake `solve_action()` methods with hardcoded data.
No real solver is invoked when a user clicks "Solve".

## Tasks

### Root Finder Page (`root_finder_page.py`)

- [x] Parse `func_entry` text and pass to `NewtonRaphsonSolver` or `SimpleIterationSolver`
- [x] Parse `guess_entry` as float with error handling
- [x] Display: root, iterations, converged status in result panel
- [x] Show error message panel on exception

### Network Solver Page (`network_solver_page.py`)

- [x] Parse matrix textbox with `ast.literal_eval` (safe)
- [x] Parse b-vector input
- [x] Call `GaussSeidelSolver` or `JacobiSolver` based on method dropdown
- [x] Display: solution vector [x1, x2, ...], iterations, converged

### Calculus Page (`calculus_page.py`)

- [x] Add mode selector: Interpolation vs Integration
- [x] Interpolation: parse x_points + y_points, call `InterpolationSolver`, show coefficients
- [x] Integration: parse x/y points + method, call `IntegrationSolver`, show total integral

## Files to Edit

- `numcore_gui/pages/root_finder_page.py`
- `numcore_gui/pages/network_solver_page.py`
- `numcore_gui/pages/calculus_page.py`
