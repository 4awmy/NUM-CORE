# Implementation Plan: Enhanced GUI, Auto-Solver Comparison, and Course-Complete Solver Suite

**Branch**: `002-enhanced-gui-solvers` | **Date**: 2026-05-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-enhanced-gui-solvers/spec.md`

## Summary

Deliver a fully course-aligned NUM-CORE solver suite (all methods through Week 10 of CCS3002) with five major enhancements over the existing codebase:

1. **Smart equation input** — text field with real-time matplotlib MathText preview
2. **Auto-solver comparison mode** — one-click comparison of all applicable methods per chapter
3. **True black theme** — pure #000000 backgrounds across GUI and all plots
4. **Enhanced interactive plots** — zoom/pan, method-specific visualizations, black canvas
5. **Lecturer methodology compliance** — exact table formats per method as prescribed by Dr. Ahmed Yehia

**Course solver scope**: All 15 methods through Week 10 ship in the GUI. Post-Week 10 methods (Weeks 12–15: Gaussian Quadrature, Numerical Differentiation, Curve Fitting, ODEs) are deferred to a subsequent TUI-only phase.

The existing modular architecture (engine → CLI/GUI layers) is retained and extended. All changes are additive.

---

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: `sympy`, `numpy`, `matplotlib`, `customtkinter`, `rich`, `pytest`
**Storage**: CSV file export only (no database); local filesystem
**Testing**: `pytest` via `uv run pytest`; coverage via `uv run pytest --cov=src`
**Target Platform**: Desktop — Windows, macOS, Linux
**Project Type**: Desktop application with dual interfaces (GUI primary, TUI secondary)
**Performance Goals**: Live equation preview renders within 300ms of keystroke; plot render within 1s of solve; GUI input response < 500ms; comparison mode for ≤4 methods completes within 3s
**Constraints**: Offline-capable; no network dependencies; double-precision float; no external LaTeX install required for math preview
**Scale/Scope**: Single-user desktop tool; up to 500 iterations per solver in comparison mode

---

## Constitution Check

*NUM-CORE Constitution (v1.0.0) gates:*

| Gate | Principle | Status | Notes |
|------|-----------|--------|-------|
| Engine-First Design | I | ✅ PASS | All 15 solvers + ComparisonRunner implemented in `numcore_engine/`. No UI logic in engine. |
| Protocol-Driven Contracts | II | ✅ PASS | All new solvers implement the frozen `Solver` Protocol. ComparisonRunner depends on Protocol, not concrete classes. |
| Dual Interface Parity | III | ⚠️ DEFERRED | Post-Week 10 methods (Weeks 12–15) are TUI-only in Phase H by design. GUI gets them in a future spec. Weeks 1–10 methods ship in both GUI and TUI. |
| Test-First Discipline | IV | ✅ PASS | Unit tests written per solver before implementation (separate test tasks). ≥85% engine coverage required. Contract tests added for `tests/contract/`. |
| Convergence & Stability | V | ✅ PASS | Divergence detection on all iterative solvers; SDD check enforced in linear solvers; convergence check displayed in Simple Iteration. |

**Complexity Tracking** (Principle III partial deferral):

| Deviation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Post-Week 10 GUI parity deferred | TUI-first for Weeks 12–15 keeps MVP deliverable; GUI pages are placeholders | Adding 10+ complex solvers (Gaussian Quadrature, ODEs, Curve Fitting) to GUI simultaneously would delay Week 1–10 delivery significantly |

---

## Project Structure

### Documentation (this feature)

```text
specs/002-enhanced-gui-solvers/
├── plan.md              ← this file
├── research.md          ← Phase 0 output
├── data-model.md        ← Phase 1 output
├── quickstart.md        ← Phase 1 output
├── contracts/
│   ├── solver-interface.md      ← Phase 1 output
│   ├── comparison-interface.md  ← Phase 1 output
│   └── equation-input.md        ← Phase 1 output
└── tasks.md             ← Phase 2 output (/speckit-tasks)
```

### Source Code (repository root)

```text
numcore_engine/
├── __init__.py
├── interfaces.py              # Solver Protocol + ComparisonRunner Protocol (extend only)
├── models.py                  # NumericalStep, SimulationData, ComparisonResult (extend only)
├── parser.py                  # Function string → callable (extend: accept ^ notation)
├── comparison.py              # ComparisonRunner — NEW
└── solvers/
    ├── root_finder.py         # Bisection, Secant, Newton-Raphson, Simple Iteration
    ├── network_solver.py      # Jacobi, Gauss-Seidel + SDD check
    └── calculus_engine.py     # Lagrange, Newton Fwd/Bwd Diff, Newton Fwd/Bwd Div Diff,
                               # Composite Trapezoidal, Composite Midpoint,
                               # Composite Simpson's 1/3 & 3/8

