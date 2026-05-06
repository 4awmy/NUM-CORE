# Tasks: Enhanced GUI, Auto-Solver Comparison, and Course-Complete Solver Suite

**Input**: Design documents from `/specs/002-enhanced-gui-solvers/`
**Prerequisites**: plan.md, spec.md (7 user stories), data-model.md, contracts/, research.md

**Organization**: Tasks grouped by user story in priority order (P1 → P3). Tasks carry a `[DevA]` or `[DevB]` label showing the recommended 2-person assignment. All `[P]` tasks within the same phase can run in parallel by either developer.

**2-Person Split**:
- **Dev A — Numerical Engine**: Solvers, Smart Solver logic, Lecturer format tables, TUI, engine tests
- **Dev B — GUI & UX**: Equation input widget, black theme, plots, GUI wiring, dashboard

---

## Phase 1: Setup & Project Skeleton

**Purpose**: Create all new files/directories so both developers can work without merge conflicts.

- [ ] T001 Verify dependencies installed (`sympy`, `numpy`, `matplotlib`, `customtkinter`, `rich`, `pytest`) via `uv sync`
- [ ] T002 [P] Create `numcore_engine/comparison.py` with empty `ComparisonRunner` stub
- [ ] T003 [P] Create `numcore_gui/equation_input.py` with empty `EquationInputWidget` stub
- [ ] T004 [P] Create `numcore_gui/theme.py` with empty color constant placeholders
- [ ] T005 [P] Create `numcore_gui/smart_solver_panel.py` with empty widget stub
- [ ] T006 [P] Create `numcore_gui/styles/` directory and empty `numcore_black.mplstyle` file
- [ ] T007 [P] Create `numcore_engine/solvers/ode_solver.py` with empty class stubs
- [ ] T008 [P] Create `tests/contract/` directory and empty `test_solver_protocol.py`

**Checkpoint**: Both developers can now open non-conflicting files immediately.

---

## Phase 2: Foundational (Blocking — Both Must Wait)

**Purpose**: Shared data models and parser extensions that every solver and widget depends on.

**⚠️ CRITICAL**: Phases 3–10 cannot begin until this phase is complete.

- [ ] T009 Extend `numcore_engine/models.py`: add `ComparisonResult` dataclass; add new metadata keys to `SimulationData` (`diverged`, `convergence_check_value`, `convergence_check_passed`, `x0_check_passed`, `sdd_check`, `sdd_reordered`, `update_type`, `dd_table`, `polynomial_str`, `h`, `xy_table`, `weighted_sum_str`, `n_even_check`, `n_mod3_check`, `computation_time_ms`)
- [ ] T010 Extend `numcore_engine/parser.py`: normalize `^` → `**`, accept `ln()` → `log()`, validate expression on parse, return structured error message on failure

**Checkpoint**: Foundation ready — Dev A and Dev B streams can now run fully in parallel.

---

## Phase 3: US6 — Course-Complete Solver Suite, Weeks 1–10 [DevA] (Priority: P2)

**Goal**: All 15 course methods implemented in the engine with correct lecturer methodology data in metadata.

**Independent Test**: `uv run pytest tests/unit/ -v` — all 15 solvers produce correct answers within 0.1% of analytical solution on standard test problems.

**Dev A owns this entire phase. Dev B works on Phases 4–5 simultaneously.**

### Chapter 1 — Root Finding (all 4 parallelizable)

- [ ] T011 [P] [DevA] [US6] Implement `BisectionSolver` in `numcore_engine/solvers/root_finder.py` — validate f(a)·f(b)<0; step data keys: {n,a,b,c,f_a,f_b,f_c,error}; error=|b-a|/2 per step; metadata: diverged flag
- [ ] T012 [P] [DevA] [US6] Implement `SecantSolver` in `numcore_engine/solvers/root_finder.py` — two initial points x₀,x₁; no derivative required; return root + iteration steps
- [ ] T013 [P] [DevA] [US6] Enhance `NewtonRaphsonSolver` in `numcore_engine/solvers/root_finder.py` — sympy auto-derivative; compute f(x₀)·f″(x₀)>0 check; step data: {x_n, f_xn, f_prime_xn}; metadata: x0_check_passed, diverged
- [ ] T014 [P] [DevA] [US6] Enhance `SimpleIterationSolver` in `numcore_engine/solvers/root_finder.py` — accept g(x) string; compute |g′(x₀)| with sympy; metadata: convergence_check_value, convergence_check_passed, diverged

