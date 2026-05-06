## Goal

Add a 3rd option "Compare Both Methods" in the Linear Systems submenu.
Runs Jacobi and Gauss-Seidel on the same input and shows a side-by-side Rich table.

## Expected Output

```
+-------------------+--------------+--------------+---------+
| Metric            |    Jacobi    | Gauss-Seidel | Winner  |
+-------------------+--------------+--------------+---------+
| Iterations        |      20      |      13      |  G-S    |
| Final Error       |   8.2e-07    |   4.1e-07    |  G-S    |
| Converged         |     Yes      |     Yes      |  Tie    |
| Solution x1       |   1.200000   |   1.200000   |  Same   |
+-------------------+--------------+--------------+---------+
```

## Tasks

- [x] Add option 3 "Compare Both Methods" to `network_solver_menu()` in `terminal.py`
- [x] Add `run_comparison()` method to `NumericalCLI`
- [x] Use same input prompts as `run_gauss_seidel()`
- [x] Run both `JacobiSolver` and `GaussSeidelSolver` on identical inputs
- [x] Build comparison Rich Table with per-row winner highlighting
- [x] Show both step-by-step tables (one per method) if user wants verbose output

## Files to Edit

- `numcore_cli/terminal.py`