numcore_cli/
├── __init__.py
├── terminal.py                # Main TUI loop + menus (extend for comparison + new solvers)
└── formatter.py               # Rich table formatting (extend: lecturer-format tables, CSV)

numcore_gui/
├── __init__.py
├── dashboard.py               # Main CTk window + sidebar (black theme, restructured nav)
├── visualization.py           # PlotManager (all plot methods + interactive support)
├── equation_input.py          # EquationInputWidget — NEW (text field + preview canvas)
├── help_system.py
└── pages/
    ├── chapter_1_page.py      # Root finding: 4 solvers + compare
    ├── chapter_2_page.py      # Linear systems: 2 solvers + compare
    ├── chapter_3_page.py      # Interpolation: 5 solvers + compare
    └── chapter_4_page.py      # Integration: 4 solvers + compare

main.py                        # Startup mode selector (--tui / --gui flags)

tests/
├── unit/
│   ├── test_root_finder.py
│   ├── test_network_solver.py
│   ├── test_calculus_engine.py
│   └── test_comparison_runner.py
├── integration/
│   ├── test_app_flow.py
│   └── test_cli_engine.py
└── contract/
    └── test_solver_protocol.py    ← NEW (constitution requirement)
```

**Structure Decision**: Existing modular layout retained. New additions: `comparison.py` in engine, `equation_input.py` widget in GUI, `tests/contract/` directory. All solver additions are in-place extensions of existing modules.

---

## Implementation Phases

### Phase A — Engine: Course-Complete Solvers (No UI dependencies)
*All solver tasks are parallelizable. Priority: P1 (blocks all GUI phases)*

**Chapter 1 — Root Finding (4 solvers)**

| Task | File | Notes |
|------|------|-------|
| [P] `BisectionSolver` — validate f(a)·f(b)<0, Error=\|b-a\|/2 per iteration | `root_finder.py` | Lecturer table: n,a,b,c,f(a),f(b),f(c),Error |
| [P] `SecantSolver` — two initial points x₀,x₁, no derivative | `root_finder.py` | |
| [P] `NewtonRaphsonSolver` — sympy derivative, f(x₀)·f″(x₀)>0 check, f(xₙ)+f′(xₙ) per step | `root_finder.py` | Lecturer format: show f(xₙ), f′(xₙ) columns |
| [P] `SimpleIterationSolver` — accept g(x), compute and check \|g′(x₀)\|<1 before iterating | `root_finder.py` | Convergence check must surface in metadata |

**Chapter 2 — Linear Systems (2 solvers)**

| Task | File | Notes |
|------|------|-------|
| [P] `JacobiSolver` — SDD check+reorder, simultaneous update, SDD matrix in metadata | `network_solver.py` | Label: "simultaneous" |
| [P] `GaussSeidelSolver` — SDD check+reorder, successive update | `network_solver.py` | Label: "successive" |

**Chapter 3 — Interpolation (5 solvers)**

| Task | File | Notes |
|------|------|-------|
| [P] `LagrangeInterpolationSolver` — compute L_i(x) basis polynomials individually | `calculus_engine.py` | |
| [P] `NewtonForwardDifferenceSolver` — forward difference table + NFDF formula | `calculus_engine.py` | |
| [P] `NewtonBackwardDifferenceSolver` — backward difference table + NBDF formula | `calculus_engine.py` | |
| [P] `NewtonForwardDividedDifferenceSolver` — triangular divided difference table | `calculus_engine.py` | Lecturer triangular table format in metadata |
| [P] `NewtonBackwardDividedDifferenceSolver` — backward divided difference table | `calculus_engine.py` | |

**Chapter 4 — Integration (4 solvers)**

| Task | File | Notes |
|------|------|-------|
| [P] `CompositeTrapezoidalSolver` — h=(b-a)/n, table, weighted sum | `calculus_engine.py` | Formula: h/2[y₀+2(y₁+...+yₙ₋₁)+yₙ] |
| [P] `CompositeMidpointSolver` — h=(b-a)/n, table, weighted sum | `calculus_engine.py` | |
| [P] `CompositeSimpsonsOneThirdSolver` — validate n even, show weighted-sum pattern | `calculus_engine.py` | Inline error if n odd |
| [P] `CompositeSimpsonsThreeEighthsSolver` — validate n multiple of 3 | `calculus_engine.py` | Inline error if n%3≠0 |

**Cross-Cutting Robustness**

| Task | File | Notes |
|------|------|-------|
| [P] Divergence detection on all iterative solvers (5 consecutive growing errors) | all solver files | `metadata["diverged"] = True` |
| [P] Extend `parser.py` to normalize `^` → `**` and validate math expressions | `parser.py` | Enable `x^2` and `x**2` equivalence |
| [P] Add `export_steps_to_csv()` to `NumericalFormatter` (if not already complete) | `formatter.py` | |

---

### Phase B — Equation Input Widget (no solver dependencies)
*Can run in parallel with Phase A*

| Task | File | Notes |
|------|------|-------|
| Create `EquationInputWidget` CTk frame | `numcore_gui/equation_input.py` | Text entry + preview canvas |
| [P] Embed small matplotlib figure for MathText preview rendering | `equation_input.py` | Uses `matplotlib.mathtext`; no LaTeX install needed |
| Add live preview callback: debounce 300ms after keystroke → render `$f(x) = ...$` | `equation_input.py` | Debounce via `after()` |
| Display inline syntax error label below field on parse failure | `equation_input.py` | |
| Add function reference panel: buttons for sin, cos, tan, exp, ln, sqrt, π, e | `equation_input.py` | Inserts text snippet at cursor position |

---

### Phase C — Auto-Solver Comparison Engine (depends on Phase A)
*Sequential within this phase; parallelizable C1 vs C2*

| Task | File | Notes |
|------|------|-------|
| [P] Create `ComparisonRunner` class in `numcore_engine/comparison.py` | `comparison.py` | Accepts problem dict + list of Solver instances; runs all; returns ComparisonResult |
| [P] Add `ComparisonResult` to `numcore_engine/models.py` | `models.py` | Holds list of SolverResults, best_method name, input_params |
| Define `chapter_1_compare()`, `chapter_2_compare()`, `chapter_3_compare()`, `chapter_4_compare()` runner functions | `comparison.py` | Chapter-specific convenience wrappers |

---

### Phase D — True Black Theme (parallel with B, C)
*Parallelizable visual changes*

| Task | File | Notes |
|------|------|-------|
| [P] Define custom matplotlib style: `numcore_black.mplstyle` with all backgrounds #000000 | `numcore_gui/styles/numcore_black.mplstyle` | Register at app startup |
| [P] Configure CTk theme: override all frame/window/panel backgrounds to #000000 | `dashboard.py` | Use CTk `configure(fg_color="#000000")` throughout |
| [P] Define app-wide color palette constants file | `numcore_gui/theme.py` | BLACK, ACCENT_BLUE, ACCENT_ORANGE, TEXT_PRIMARY, TEXT_SECONDARY, SUCCESS_GREEN, ERROR_RED, WARN_YELLOW |
| Apply theme palette to all existing chapter pages | all chapter pages | |

---

### Phase E — Enhanced Plotter (depends on Phase A + D)
*Parallelizable: each plot type is independent*

| Task | File | Notes |
|------|------|-------|
| [P] Add `NavigationToolbar2Tk` to all embedded plot canvases for zoom/pan | `visualization.py` | Standard matplotlib toolbar; embedded in CTk frame |
| [P] `plot_bisection_brackets()` — function curve + narrowing bracket markers per iteration | `visualization.py` | Unique to Bisection |
| [P] `plot_newton_tangents()` — function curve + tangent lines at each Newton step | `visualization.py` | Unique to Newton-Raphson |
| [P] `plot_convergence_log()` — error vs iteration, log-Y, tolerance threshold line | `visualization.py` | All iterative solvers |
| [P] `plot_comparison()` — overlay all method error curves, distinct colors, legend | `visualization.py` | Comparison mode |
| [P] `plot_interpolation_curve()` — scatter + polynomial curve overlay, legend | `visualization.py` | Interpolation |
| [P] `plot_integration_area()` — curve + filled area + annotated integral value | `visualization.py` | Integration |
| [P] `plot_solution_vector()` — bar chart for linear system solution vector | `visualization.py` | Linear systems |

---

### Phase F — Lecturer Methodology Result Display (depends on Phase A)
*Parallelizable per chapter*

| Task | File | Notes |
|------|------|-------|
| [P] `format_bisection_table()` — columns: n,a,b,c,f(a),f(b),f(c),Error=\|b-a\|/2 | `formatter.py` | |
| [P] `format_simple_iteration_table()` — convergence check header + iteration table | `formatter.py` | Show \|g′(x₀)\| < 1 with pass/fail |
| [P] `format_newton_raphson_table()` — show f(x₀)·f″(x₀)>0 check + f(xₙ),f′(xₙ) columns | `formatter.py` | |
| [P] `format_sdd_verification()` — per-row diagonal dominance check table | `formatter.py` | \|a_ii\| > Σ\|a_ij\| per row, pass/fail |
| [P] `format_divided_difference_table()` — triangular layout: x₀,y₀,1st DD,2nd DD,... | `formatter.py` | |
| [P] `format_integration_table()` — h value, x/y table, weighted-sum formula, result | `formatter.py` | |
| [P] `format_comparison_table()` — per-method: solution, iterations, final error, status, time; best highlighted | `formatter.py` | |

---

### Phase G — GUI Page Wiring (depends on A + B + D + F)
*Parallelizable: each chapter page is independent*

| Task | File | Notes |
|------|------|-------|
| [P] Wire Chapter 1 page: 4 root finders + comparison mode + EquationInputWidget | `chapter_1_page.py` | |
| [P] Wire Chapter 2 page: 2 linear solvers + comparison mode (matrix input) | `chapter_2_page.py` | Matrix input: separate field for A and b |
| [P] Wire Chapter 3 page: 5 interpolation solvers + comparison mode | `chapter_3_page.py` | x_points + y_points inputs |
| [P] Wire Chapter 4 page: 4 integration solvers + comparison mode | `chapter_4_page.py` | Show function input + a, b, n fields |
| Connect all chapter pages to enhanced plots (Phase E) | all chapter pages | |
| Add "Auto-Compare All Methods" button to all chapter pages | all chapter pages | |

---

### Phase H — Dashboard Redesign (parallel with G)
*Parallelizable visual layout work*

| Task | File | Notes |
|------|------|-------|
| Redesign sidebar: chapters 1–4 + section titles, no mission-themed labels | `dashboard.py` | |
| Set window minimum: 1280×800, dark theme, black background | `dashboard.py` | |
| Add status bar (last action, current chapter, solve time) | `dashboard.py` | |

---

### Phase I — Post-Week 10 TUI Solvers (depends on Phase A engine patterns)
*Deferred; TUI-only; parallelizable*

| Task | File | Notes |
|------|------|-------|
| [P] `GaussianQuadratureSolver` (2-pt + 3-pt) | `calculus_engine.py` | TUI-only for now |
| [P] `NumericalDifferentiationSolver` (2-pt, 3-pt endpoint, 3-pt midpoint) | `calculus_engine.py` | |
| [P] `CurveFittingSolver` (linear, quadratic regression + 4 linearization variants) | `calculus_engine.py` | |
| [P] `TaylorSeriesODESolver` (Order 4) | new file: `ode_solver.py` | |
| [P] `RungeKutta4Solver` | `ode_solver.py` | |
| [P] `ModifiedEulerSolver` | `ode_solver.py` | |
| Wire all Phase I solvers into TUI menus | `terminal.py` | New TUI chapter menus |

---

### Phase J — Testing & Polish (depends on all above)
*Sequential validation*

| Task | File | Notes |
|------|------|-------|
| Write/run contract tests for all solver Protocol compliance | `tests/contract/test_solver_protocol.py` | NEW (constitution requirement) |
| Write/run unit tests for all Phase A–I solvers (≥85% engine coverage) | `tests/unit/` | |
| Write/run integration tests (TUI→solver→output, GUI→solve→result panel, CSV export) | `tests/integration/` | |
| Manual smoke test (all chapters, all methods, startup flags) | manual | |
| Update README.md with solver list organized by week/chapter | `README.md` | |
| Docstrings for all new solver classes | all engine files | |
| Remove remaining mission-themed content | dashboard.py, pages | |

---

## Dependency Graph

```
Phase A (Engine Solvers) ─────┬──→ Phase C (Comparison Engine)
                               ├──→ Phase E (Enhanced Plotter)
                               └──→ Phase F (Lecturer Tables)

Phase B (Equation Input) ─────┐
Phase C (Comparison Engine) ──┤
Phase D (Black Theme) ─────────┤──→ Phase G (GUI Wiring)
Phase E (Enhanced Plotter) ───┤
Phase F (Lecturer Tables) ────┘

Phase A (Engine Patterns) ────────→ Phase I (Post-Week 10 TUI)

Phase G + H (GUI + Dashboard) ────→ Phase J (Polish & Testing)

Phase I ──────────────────────────→ Phase J (Polish & Testing)
```

---

## Recommended MVP Scope

- **Minimum deliverable**: Phase A + Phase B + Phase D + Phase G (all 15 solvers wired to GUI with equation input and black theme)
- **Core value add**: Phase C + Phase F (comparison mode + lecturer-format tables — the academic study tools)
- **Polish**: Phase E + Phase H + Phase J (enhanced plots, dashboard redesign, full testing)
- **Deferred**: Phase I (post-Week 10 TUI solvers)