### Chapter 2 — Linear Systems (both parallelizable)

- [ ] T015 [P] [DevA] [US6] Enhance `JacobiSolver` in `numcore_engine/solvers/network_solver.py` — run SDD check per row (|a_ii| > Σ|a_ij|); reorder if needed; label update_type="simultaneous"; metadata: sdd_check list, sdd_reordered, diverged
- [ ] T016 [P] [DevA] [US6] Enhance `GaussSeidelSolver` in `numcore_engine/solvers/network_solver.py` — same SDD check; label update_type="successive"; metadata: sdd_check, sdd_reordered, diverged

### Chapter 3 — Interpolation (all 5 parallelizable)

- [ ] T017 [P] [DevA] [US6] Implement `LagrangeInterpolationSolver` in `numcore_engine/solvers/calculus_engine.py` — compute L_i(x) basis polynomials individually; metadata: polynomial_str
- [ ] T018 [P] [DevA] [US6] Implement `NewtonForwardDifferenceSolver` in `numcore_engine/solvers/calculus_engine.py` — forward difference table; metadata: polynomial_str
- [ ] T019 [P] [DevA] [US6] Implement `NewtonBackwardDifferenceSolver` in `numcore_engine/solvers/calculus_engine.py` — backward difference table; metadata: polynomial_str
- [ ] T020 [P] [DevA] [US6] Implement `NewtonForwardDividedDifferenceSolver` in `numcore_engine/solvers/calculus_engine.py` — triangular divided difference table; metadata: dd_table (2D list), polynomial_str
- [ ] T021 [P] [DevA] [US6] Implement `NewtonBackwardDividedDifferenceSolver` in `numcore_engine/solvers/calculus_engine.py` — backward divided difference; metadata: dd_table, polynomial_str

### Chapter 4 — Integration (all 4 parallelizable)

- [ ] T022 [P] [DevA] [US6] Implement `CompositeTrapezoidalSolver` in `numcore_engine/solvers/calculus_engine.py` — h=(b-a)/n; metadata: h, xy_table, weighted_sum_str using formula h/2[y₀+2(y₁+…+yₙ₋₁)+yₙ]
- [ ] T023 [P] [DevA] [US6] Implement `CompositeMidpointSolver` in `numcore_engine/solvers/calculus_engine.py` — metadata: h, xy_table, weighted_sum_str
- [ ] T024 [P] [DevA] [US6] Implement `CompositeSimpsonsOneThirdSolver` in `numcore_engine/solvers/calculus_engine.py` — validate n even (metadata: n_even_check); inline error if odd; metadata: h, xy_table, weighted_sum_str
- [ ] T025 [P] [DevA] [US6] Implement `CompositeSimpsonsThreeEighthsSolver` in `numcore_engine/solvers/calculus_engine.py` — validate n%3==0 (metadata: n_mod3_check); inline error if not; metadata: h, xy_table, weighted_sum_str

### Robustness

- [ ] T026 [DevA] [US6] Add divergence detection to all 6 iterative solvers (T011–T016): track error over 5 iterations; if monotonically increasing set `metadata["diverged"] = True`; solver continues to max_iter regardless
- [ ] T027 [P] [DevA] [US6] Write unit tests for all 15 solvers in `tests/unit/test_root_finder.py`, `tests/unit/test_network_solver.py`, `tests/unit/test_calculus_engine.py` — assert correct solution, column keys, formula values (SC-003 automated assertions)

**Checkpoint [DevA]**: All 15 engine solvers pass unit tests. Dev A can now proceed to Phase 6.

---

## Phase 4: US1 — Equation Input Widget [DevB] (Priority: P1)

**Goal**: Visual equation input field with live MathText preview, symbol toolbar, and inline error display.

**Independent Test**: Type `x^3 - 7*x^2 + 14*x - 6` → preview renders formatted math within 300ms → click symbol button inserts text at cursor → type `x^^2` → error label appears with hint.

**Dev B owns this phase. Dev A works on Phase 3 simultaneously.**

