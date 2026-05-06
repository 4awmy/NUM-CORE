## Problem

If a user gives a bad initial guess or a non-convergent system, the solver silently
runs all max_iterations and returns a wrong answer with no warning.

## Tasks

### Engine changes

- [ ] `NewtonRaphsonSolver`: if error grows for 5 consecutive steps, set
      `metadata["diverged"] = True` and break early
- [ ] `SimpleIterationSolver`: same check
- [ ] `GaussSeidelSolver`: same check
- [ ] `JacobiSolver`: same check

### TUI changes (`terminal.py`)

- [ ] After every `result = solver.solve(...)`, check `result.metadata.get("diverged")`
- [ ] If True, print a Rich warning Panel:
  ```
  WARNING: Method is DIVERGING — error grew for 5 consecutive iterations.
  For root finding: try a closer initial guess.
  For linear systems: check that your matrix is diagonally dominant.
  ```

## Files to Edit

- `numcore_engine/solvers/root_finder.py`
- `numcore_engine/solvers/network_solver.py`
- `numcore_cli/terminal.py`
