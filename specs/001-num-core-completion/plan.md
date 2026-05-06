# Implementation Plan: NUM-CORE Complete Solver Suite

**Branch**: `001-num-core-completion` | **Date**: 2026-04-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-num-core-completion/spec.md`

## Summary

Complete the NUM-CORE numerical engineering solver suite across 4 chapters with comprehensive numerical methods:

- **Chapter 1**: Root Finding — Bisection, Secant, Newton–Raphson, Simple Iteration
- **Chapter 2**: Linear Systems — Jacobi, Gauss–Seidel
- **Chapter 3**: Interpolation — Lagrange, Newton Forward/Backward Difference, Newton Forward/Backward Divided Difference
- **Chapter 4**: Integration & Differentiation — Midpoint, Trapezoidal, Simpson's (each with Basic + Composite variants), Gaussian Quadrature, Numerical Differentiation

Deliverables: GUI chapter pages with real solver wiring, scientific applications showcase per chapter, live matplotlib plots, CSV export, comparison modes, divergence detection, and startup mode selector. The architecture already exists; this plan completes the bridge between engine, CLI, and GUI layers.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: `sympy`, `numpy`, `matplotlib`, `customtkinter`, `rich`, `pytest`
**Storage**: CSV file export only (no database); local filesystem
**Testing**: `pytest` with `uv run pytest`; coverage via `uv run pytest --cov=src`
**Target Platform**: Desktop — Windows, macOS, Linux
**Project Type**: Desktop application with dual interfaces (TUI + GUI)
**Performance Goals**: Solver convergence plots render within 1 second; GUI input response < 500ms
**Constraints**: Offline-capable; no network dependencies; double-precision floating point
**Scale/Scope**: Single-user desktop tool; up to 1000 iterations per solver call

## Constitution Check

*NUM-CORE Constitution (v1.0.0) gates validation:*

| Gate | Principle | Status | Notes |
|------|-----------|--------|-------|
| Protocol-Driven Contracts | II | ✅ PASS | `Solver` Protocol in `interfaces.py`; all solvers implement it |
| Engine-First Design | I | ✅ PASS | Engine standalone; UI depends on engine, not reverse |
| Dual Interface Parity | III | ✅ PASS | All features planned for both CLI and GUI (comparison mode in both) |
| Test-First Discipline | IV | ✅ PASS | Test structure planned; unit + integration tests required |
| Convergence & Stability | V | ✅ PASS | Divergence detection + warnings for all iterative solvers |

## Project Structure

### Documentation (this feature)

```text
specs/001-num-core-completion/
├── plan.md              ← this file
├── research.md          ← Phase 0 output
├── data-model.md        ← Phase 1 output
├── quickstart.md        ← Phase 1 output
├── contracts/           ← Phase 1 output
│   ├── solver-interface.md
│   ├── tui-commands.md
│   └── gui-contracts.md
└── tasks.md             ← Phase 2 output (/speckit-tasks)
```

### Source Code (repository root)

```text
numcore_engine/
├── __init__.py
├── interfaces.py          # Solver Protocol (DO NOT CHANGE)
├── models.py              # NumericalStep, SimulationData (extend only)
├── parser.py              # Function string → callable
└── solvers/
    ├── root_finder.py     # Newton-Raphson + Simple Iteration
    ├── network_solver.py  # Gauss-Seidel (add Jacobi here)
    └── calculus_engine.py # Interpolation + Integration

numcore_cli/
├── __init__.py
├── terminal.py            # Main TUI loop + menus
└── formatter.py           # Rich table formatting + CSV export

numcore_gui/
├── __init__.py
├── dashboard.py           # Main CTk window + sidebar
├── visualization.py       # PlotManager (add all plot methods)
├── help_system.py
└── pages/
    ├── chapter_1_page.py         # Bisection Method solver interface
    ├── chapter_1_app.py          # Scientific applications for Chapter 1 (NEW)
    ├── chapter_2_page.py         # Linear Systems: Jacobi & Gauss-Seidel solver interface
    ├── chapter_2_app.py          # Scientific applications for Chapter 2 (NEW)
    ├── chapter_3_page.py         # Interpolation: Newton's Divided Difference solver interface
    ├── chapter_3_app.py          # Scientific applications for Chapter 3 (NEW)
    ├── chapter_4_page.py         # Integration: Trapezoidal Rule solver interface
    └── chapter_4_app.py          # Scientific applications for Chapter 4 (NEW)

