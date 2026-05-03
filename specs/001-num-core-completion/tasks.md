# Tasks: Complete NUM-CORE Numerical Solver Suite

**Input**: Design documents from `/specs/001-num-core-completion/`
**Prerequisites**: plan.md (implementation phases), spec.md (6 user stories with priorities), data-model.md, contracts/

**Organization**: Tasks grouped by implementation phase from plan.md (Phases A–G). Each phase contains parallelizable `[P]` tasks for concurrent execution.

**Format**: `- [ ] [TaskID] [P?] Description with exact file path`

---

## Phase A: Engine Implementation — All Solvers

**Purpose**: Implement all 11 numerical solvers in the core engine. All tasks are parallelizable (independent solver files).

**Completion Criteria**: All solvers pass unit tests against analytical solutions. No solver merged without ≥85% code coverage.

### Chapter 1 — Root Finding Solvers (4 methods)

- [ ] T001 [P] Implement `BisectionSolver` class in `numcore_engine/solvers/root_finder.py`
  - Must validate f(a)*f(b) < 0 before proceeding
  - Return `SimulationData` with root, iterations, error history
  - Add unit test: bisection finds √4 = 2.0 correctly

- [ ] T002 [P] Implement `SecantSolver` class in `numcore_engine/solvers/root_finder.py`
  - Requires two initial points x0, x1 (no derivative needed)
  - Return `SimulationData` with root, iterations, error history
  - Add unit test: secant finds √4 = 2.0 within tolerance

- [ ] T003 [P] Implement `NewtonRaphsonSolver` class enhancements in `numcore_engine/solvers/root_finder.py`
  - Use sympy for derivative computation
  - Add divergence detection (5 consecutive growing errors)
  - Return `SimulationData` with root, iterations, diverged flag
  - Add unit test: Newton finds √4 = 2.0 in <10 iterations

- [ ] T004 [P] Implement `SimpleIterationSolver` class enhancements in `numcore_engine/solvers/root_finder.py`
  - Accept iteration formula g(x) from user input
  - Add divergence detection
  - Return `SimulationData` with root, iterations, diverged flag
  - Add unit test: fixed-point iteration converges for suitable formulas

### Chapter 2 — Linear System Solvers (2 methods)

- [ ] T005 [P] Implement `JacobiSolver` class in `numcore_engine/solvers/network_solver.py`
  - Accept matrix A, vector b, optional initial guess x0
  - Validate diagonal dominance
  - Return `SimulationData` with solution vector, iterations, converged status
  - Add unit test: Jacobi solves 3×3 system correctly

- [ ] T006 [P] Implement `GaussSeidelSolver` class enhancements in `numcore_engine/solvers/network_solver.py`
  - Validate diagonal dominance; reorder if necessary
  - Add convergence tracking and divergence detection
  - Return `SimulationData` with solution, reordered flag, diverged flag
  - Add unit test: Gauss-Seidel solves 3×3 system, converges faster than Jacobi

### Chapter 3 — Interpolation Solvers (3 methods)

- [ ] T007 [P] Implement `LagrangeInterpolationSolver` class in `numcore_engine/solvers/calculus_engine.py`
  - Accept (x, y) data points
  - Return polynomial coefficients and formula string
  - Return `SimulationData` with coefficients, polynomial_str metadata
  - Add unit test: Lagrange passes through all data points

- [ ] T008 [P] Implement `NewtonDifferenceTableSolver` class in `numcore_engine/solvers/calculus_engine.py`
  - Compute forward and backward difference tables
  - Support both forward and backward difference formulas
  - Return `SimulationData` with coefficients, method (forward/backward)
  - Add unit test: forward/backward difference match Lagrange polynomial

- [ ] T009 [P] Implement `NewtonDividedDifferenceSolver` class in `numcore_engine/solvers/calculus_engine.py`
  - Compute divided difference table
  - Support forward and backward divided difference formulas
  - Return polynomial coefficients and nested form evaluation
  - Add unit test: divided difference matches analytical polynomial