- [ ] T028 [DevB] [US1] Implement `EquationInputWidget` base CTk frame in `numcore_gui/equation_input.py` with `get_expression()`, `get_raw()`, `set_expression()`, `is_valid()`, `show_error()`, `clear_error()` methods
- [ ] T029 [DevB] [US1] Add text entry field with `<KeyRelease>` binding and `after(300)` debounce callback in `numcore_gui/equation_input.py`
- [ ] T030 [P] [DevB] [US1] Add embedded matplotlib MathText preview canvas (FigureCanvasTkAgg, 4×0.6 inch, black background) in `numcore_gui/equation_input.py` — renders `$f(x) = <expr>$`; shows red "⚠ Invalid expression" on parse failure
- [ ] T031 [P] [DevB] [US1] Add function symbol toolbar row (buttons: sin, cos, tan, ln, exp, sqrt, π, e) that insert text snippets at cursor position in `numcore_gui/equation_input.py`
- [ ] T032 [DevB] [US1] Wire expression normalization: call `parser.normalize()` on raw text to convert `^`→`**`, `ln`→`log`; display normalized form in preview in `numcore_gui/equation_input.py`
- [ ] T033 [DevB] [US1] Integration test: valid expressions parse correctly, invalid show errors, symbol buttons insert text in `tests/integration/test_equation_input.py`

**Checkpoint [DevB]**: `EquationInputWidget` works standalone — can be dropped into any chapter page.

---

## Phase 5: US3 — True Black Theme [DevB] (Priority: P1)

**Goal**: Pure #000000 backgrounds across all GUI surfaces and all matplotlib plots.

**Independent Test**: Launch app — measure any frame/window background = #000000. Render any plot — measure figure.facecolor = #000000. All text contrast ≥ 4.5:1.

**Dev B runs this in parallel with Phase 4 (different files, no conflict).**

- [ ] T034 [P] [DevB] [US3] Write `numcore_gui/styles/numcore_black.mplstyle` — set figure.facecolor:#000000, axes.facecolor:#000000, axes.edgecolor:#444444, text.color:#ffffff, xtick.color:#aaaaaa, ytick.color:#aaaaaa, grid.color:#222222, lines.color:#4fc3f7
- [ ] T035 [P] [DevB] [US3] Define color palette in `numcore_gui/theme.py`: BLACK=#000000, ACCENT_BLUE=#4fc3f7, ACCENT_ORANGE=#ff9800, TEXT_PRIMARY=#ffffff, TEXT_SECONDARY=#aaaaaa, SUCCESS=#4caf50, ERROR=#f44336, WARN=#ff9800, PANEL=#111111, BORDER=#333333
- [ ] T036 [DevB] [US3] Apply black theme to `numcore_gui/dashboard.py` — set all CTk window/frame `fg_color` to BLACK; sidebar to PANEL; remove any gray backgrounds
- [ ] T037 [P] [DevB] [US3] Apply theme palette to all chapter pages (`chapter_1_page.py` through `chapter_4_page.py`) — frame backgrounds, button colors, label foregrounds
- [ ] T038 [DevB] [US3] Register `numcore_black.mplstyle` at app startup in `main.py` via `matplotlib.style.use()` before any GUI import

**Checkpoint [DevB]**: Black theme applied globally — any plot or page opened is pure black.

---

## Phase 6: US5 — Lecturer Methodology Tables [DevA] (Priority: P1)

**Goal**: Formatter functions producing exact column structures per lecturer's methodology for all methods.

**Independent Test**: Call each format function with a sample `SimulationData` object — assert column names, formula values, and string fields match expected output exactly (SC-003 automated assertions).

**Dev A runs after Phase 3 checkpoint. Dev B continues Phase 7.**

