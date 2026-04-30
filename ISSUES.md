# NUM-CORE — Feature Backlog & GitHub Issues
# ============================================
# Run this with Gemini CLI or `gh` to create all issues at once.
# Each issue is separated and ready to copy-paste into `gh issue create`.

---

## HOW TO CREATE ALL ISSUES AT ONCE (Gemini CLI)

Ask Gemini CLI:
> "Create GitHub issues for all items in ISSUES.md using `gh issue create`"

Or manually:
```bash
gh issue create --title "<title>" --body "<body>" --label "<labels>"
```

---

## ISSUE #1 — [GUI] Complete Redesign & Rebrand

**Title:** `[GUI] Redesign dashboard — remove Mission Control theme, use clean academic layout`
**Labels:** `enhancement`, `gui`, `good-first-issue`

**Body:**
```markdown
## Problem
The current GUI uses a confusing "Mission Control" space theme ("Mission: Beam Stress",
"Analyze Circuit") that is unrelated to the numerical methods content. Pages use
hardcoded mock data. Layout is too cramped.

## Tasks
- [ ] Remove all "Mission" labels — rename to proper method names
- [ ] Sidebar: "Root Finding", "Linear Systems", "Calculus"
- [ ] Default to Dark theme
- [ ] Increase default window to 1280x800
- [ ] Add method selector dropdown per page (e.g., Newton-Raphson vs Simple Iteration)
- [ ] Add tolerance + max iterations input fields to all pages
- [ ] Show a result panel: root value, iterations, converged: yes/no
- [ ] Add a status bar at the bottom of the window
- [ ] Add NUM-CORE logo/branding to sidebar header

## Files to Edit
- `numcore_gui/dashboard.py`
- `numcore_gui/pages/root_finder_page.py`
- `numcore_gui/pages/network_solver_page.py`
- `numcore_gui/pages/calculus_page.py`
```

---

## ISSUE #2 — [GUI] Wire All Pages to Real Solvers

**Title:** `[GUI] Connect GUI pages to real engine solvers — remove all mock/fake data`
**Labels:** `enhancement`, `gui`, `engine`

**Body:**
```markdown
## Problem
All three GUI pages call fake `solve_action()` methods with hardcoded data.
No real solver is invoked when a user clicks "Solve".

## Tasks

### Root Finder Page (`root_finder_page.py`)
- [ ] Parse `func_entry` text and pass to `NewtonRaphsonSolver` or `SimpleIterationSolver`
- [ ] Parse `guess_entry` as float with error handling
- [ ] Display: root, iterations, converged status in result panel
- [ ] Show error message panel on exception

### Network Solver Page (`network_solver_page.py`)
- [ ] Parse matrix textbox with `ast.literal_eval` (safe)
- [ ] Parse b-vector input
- [ ] Call `GaussSeidelSolver` or `JacobiSolver` based on method dropdown
- [ ] Display: solution vector [x1, x2, ...], iterations, converged

### Calculus Page (`calculus_page.py`)
- [ ] Add mode selector: Interpolation vs Integration
- [ ] Interpolation: parse x_points + y_points, call `InterpolationSolver`, show coefficients
- [ ] Integration: parse x/y points + method, call `IntegrationSolver`, show total integral

## Files to Edit
- `numcore_gui/pages/root_finder_page.py`
- `numcore_gui/pages/network_solver_page.py`
- `numcore_gui/pages/calculus_page.py`
```

---

## ISSUE #3 — [GUI] Add Live Convergence Plots with Real Solver Data

**Title:** `[GUI] Add real matplotlib convergence plots to all GUI pages`
**Labels:** `enhancement`, `gui`

**Body:**
```markdown
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
```

---

## ISSUE #4 — [TUI] Jacobi vs Gauss-Seidel Comparison Mode

**Title:** `[TUI] Add option 3 to Linear Systems menu — compare Jacobi vs Gauss-Seidel`
**Labels:** `enhancement`, `tui`

**Body:**
```markdown
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
- [ ] Add option 3 "Compare Both Methods" to `network_solver_menu()` in `terminal.py`
- [ ] Add `run_comparison()` method to `NumericalCLI`
- [ ] Use same input prompts as `run_gauss_seidel()`
- [ ] Run both `JacobiSolver` and `GaussSeidelSolver` on identical inputs
- [ ] Build comparison Rich Table with per-row winner highlighting
- [ ] Show both step-by-step tables (one per method) if user wants verbose output

## Files to Edit
- `numcore_cli/terminal.py`
```

---

## ISSUE #5 — [Engine] Divergence Detection in All Iterative Solvers

**Title:** `[Engine] Detect and warn when iterative methods are diverging`
**Labels:** `enhancement`, `engine`

**Body:**
```markdown
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
```

---

## ISSUE #6 — [main] Startup Mode Selector — TUI vs GUI

**Title:** `[main] Add mode selector at startup — choose Terminal or Graphical interface`
**Labels:** `enhancement`

**Body:**
```markdown
## Goal
When running `python main.py`, show a startup menu so the user can pick between
the TUI and the GUI. Also support `--tui` / `--gui` flags to skip the menu.

## Expected Output
```
+==================================+
|         NUM-CORE v2.0            |
+==================================+
|  1.  Terminal Interface (TUI)    |
|  2.  Graphical Dashboard (GUI)   |
|  3.  Exit                        |
+==================================+
```

## Tasks
- [ ] Use Rich Panel + IntPrompt for the selector menu
- [ ] Choice 1 → `launch_cli()`
- [ ] Choice 2 → `from numcore_gui.dashboard import Dashboard; Dashboard().mainloop()`
- [ ] Choice 3 → `sys.exit(0)`
- [ ] Add argparse: `python main.py --tui` or `python main.py --gui` skips the menu

## Files to Edit
- `main.py`
```

---

## ISSUE #7 — [TUI] Export Iteration Results to CSV

**Title:** `[TUI] Add CSV export option after every solve`
**Labels:** `enhancement`, `tui`, `good-first-issue`

**Body:**
```markdown
## Goal
After any solver finishes, offer the user an option to export the full iteration
table to a CSV file. Uses Python's built-in `csv` module (no new dependencies).

## Expected Flow
```
Export results to CSV? (y/n) [n]: y
Enter filename [results.csv]:
Saved: results_newton_raphson.csv
```

## Tasks
- [ ] Add `export_steps_to_csv(steps, filename, method)` static method to `NumericalFormatter`
- [ ] CSV columns should match the method-specific table (x_n, f(x_n), etc.)
- [ ] Add the export prompt after every `run_*()` method call in `terminal.py`
- [ ] Show success / failure message with file path

## Files to Edit
- `numcore_cli/formatter.py`
- `numcore_cli/terminal.py`
```

---

## GEMINI CLI PROMPT TO CREATE ALL ISSUES

Copy and paste this prompt to Gemini CLI:

```
Read the file ISSUES.md in this repository. For each issue block, create a GitHub issue
using `gh issue create` with:
- The exact title in the "Title:" line
- The labels in the "Labels:" line  
- The content under "Body:" as the issue body

Create all 7 issues one by one.
```