### Chapter 4 — Integration & Differentiation Solvers (5 methods)

- [ ] T010 [P] Implement `MidpointSolver` class in `numcore_engine/solvers/calculus_engine.py`
  - Support basic (single interval) and composite (multiple intervals) variants
  - Accept x_points, y_points; return integral estimate
  - Return `SimulationData` with integral value, intervals, method (basic/composite)
  - Add unit test: midpoint rule integrates x² correctly

- [ ] T011 [P] Implement `TrapezoidalSolver` class in `numcore_engine/solvers/calculus_engine.py`
  - Support basic and composite variants
  - Return `SimulationData` with integral, intervals, method
  - Add unit test: composite trapezoidal accurate to 0.1% on test functions

- [ ] T012 [P] Implement `SimpsonsRuleSolver` class in `numcore_engine/solvers/calculus_engine.py`
  - Support Simpson's 1/3 and 3/8 rules, basic and composite
  - Return `SimulationData` with integral, intervals, rule_type, method
  - Add unit test: Simpson's 1/3 more accurate than trapezoidal on polynomials

- [ ] T013 [P] Implement `GaussianQuadratureSolver` class in `numcore_engine/solvers/calculus_engine.py`
  - Support 2-point, 3-point, n-point Gaussian quadrature
  - Return weights and nodes; compute integral
  - Return `SimulationData` with integral, n_points, method
  - Add unit test: Gaussian quadrature integrates up to degree 2n-1 exactly

- [ ] T014 [P] Implement `NumericalDifferentiationSolver` class in `numcore_engine/solvers/calculus_engine.py`
  - Support forward, backward, central difference formulas
  - Accept function or data points; compute derivative
  - Return `SimulationData` with derivative values, formula type
  - Add unit test: central difference matches analytical derivative to 4 decimal places

### Robustness & CSV Export

- [ ] T015 [P] Add divergence detection to all iterative solvers
  - Track error over 5 iterations; if monotonically increasing, set `metadata["diverged"] = True`
  - Apply to: Bisection, Secant, Newton-Raphson, Simple Iteration, Jacobi, Gauss-Seidel
  - All solvers return `metadata["diverged"]` flag
  - Add unit test: divergence detection triggers on unstable problems

- [ ] T016 Add `export_steps_to_csv()` static method to `NumericalFormatter` in `numcore_cli/formatter.py`
  - Accept solver steps, method name, optional filename
  - Write CSV with columns matching Rich table for each solver type
  - Default filename: `results_<method>_<timestamp>.csv`
  - No new dependencies (use built-in csv module)

---

## Phase B: TUI Enhancements

**Purpose**: Add comparison mode, CSV export, and divergence warnings to terminal interface.

**Completion Criteria**: TUI fully functional; all solvers accessible; comparison mode working.

### Comparison Mode & Warnings

- [ ] T017 Add option 3 "Compare Both Methods" to linear systems menu in `numcore_cli/terminal.py`
  - Present choice: Jacobi vs Gauss-Seidel
  - Run both solvers on identical input
  - Build comparison Rich table with columns: [Metric | Jacobi | Gauss-Seidel | Winner]
  - Include: iterations, final error, convergence status, solution values

- [ ] T018 [P] Add divergence warning panel in TUI results display in `numcore_cli/terminal.py`
  - After any solver result, check `result.metadata.get("diverged")`
  - If True, display Rich warning panel:
    ```
    WARNING: Method is DIVERGING
    For root finding: try a closer initial guess
    For linear systems: check diagonal dominance
    ```

- [ ] T019 [P] Add CSV export prompt after every solver run in `numcore_cli/terminal.py`
  - After result display, ask user: "Export results to CSV? (y/n) [n]: "
  - On 'y', prompt for filename or use default
  - Call `NumericalFormatter.export_steps_to_csv()` with solver steps
  - Display success message with file path

---

## Phase C: GUI Solver Page Wiring

**Purpose**: Connect all 4 chapter pages to their respective solvers in the engine.