- [ ] T039 [P] [DevA] [US5] Implement `format_bisection_table()` in `numcore_cli/formatter.py` — columns [n, a, b, c, f(a), f(b), f(c), Error] where Error=|b-a|/2; assert in test that error column = |b-a|/2 exactly
- [ ] T040 [P] [DevA] [US5] Implement `format_simple_iteration_table()` in `numcore_cli/formatter.py` — render convergence check header showing |g′(x₀)| value with PASS/FAIL label; iteration table follows
- [ ] T041 [P] [DevA] [US5] Implement `format_newton_raphson_table()` in `numcore_cli/formatter.py` — render f(x₀)·f″(x₀)>0 check line; iteration columns: [n, x_n, f(x_n), f'(x_n), error]
- [ ] T042 [P] [DevA] [US5] Implement `format_sdd_verification()` in `numcore_cli/formatter.py` — render per-row table: [row, |a_ii|, Σ|a_ij|, dominant?] with overall PASS/FAIL
- [ ] T043 [P] [DevA] [US5] Implement `format_divided_difference_table()` in `numcore_cli/formatter.py` — triangular layout: x_i | y_i | 1st DD | 2nd DD | 3rd DD … (columns expand with data size)
- [ ] T044 [P] [DevA] [US5] Implement `format_integration_table()` in `numcore_cli/formatter.py` — output: h statement, x/y value table, weighted-sum formula string (expanded), final integral value
- [ ] T045 [P] [DevA] [US5] Implement `format_comparison_table()` in `numcore_cli/formatter.py` — columns: [Method, Solution, Iterations, Final Error, Status, Time(ms)]; highlight best row; flag diverged rows
- [ ] T046 [DevA] [US5] Write unit tests for all 7 format functions in `tests/unit/test_formatter.py` — assert exact column names, formula correctness, edge cases (diverged, SDD fail, n-odd Simpson's)

**Checkpoint [DevA]**: All format functions tested. Dev A proceeds to Phase 8 (Smart Solver engine).

---

## Phase 7: US4 — Enhanced Plotter [DevB] (Priority: P1)

**Goal**: All plot types rendered on black background with zoom/pan and method-specific visual details.

**Independent Test**: Instantiate each plot method with sample `SimulationData`, call render — assert figure facecolor=#000000, toolbar present, correct plot type drawn.

**Dev B runs this after Phases 4–5. Dev A runs Phase 6 simultaneously.**

- [ ] T047 [P] [DevB] [US4] Add `NavigationToolbar2Tk` to `PlotManager` in `numcore_gui/visualization.py` — embed zoom/pan toolbar in all plot frames; style toolbar background to BLACK
- [ ] T048 [P] [DevB] [US4] Implement `plot_bisection_brackets()` in `numcore_gui/visualization.py` — function curve over [a,b]; overlay vertical bracket markers narrowing per iteration; mark final root; black background
- [ ] T049 [P] [DevB] [US4] Implement `plot_newton_tangents()` in `numcore_gui/visualization.py` — function curve; draw tangent line at each Newton step; mark root; black background
- [ ] T050 [P] [DevB] [US4] Implement `plot_convergence_log()` in `numcore_gui/visualization.py` — error vs iteration, log-Y scale; dashed horizontal tolerance threshold line; title from solver name
- [ ] T051 [P] [DevB] [US4] Implement `plot_comparison_overlay()` in `numcore_gui/visualization.py` — overlay error curves for all methods; distinct colors from ACCENT palette; clear legend per method
- [ ] T052 [P] [DevB] [US4] Implement `plot_interpolation_curve()` in `numcore_gui/visualization.py` — scatter data points; smooth polynomial overlay; legend: "Data" / "Polynomial"
- [ ] T053 [P] [DevB] [US4] Implement `plot_integration_area()` in `numcore_gui/visualization.py` — line curve through data; fill_between for area; annotate integral value on plot
- [ ] T054 [P] [DevB] [US4] Implement `plot_solution_vector()` in `numcore_gui/visualization.py` — bar chart: variable names x₁…xₙ vs values; useful for linear system solution display
- [ ] T055 [DevB] [US4] Connect all plot methods to chapter pages: Chapter 1 → bisection_brackets + newton_tangents + convergence_log; Chapter 2 → solution_vector + convergence_log; Chapter 3 → interpolation_curve; Chapter 4 → integration_area

**Checkpoint [DevB]**: All plots render correctly on black canvas with zoom/pan.

---

## Phase 8: US2 — Smart Solver Mode [Both] (Priority: P1)

**Goal**: One-click Smart Solve runs all methods, recommends the winner with explanation, shows diagnostic on all-diverge.

**Independent Test**: Enter `f(x)=x³−2x²−5`, interval [2,3], click Smart Solve → comparison table appears with ≥2 methods, recommendation panel shows method name + reason string, best-method row is highlighted.

**Dev A (engine) and Dev B (GUI) work this phase in parallel.**

### Dev A — Smart Solver Engine

- [ ] T056 [DevA] [US2] Implement `ComparisonRunner.run()` in `numcore_engine/comparison.py` — accepts list of Solver instances + problem dict; runs each; records `computation_time_ms`; returns `ComparisonResult`
- [ ] T057 [P] [DevA] [US2] Implement `chapter_1_compare()`, `chapter_2_compare()`, `chapter_3_compare()`, `chapter_4_compare()` wrapper functions in `numcore_engine/comparison.py` — handle method-specific input routing (a/b for Bisection, x₀ for Newton, etc.)
- [ ] T058 [DevA] [US2] Implement g(x) auto-derivation in `numcore_engine/comparison.py` — attempt `g(x) = x - f(x)/f'(x_0)` or `g(x) = (rearranged form)` via sympy; test |g'(x₀)|<1; return None if no convergent form found
- [ ] T059 [DevA] [US2] Implement `best_method_selector()` in `numcore_engine/comparison.py` — select method with fewest iterations among converged; return None if all diverged
- [ ] T060 [P] [DevA] [US2] Implement `RecommendationEngine` in `numcore_engine/comparison.py` — map (method_name, problem_type) → explanation string (e.g., "Fastest convergence for smooth differentiable functions"); covers all 15 methods
- [ ] T061 [P] [DevA] [US2] Implement `DiagnosticEngine` in `numcore_engine/comparison.py` — map (method_name, divergence_reason) → cause string + fix hint (e.g., "Bisection: f(a)·f(b) > 0 — try wider interval")
- [ ] T062 [DevA] [US2] Unit tests for ComparisonRunner in `tests/unit/test_comparison_runner.py` — assert correct winner selection, recommendation not empty, diagnostic appears when all diverge, Simple Iteration excluded when g(x) undeserved

### Dev B — Smart Solver UI (parallel)

- [ ] T063 [P] [DevB] [US2] Implement `SmartSolverPanel` CTk frame in `numcore_gui/smart_solver_panel.py` — recommendation card (method name, iteration count, error, reason text) + comparison table widget
- [ ] T064 [P] [DevB] [US2] Implement comparison table UI: scrollable rows, best-method row highlighted with ACCENT_BLUE border, Diverged rows in ERROR red, clickable rows expand inline detail
- [ ] T065 [DevB] [US2] Implement inline detail expansion: clicking a method row shows its full lecturer-format result table (calls appropriate format_*() function from formatter.py)
- [ ] T066 [DevB] [US2] Implement diagnostic panel variant of SmartSolverPanel for all-diverge case: list per-method cause + fix hint in WARN yellow
- [ ] T067 [DevB] [US2] Add "Smart Solve" button to all 4 chapter pages; wire to `chapter_N_compare()` → `SmartSolverPanel.populate(comparison_result)` in `numcore_gui/pages/chapter_*_page.py`

**Checkpoint**: Smart Solve works end-to-end on at least Chapter 1 (root finding).

---

## Phase 9: US6 — GUI Wiring & Dashboard [DevB] (Priority: P2)

**Goal**: All 4 chapter pages fully wired to solvers, EquationInputWidget, plots, result panels, and Smart Solve.

**Independent Test**: Open each chapter page, enter valid inputs, click Solve — result table (lecturer format) appears, plot renders on black canvas, Smart Solve button triggers comparison.

**Dev B owns this phase. Dev A runs Phase 10 simultaneously.**

- [ ] T068 [P] [DevB] [US6] Wire Chapter 1 page to all 4 root-finding solvers + `EquationInputWidget` + result panel + plots in `numcore_gui/pages/chapter_1_page.py` — method dropdown: Bisection | Secant | Newton-Raphson | Simple Iteration; inline SDD/convergence checks shown where applicable
- [ ] T069 [P] [DevB] [US6] Wire Chapter 2 page to Jacobi + Gauss-Seidel + SDD verification display + solution vector plot in `numcore_gui/pages/chapter_2_page.py` — matrix A and b inputs; reordering notice if SDD reorder occurred
- [ ] T070 [P] [DevB] [US6] Wire Chapter 3 page to all 5 interpolation solvers + divided difference table display + interpolation curve plot in `numcore_gui/pages/chapter_3_page.py` — x_points + y_points list inputs; eval_x optional field
- [ ] T071 [P] [DevB] [US6] Wire Chapter 4 page to all 4 integration solvers + integration table display (h, x/y, weighted sum) + integration area plot in `numcore_gui/pages/chapter_4_page.py` — function input + a, b, n fields; validate n constraints inline
- [ ] T072 [DevB] [US6] Redesign `numcore_gui/dashboard.py` sidebar: remove all mission-themed labels; add section headers "Root Finding", "Linear Systems", "Interpolation", "Integration & Calc"; consistent BLACK/PANEL styling
- [ ] T073 [DevB] [US6] Set window defaults in `numcore_gui/dashboard.py`: minimum 1280×800, `set_appearance_mode("dark")`, black background applied
- [ ] T074 [DevB] [US6] Add status bar to `numcore_gui/dashboard.py`: shows last solver + elapsed time + current chapter; updates dynamically after each solve
- [ ] T075 [P] [DevB] [US6] Add inline result panels (CTkFrame below inputs) to all chapter pages: show solution value, iterations, converged/diverged status, divergence warning if applicable

**Checkpoint [DevB]**: Full GUI working for all 4 chapters with all Week 1–10 solvers.

---

## Phase 10: US7 — Post-Week 10 TUI Solvers [DevA] (Priority: P3)

**Goal**: Weeks 12–15 methods available via TUI for students using terminal.

**Independent Test**: `python main.py --tui` → navigate to each new method → solve a standard course problem → result within 0.1% of analytical answer.

**Dev A owns this phase. Dev B runs Phase 9 simultaneously.**

- [ ] T076 [P] [DevA] [US7] Implement `GaussianQuadratureSolver` (2-point and 3-point) in `numcore_engine/solvers/calculus_engine.py` — weights and nodes; compute integral; return `SimulationData` with n_points, integral
- [ ] T077 [P] [DevA] [US7] Implement `NumericalDifferentiationSolver` (2-point, 3-point endpoint, 3-point midpoint) in `numcore_engine/solvers/calculus_engine.py` — accept function or data points; return derivative values + formula type
- [ ] T078 [P] [DevA] [US7] Implement `CurveFittingSolver` in `numcore_engine/solvers/calculus_engine.py` — linear regression, quadratic regression, and linearization variants (power y=ax^b, exponential y=ae^bx, growth y=x/(a+bx))
- [ ] T079 [P] [DevA] [US7] Implement ODE solvers in `numcore_engine/solvers/ode_solver.py`: `TaylorSeriesOrder4Solver`, `RungeKutta4Solver`, `ModifiedEulerSolver` — accept y'=f(x,y), y(x₀)=y₀, return solution table
- [ ] T080 [DevA] [US7] Wire all Phase 10 solvers into TUI menus in `numcore_cli/terminal.py`: add Chapter 4 Advanced (Gaussian, Numerical Diff), Chapter 5 Curve Fitting, Chapter 6 ODE sections
- [ ] T081 [P] [DevA] [US7] Unit tests for post-Week 10 solvers in `tests/unit/test_calculus_engine.py` and `tests/unit/test_ode_solver.py` — verify against analytical solutions within 0.1%

**Checkpoint [DevA]**: All post-Week 10 methods accessible and tested via TUI.

---

## Phase 11: Polish & Cross-Cutting Concerns (Both)

**Purpose**: Final testing, cleanup, CSV export, startup selector, documentation.

- [ ] T082 [P] Write contract tests for ALL solvers (T011–T025, T076–T079) implementing Solver Protocol in `tests/contract/test_solver_protocol.py` — assert `solve()`, `get_steps()`, `validate_input()` present and callable on every class
- [ ] T083 [P] Integration tests: full TUI flow (input → solver → CSV export) in `tests/integration/test_cli_engine.py`
- [ ] T084 [P] Integration tests: full GUI flow (input → solve → result panel → plot) in `tests/integration/test_app_flow.py`
- [ ] T085 [DevA] Implement/verify `export_steps_to_csv()` in `numcore_cli/formatter.py` — accept SimulationData + method name + optional filename; write method-specific columns; default filename `results_<method>_<timestamp>.csv`
- [ ] T086 [P] Implement startup mode selector + argparse (`--tui`, `--gui`, `--help`, invalid → show help + menu) in `main.py`
- [ ] T087 [P] Grep and remove all mission-themed content (`Mission`, `Analyze Circuit`, etc.) from `numcore_gui/dashboard.py` and all chapter pages
- [ ] T088 [P] Add docstrings to all new solver classes (T011–T025, T047–T054, T056–T062, T076–T079)
- [ ] T089 Manual smoke test: all 4 chapters load; all 15 solvers produce results; Smart Solve works; --tui/--gui flags work; plots zoom/pan; CSV export creates valid file
- [ ] T090 Update `README.md` with solver list organized by course week, quick-start examples, Smart Solver usage

---

## 2-Person Parallel Execution Map

```
WEEK 1 (Phases 1–2, shared):
  Both  →  T001–T010  (setup + foundations, sequential then parallel)

WEEK 2–3 (Phases 3–5, fully parallel):
  DevA  →  T011–T027  (15 engine solvers + robustness + unit tests)
  DevB  →  T028–T038  (equation input widget + black theme)

WEEK 4 (Phases 6–7, still parallel):
  DevA  →  T039–T046  (lecturer format tables + formatter tests)
  DevB  →  T047–T055  (enhanced plotter + plot connections)

WEEK 5 (Phase 8, parallel within phase):
  DevA  →  T056–T062  (Smart Solver engine: runner, recommender, diagnostics)
  DevB  →  T063–T067  (Smart Solver UI: panel, table, diagnostics display)

WEEK 6 (Phases 9–10, parallel):
  DevA  →  T076–T081  (post-Week 10 TUI solvers)
  DevB  →  T068–T075  (GUI wiring + dashboard redesign)

WEEK 7 (Phase 11, shared):
  Both  →  T082–T090  (testing, CSV export, startup, docs, smoke test)
```

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1** (T001–T008): No dependencies — start immediately, all parallel
- **Phase 2** (T009–T010): Depends on Phase 1 — **BLOCKS all phases 3–11**
- **Phases 3–5** (T011–T038): All depend on Phase 2; fully parallel across DevA/DevB
- **Phase 6** (T039–T046): Depends on Phase 3 (needs solver metadata fields)
- **Phase 7** (T047–T055): Depends on Phases 3, 5 (needs solvers + black theme)
- **Phase 8** (T056–T067): Depends on Phases 3, 6 (DevA); Phases 4, 5, 7 (DevB)
- **Phase 9** (T068–T075): Depends on Phases 3–8
- **Phase 10** (T076–T081): Depends on Phase 3 (engine patterns); parallel with Phase 9
- **Phase 11** (T082–T090): Depends on Phases 9 + 10

### Within-Phase Dependencies

- T011–T025: All fully parallelizable (separate solver classes)
- T026 (divergence): Depends on T011–T016 existing
- T027 (unit tests): Depends on T011–T025 complete
- T028–T032 (widget): Sequential within Dev B (each step builds on previous)
- T034–T035 (theme files): Parallel (different files)
- T036–T037 (apply theme): After T034–T035
- T039–T045 (format functions): All parallel (separate functions)
- T056–T062 (engine runner): Sequential within Dev A (runner → wrappers → g(x) → selector → recommender → diagnostics → tests)
- T063–T067 (GUI Smart Solve): T063→T064→T065→T066→T067

---

## Implementation Strategy

### MVP (Minimum Viable Product)

Complete Phases 1–3, then Phase 4 + Phase 5, then Phase 6 + T067 (Smart Solve button):
- Working equation input + black theme + all 15 solvers + lecturer tables + basic Smart Solve
- Deliverable: functional black-theme GUI with equation input and all course methods

### Incremental Delivery

1. Phase 1–2 → project builds, models updated
2. Phase 3 → all 15 solvers testable via `uv run pytest tests/unit/`
3. Phase 4–5 → equation input widget demoed independently
4. Phase 6–7 → lecturer tables + plots verified
5. Phase 8 → Smart Solve end-to-end demo
6. Phase 9 → full GUI usable for all 4 chapters
7. Phase 10 → TUI complete for post-Week 10
8. Phase 11 → production-ready

---

## Summary Statistics

- **Total Tasks**: 90
- **Dev A Tasks**: 40 (engine, solvers, tables, Smart Solver logic, TUI, tests)
- **Dev B Tasks**: 38 (equation input, theme, plots, GUI wiring, Smart Solver UI)
- **Shared Tasks**: 12 (setup, foundations, polish, testing)
- **Parallelizable [P] Tasks**: 62
- **Sequential Tasks**: 28
- **User Story Coverage**:
  - US1 (Equation Input): T028–T033 — 6 tasks [DevB]
  - US2 (Smart Solver): T056–T067 — 12 tasks [Both]
  - US3 (Black Theme): T034–T038 — 5 tasks [DevB]
  - US4 (Enhanced Plots): T047–T055 — 9 tasks [DevB]
  - US5 (Lecturer Tables): T039–T046 — 8 tasks [DevA]
  - US6 (Course Solvers + GUI): T011–T027, T068–T075 — 25 tasks [DevA+DevB]
  - US7 (Post-Week 10 TUI): T076–T081 — 6 tasks [DevA]