main.py                    # Startup mode selector
tests/
├── unit/
│   ├── test_root_finder.py
│   ├── test_network_solver.py
│   └── test_calculus_engine.py
└── integration/
    ├── test_app_flow.py
    └── test_cli_engine.py
```

**Structure Decision**: Existing modular layout retained. All changes are additive within existing modules. No new packages needed.

## Complexity Tracking

No constitution violations. All changes extend existing patterns.

## Implementation Phases

### Phase A — Engine Completeness (No UI dependencies)
*Parallelizable engine work: each solver is independent*

**Chapter 1 — Root Finding** (4 solvers):
| Task | File | Priority |
|------|------|----------|
| [P] Implement `BisectionSolver` | `root_finder.py` | P1 |
| [P] Implement `SecantSolver` | `root_finder.py` | P1 |
| [P] Implement/enhance `NewtonRaphsonSolver` | `root_finder.py` | P1 |
| [P] Implement/enhance `SimpleIterationSolver` | `root_finder.py` | P1 |

**Chapter 2 — Linear Systems** (2 solvers):
| Task | File | Priority |
|------|------|----------|
| [P] Implement/enhance `JacobiSolver` | `network_solver.py` | P1 |
| [P] Implement/enhance `GaussSeidelSolver` | `network_solver.py` | P1 |

**Chapter 3 — Interpolation** (3 solvers):
| Task | File | Priority |
|------|------|----------|
| [P] Implement `LagrangeInterpolationSolver` | `calculus_engine.py` | P1 |
| [P] Implement `NewtonDifferenceTableSolver` (forward/backward difference) | `calculus_engine.py` | P1 |
| [P] Implement `NewtonDividedDifferenceSolver` (forward/backward divided difference) | `calculus_engine.py` | P1 |

**Chapter 4 — Integration & Differentiation** (5 solvers):
| Task | File | Priority |
|------|------|----------|
| [P] Implement `MidpointSolver` (basic + composite) | `calculus_engine.py` | P1 |
| [P] Implement `TrapezoidalSolver` (basic + composite) | `calculus_engine.py` | P1 |
| [P] Implement `SimpsonsRuleSolver` (basic + composite) | `calculus_engine.py` | P1 |
| [P] Implement `GaussianQuadratureSolver` | `calculus_engine.py` | P1 |
| [P] Implement `NumericalDifferentiationSolver` | `calculus_engine.py` | P1 |

**All Solvers — Robustness**:
| Task | File | Priority |
|------|------|----------|
| [P] Add divergence detection to all iterative solvers (Bisection, Secant, Newton, Simple Iteration, Jacobi, Gauss-Seidel) | all solver files | P1 |
| [P] Add `export_steps_to_csv()` to `NumericalFormatter` | `formatter.py` | P2 |

### Phase B — TUI Enhancements (depends on Phase A)
*Sequential within phase, can parallelize B1 vs B2*

| Task | File | Priority |
|------|------|----------|
| [P] Add comparison mode (option 3) to linear systems menu | `terminal.py` | P1 |
| [P] Add CSV export prompt after every `run_*()` call | `terminal.py` | P2 |
| [P] Add divergence warning panel in TUI results | `terminal.py` | P1 |

### Phase C — GUI Wiring (depends on Phase A)
*Parallelizable: each chapter page is independent*

| Task | File | Priority |
|------|------|----------|
| [P] Wire Chapter 1 page to all 4 root-finding solvers (Bisection, Secant, Newton, Simple Iteration) | `chapter_1_page.py` | P1 |
| [P] Wire Chapter 2 page to both linear system solvers (Jacobi, Gauss-Seidel) + comparison mode | `chapter_2_page.py` | P1 |
| [P] Wire Chapter 3 page to all 3 interpolation solvers (Lagrange, Difference Table, Divided Difference) | `chapter_3_page.py` | P1 |
| [P] Wire Chapter 4 page to all 5 integration/differentiation solvers (Midpoint, Trapezoidal, Simpson's, Gaussian, Numerical Diff) | `chapter_4_page.py` | P1 |
| Add method selector dropdowns for each chapter with variants (basic/composite where applicable) | all chapter pages | P1 |

### Phase D — GUI Redesign (parallel with C)
*Parallelizable: visual changes per chapter page*

| Task | File | Priority |
|------|------|----------|
| [P] Redesign dashboard layout + sidebar navigation (remove mission theme, add chapter names) | `dashboard.py` | P1 |
| [P] Add method selector dropdowns + result panels to all chapter pages | all chapter pages | P1 |
| [P] Increase window to 1280x800, dark theme default | `dashboard.py` | P1 |

### Phase E — Visualization (depends on C + D)
*Parallelizable: each plot type is independent*

**Plot Methods (PlotManager)**:
| Task | File | Priority |
|------|------|----------|
| [P] Add `plot_convergence_log()` (error vs iteration, log scale) | `visualization.py` | P2 |
| [P] Add `plot_comparison()` (overlay 2+ solver curves) | `visualization.py` | P2 |
| [P] Add `plot_function_with_roots()` (function curve + root markers) | `visualization.py` | P2 |
| [P] Add `plot_solution_vector()` (bar chart for linear systems) | `visualization.py` | P2 |
| [P] Add `plot_interpolation_curve()` (scatter + polynomial overlay) | `visualization.py` | P2 |
| [P] Add `plot_integration_area()` (curve + filled area under) | `visualization.py` | P2 |
| [P] Add `plot_differentiation_derivative()` (original + derivative curves) | `visualization.py` | P2 |

**Page Connections**:
| Task | File | Priority |
|------|------|----------|
| [P] Connect Chapter 1 page to convergence + function root plots | `chapter_1_page.py` | P2 |
| [P] Connect Chapter 2 page to convergence + solution vector plots | `chapter_2_page.py` | P2 |
| [P] Connect Chapter 3 page to interpolation curve plots | `chapter_3_page.py` | P2 |
| [P] Connect Chapter 4 page to integration/differentiation plots | `chapter_4_page.py` | P2 |

### Phase F — Startup & Polish (depends on all above)
*Sequential*

| Task | File | Priority |
|------|------|----------|
| Implement startup mode selector (menu + --tui/--gui flags) | `main.py` | P1 |
| Add status bar to GUI window | `dashboard.py` | P2 |

### Phase G — Scientific Applications Pages (depends on C + D)
*Parallelizable: each chapter gets its own applications page*

| Task | File | Priority |
|------|------|----------|
| [P] Create Chapter 1 applications page (Bisection real-world use case) | `numcore_gui/pages/chapter_1_app.py` (NEW) | P2 |
| [P] Create Chapter 2 applications page (Linear systems real-world use case) | `numcore_gui/pages/chapter_2_app.py` (NEW) | P2 |
| [P] Create Chapter 3 applications page (Interpolation real-world use case) | `numcore_gui/pages/chapter_3_app.py` (NEW) | P2 |
| [P] Create Chapter 4 applications page (Integration real-world use case) | `numcore_gui/pages/chapter_4_app.py` (NEW) | P2 |
| Add navigation to scientific apps pages in dashboard sidebar | `dashboard.py` | P2 |

**Content per applications page**:
- Real-world problem statement (e.g., "Finding optimal beam thickness" for Chapter 1)
- Step-by-step walkthrough with sample data
- Pre-filled solver inputs for the example
- Results visualization with explanation and interpretation
- "Try it yourself" section to modify inputs and re-solve live
- Educational text explaining when/why this method is used

## Dependency Graph

```
Phase A (Engine) ──┬──→ Phase B (TUI)
                   ├──→ Phase C (GUI Wiring)
                   └──→ Phase D (GUI Redesign)

Phase C + D ────────────→ Phase E (Visualization)

Phase C + D ────────────→ Phase G (Scientific Applications)

Phase B + E + G ────────→ Phase F (Startup & Polish)
```