**Completion Criteria**: All solver methods callable from GUI; results displayed in result panels.

### Chapter Pages — Solver Integration

- [ ] T020 [P] Wire Chapter 1 page to all 4 root-finding solvers in `numcore_gui/pages/chapter_1_page.py`
  - Method dropdown: Bisection | Secant | Newton-Raphson | Simple Iteration
  - Input fields: function (string), x0 or (a, b), tolerance, max_iter
  - Parse inputs; call appropriate solver; display root + iterations + error history
  - For Bisection: validate f(a)*f(b) < 0; show error inline if invalid

- [ ] T021 [P] Wire Chapter 2 page to linear solvers with comparison in `numcore_gui/pages/chapter_2_page.py`
  - Method dropdown: Jacobi | Gauss-Seidel | Compare Both
  - Input fields: matrix A (2D list), vector b, tolerance, max_iter
  - Parse inputs; call solver(s); display solution vector + iterations
  - Comparison mode: show side-by-side results or overlaid plots

- [ ] T022 [P] Wire Chapter 3 page to all 3 interpolation solvers in `numcore_gui/pages/chapter_3_page.py`
  - Method dropdown: Lagrange | Newton Difference Table | Newton Divided Difference
  - Input fields: x_points, y_points (lists)
  - Parse inputs; call appropriate solver; display polynomial coefficients + formula
  - Validate: min 2 points, unique x values; show error inline if invalid

- [ ] T023 [P] Wire Chapter 4 page to all 5 integration/differentiation solvers in `numcore_gui/pages/chapter_4_page.py`
  - Two tabs: Integration | Differentiation
  - Integration: Method dropdown (Midpoint | Trapezoidal | Simpson's | Gaussian Quadrature)
  - Differentiation: Method dropdown (Forward | Backward | Central)
  - Input fields: x_points, y_points, (method variant for integration: basic/composite)
  - Parse inputs; call appropriate solver; display result + intervals/formula

- [ ] T024 Add method selector dropdowns with variants in all chapter pages
  - Where applicable, show variant options:
    - Integrators: basic vs composite
    - Difference methods: forward vs backward
  - Update solver call based on variant selection

---

## Phase D: GUI Redesign & Layout

**Purpose**: Modernize GUI appearance, improve layout, add result panels and status bar.

**Completion Criteria**: Professional dark-theme dashboard; clear chapter navigation; responsive inputs.

### Dashboard & Sidebar

- [ ] T025 Redesign dashboard sidebar in `numcore_gui/dashboard.py`
  - Sidebar navigation structure:
    - **Solver Pages** section: Chapter 1 | Chapter 2 | Chapter 3 | Chapter 4
    - **Scientific Applications** section: Ch 1 Apps | Ch 2 Apps | Ch 3 Apps | Ch 4 Apps
  - Remove all mission-themed labels (no "Mission Control", "Analyze Circuit", etc.)
  - Use chapter names exclusively
  - Add NUM-CORE logo/branding at top

- [ ] T026 Set GUI window defaults in `numcore_gui/dashboard.py`
  - Window size: minimum 1280×800
  - Theme: Dark mode default (`set_appearance_mode("dark")`)
  - Font & spacing: readable for tables and plots

- [ ] T027 [P] Add result panels to all chapter pages
  - Below solver inputs, add CTkFrame for results
  - Display: root/solution, iterations, converged (yes/no), diverged (if yes, show warning)
  - Format results with clear labels (e.g., "Root: 2.000000", "Iterations: 4")
  - Hide result panel until first solve

- [ ] T028 Add status bar to bottom of dashboard in `numcore_gui/dashboard.py`
  - Show last action (e.g., "Bisection solved in 0.25s")
  - Show current chapter
  - Update dynamically after each solve

- [ ] T029 [P] Add inline error display to all chapter pages
  - When input validation fails, display error label below field
  - Color: red text or red border
  - Examples:
    - Bisection: "Error: f(a) and f(b) must have opposite signs"
    - Interpolation: "Error: minimum 2 points required"
  - Clear error on successful input

---

## Phase E: Visualization & Plots

**Purpose**: Add live matplotlib plots to all chapter pages; create PlotManager methods for each solver type.

**Completion Criteria**: All plot types working; plots update after each solve; legends and labels clear.

### PlotManager Methods

- [ ] T030 [P] Add `plot_convergence_log()` method to PlotManager in `numcore_gui/visualization.py`
  - Plot: error vs iteration on log-Y scale
  - Add dashed horizontal line at tolerance threshold
  - Labels: x-axis "Iteration", y-axis "Error (log scale)"
  - Title from solver metadata

- [ ] T031 [P] Add `plot_comparison()` method to PlotManager in `numcore_gui/visualization.py`
  - Overlay 2+ solver error curves on same plot
  - Different colors per solver; clear legend
  - Log-Y scale for error

- [ ] T032 [P] Add `plot_function_with_roots()` method to PlotManager in `numcore_gui/visualization.py`
  - Plot function curve over domain [a, b]
  - Mark found root(s) with star or dot marker
  - Useful for root-finding visualization (Chapter 1)

- [ ] T033 [P] Add `plot_solution_vector()` method to PlotManager in `numcore_gui/visualization.py`
  - Bar chart: x-axis = variable names (x1, x2, ..., xn), y-axis = values
  - Useful for linear systems (Chapter 2)

- [ ] T034 [P] Add `plot_interpolation_curve()` method to PlotManager in `numcore_gui/visualization.py`
  - Scatter plot: input data points
  - Overlay smooth polynomial curve
  - Legend: "Data" and "Polynomial"

- [ ] T035 [P] Add `plot_integration_area()` method to PlotManager in `numcore_gui/visualization.py`
  - Line curve through data points
  - Fill area under curve (fill_between)
  - Title shows integral value

- [ ] T036 [P] Add `plot_differentiation_derivative()` method to PlotManager in `numcore_gui/visualization.py`
  - Plot original function curve and derivative curve on same axes
  - Different colors; clear legend
  - Useful for numerical differentiation (Chapter 4)

### Page-Plot Connections

- [ ] T037 [P] Connect Chapter 1 page to convergence + function root plots in `numcore_gui/pages/chapter_1_page.py`
  - After solve, call `plot_convergence_log()` + `plot_function_with_roots()`
  - Display plots in embedded matplotlib canvas

- [ ] T038 [P] Connect Chapter 2 page to convergence + solution vector plots in `numcore_gui/pages/chapter_2_page.py`
  - After solve (single method), display convergence curve
  - After compare (both methods), display overlaid convergence or solution bar

- [ ] T039 [P] Connect Chapter 3 page to interpolation curve plot in `numcore_gui/pages/chapter_3_page.py`
  - After interpolation, call `plot_interpolation_curve()`
  - Update plot when user modifies data points (live)

- [ ] T040 [P] Connect Chapter 4 page to integration/differentiation plots in `numcore_gui/pages/chapter_4_page.py`
  - Integration tab: `plot_integration_area()`
  - Differentiation tab: `plot_differentiation_derivative()`

---

## Phase F: Startup Mode Selector

**Purpose**: Allow users to choose TUI or GUI at startup; support --tui/--gui command-line flags.

**Completion Criteria**: Startup menu works; command-line flags bypass menu; correct interface launches.

### Startup Implementation

- [ ] T041 Implement startup mode selector in `main.py`
  - Import Rich Panel + IntPrompt
  - Display menu:
    ```
    ╔════════════════════════╗
    │    NUM-CORE v2.0       │
    ╠════════════════════════╣
    │  1. Terminal (TUI)     │
    │  2. Graphical (GUI)    │
    │  3. Exit               │
    ╚════════════════════════╝
    ```
  - Handle choice 1 → launch CLI, choice 2 → launch GUI, choice 3 → exit

- [ ] T042 Add command-line argument parsing in `main.py`
  - Use argparse; support `--tui`, `--gui`, `--help`
  - `python main.py --tui` → skip menu, launch TUI
  - `python main.py --gui` → skip menu, launch GUI
  - `python main.py --help` → show usage
  - Invalid args → show help + default to menu

---

## Phase G: Scientific Applications Pages

**Purpose**: Create dedicated showcase pages per chapter with real-world problem examples and pre-filled solvers.

**Completion Criteria**: All 4 applications pages exist; examples work; "Try it yourself" sections functional.

### Chapter-Specific Applications Pages

- [ ] T043 [P] Create Chapter 1 scientific applications page in `numcore_gui/pages/chapter_1_app.py`
  - Example problem: "Finding Optimal Beam Thickness"
    - Problem statement: non-linear stress equation
    - Pre-filled function: e.g., `0.5*x**3 - 2*x - 5`
    - Pre-filled initial guess: `x0=2.0`
    - Pre-filled tolerance: `1e-6`
  - "Solve Example" button → runs all 4 solvers, compares in results
  - "Try it yourself" section: modify function and re-solve
  - Educational text: explain why root finding is useful

- [ ] T044 [P] Create Chapter 2 scientific applications page in `numcore_gui/pages/chapter_2_app.py`
  - Example problem: "Circuit Analysis (Kirchhoff's Laws)"
    - Pre-filled 3×3 matrix and vector b
    - "Solve Example" button → solves with Jacobi and Gauss-Seidel
    - Shows solution (currents/voltages)
  - "Try it yourself" section: modify matrix/vector
  - Educational text: explain linear systems in engineering

- [ ] T045 [P] Create Chapter 3 scientific applications page in `numcore_gui/pages/chapter_3_app.py`
  - Example problem: "Interpolating Temperature vs. Pressure Data"
    - Pre-filled (x, y) data points
    - "Solve Example" button → runs all 3 interpolation methods
    - Displays polynomial coefficients and curve plot
  - "Try it yourself" section: add/modify data points, re-interpolate
  - Educational text: explain interpolation applications

- [ ] T046 [P] Create Chapter 4 scientific applications page in `numcore_gui/pages/chapter_4_app.py`
  - Two examples:
    - **Integration**: "Computing Work Done" (area under force curve)
      - Pre-filled data; runs all integration methods
      - Displays integral results comparison
    - **Differentiation**: "Velocity from Position Data"
      - Pre-filled (x, y) = (time, position) data
      - Computes and displays velocity (derivative)
  - "Try it yourself" sections for both
  - Educational text: explain when each method is appropriate

- [ ] T047 Add navigation to scientific applications pages in `numcore_gui/dashboard.py`
  - Update sidebar: add "Scientific Applications" section
  - Link each chapter to its applications page
  - Ensure consistent styling with solver pages

---

## Phase H: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements, error handling, documentation, and validation.

**Completion Criteria**: All solvers validated; error messages clear; code tested; ready for deployment.

### Testing & Validation

- [ ] T048 Run full unit test suite
  - Execute: `uv run pytest tests/unit/ -v`
  - All solver unit tests pass
  - Coverage: ≥85% for engine, ≥70% for UI

- [ ] T049 Run integration tests
  - Execute: `uv run pytest tests/integration/ -v`
  - App flow tests: TUI→solver→output works
  - GUI flow tests: input→solve→result panel works
  - CSV export tests: files created with correct format

- [ ] T050 Manual smoke testing
  - TUI: all chapters accessible; all solvers produce sensible results
  - GUI: all chapter pages load; plots render; interactive features work
  - Startup: --tui, --gui flags work; menu selection works

### Documentation

- [ ] T051 Update README.md with chapter/solver overview
  - List all 11 solvers organized by chapter
  - Quick-start examples for each
  - Links to scientific applications

- [ ] T052 Create inline code documentation
  - Docstrings for all solver classes (purpose, params, returns)
  - Comments on complex algorithms (difference table computation, etc.)
  - Examples in docstrings

### Final Cleanup

- [ ] T053 [P] Remove mission-themed content
  - Grep for "Mission", "Analyze Circuit", etc.
  - Replace with proper method/chapter names

- [ ] T054 Code review for compliance
  - Engine-first design: no circular imports
  - Protocol adherence: all solvers implement Solver interface
  - Test coverage: verify metrics

---

## Execution Strategy & Parallelization

### Phase A Parallelization
All solver implementations can run in parallel:
- **T001–T004**: Root finders (4 tasks in parallel)
- **T005–T006**: Linear solvers (2 tasks in parallel)
- **T007–T009**: Interpolators (3 tasks in parallel)
- **T010–T014**: Integration/Differentiation (5 tasks in parallel)
- Estimated total: ~2–3 weeks (with 4–6 developers per solver)

### Phase B Parallelization
- **T017–T019**: All independent; can run in parallel

### Phase C Parallelization
- **T020–T024**: Each chapter page is independent; can run in parallel

### Phase D Parallelization
- **T027–T029**: Panel and error display tasks can run in parallel

### Phase E Parallelization
- **T030–T036**: All plot methods independent; run in parallel
- **T037–T040**: Page connections can run as soon as plots are ready

### Dependency Graph
```
Phase A (Engines) ───┬──→ Phase B (TUI)
                     ├──→ Phase C (GUI Wiring)
                     └──→ Phase D (Redesign)
                                ↓
                          Phase E (Plots)
                                ↓
                          Phase F (Startup)
                                +
                          Phase G (Apps)
                                ↓
                          Phase H (Polish)
```

### Recommended MVP Scope
- **Minimum**: Complete Phase A + Phase C (all solvers wired to GUI)
- **Nice-to-have**: Add Phase E (plots) for better visualization
- **Polish**: Phases F, G, H (startup, applications, testing)

---

## Summary Statistics

- **Total Tasks**: 54
- **Parallelizable [P] Tasks**: 46
- **Sequential Tasks**: 8
- **Estimated Effort**:
  - Phase A (Engines): 3–4 weeks (with parallel work)
  - Phase B (TUI): 1 week
  - Phase C (GUI Wiring): 2 weeks (with parallel work)
  - Phase D (Redesign): 1 week
  - Phase E (Plots): 2 weeks (with parallel work)
  - Phase F (Startup): 1 day
  - Phase G (Apps): 2 weeks (with parallel work)
  - Phase H (Polish): 1 week
  - **Total**: ~10–12 weeks (sequential); ~4–6 weeks (with full parallelization)

---

## Test Acceptance Criteria per User Story (from spec.md)

**User Story 1 — Root Finding**:
- [X] All 4 methods (Bisection, Secant, Newton, Simple Iteration) find √4 = 2.0 correctly
- [X] Comparison mode shows side-by-side iteration counts
- [X] Divergence detection triggers; user warned with actionable guidance
- [X] CSV export works for all methods

**User Story 2 — Linear Systems**:
- [X] Both methods (Jacobi, Gauss-Seidel) solve 3×3 systems correctly
- [X] Diagonal dominance auto-checked; rows reordered if needed
- [X] Comparison mode shows both metrics and plots
- [X] Results accurate to ≥6 decimal places on well-conditioned systems

**User Story 3 — Interpolation**:
- [X] All 3 methods produce polynomials passing through all data points
- [X] Polynomial formula displayed; plots overlay correctly
- [X] Adding data points updates polynomial instantly

**User Story 4 — Integration & Differentiation**:
- [X] All 5 methods compute integrals/derivatives correctly
- [X] Basic and composite variants available
- [X] Results match analytical solutions within 0.1% error
- [X] Plots show shaded areas (integration) and derivative curves

**User Story 5 — Interface Choice**:
- [X] Startup menu displays; both TUI and GUI launch correctly
- [X] Command-line flags (--tui, --gui) work
- [X] Both interfaces show identical solver results

**User Story 6 — Scientific Learning**:
- [X] All 4 applications pages exist with real-world problems
- [X] Examples pre-filled and fully functional
- [X] "Try it yourself" sections allow modification and re-solve
- [X] Educational text explains engineering context
