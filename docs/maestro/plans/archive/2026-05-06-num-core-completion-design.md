# Design Document: NUM-CORE Project Completion

**Date**: 2026-05-06
**Design Depth**: Standard
**Task Complexity**: Complex

## 1. Problem Statement
The NUM-CORE project has reached a point where the core infrastructure is solid, but significant gaps remain in the numerical engine and interface parity. This initiative aims to bridge these gaps by:
1. Completing the Numerical Engine (Chapter 5 Curve Fitting, Chapter 6 Advanced ODEs, Gaussian Quadrature).
2. Interface Synchronization: Wiring all solvers into both TUI and GUI.
3. Feature Polish: Textbook-style formatting, CSV export, and a Startup Mode Selector.
4. Quality Assurance: Hardening with Unit and Contract tests.

## 2. Requirements

### Functional Requirements
- **REQ-1 (Engine)**: Implement CurveFittingSolver (Linear, Quadratic, Power, Exponential, Growth models).
- **REQ-2 (Engine)**: Implement ModifiedEulerSolver and TaylorSeriesOrder4Solver.
- **REQ-3 (CLI)**: Add 'Compare Both Methods' to linear systems menu.
- **REQ-4 (CLI)**: Wire all Chapter 3-6 solvers into TUI menus.
- **REQ-5 (GUI)**: Finalize wiring for Chapter 1-4 pages; remove "mission-themed" content.
- **REQ-6 (General)**: Implement unified `export_steps_to_csv()` in `NumericalFormatter`.
- **REQ-7 (General)**: Implement startup mode selector in `main.py` with argparse support.

### Non-Functional Requirements
- **NFR-1 (Tech)**: Use Pure NumPy for all numerical logic; avoid SciPy.
- **NFR-2 (Design)**: Maintain unified formatting logic via `NumericalFormatter`.
- **NFR-3 (Quality)**: 100% coverage for new solvers via unit and contract tests.

## 3. Approach

### Selected Approach: Approach 1 — Full-Parity Synchronization
We will implement the remaining features in synchronized waves to ensure the Engine, TUI, and GUI reach maturity together.

### Decision Matrix
| Criterion | Weight | Approach 1 (Sync) | Approach 2 (Hardening) |
|-----------|--------|-------------------|-------------------------|
| Feature Parity | 40% | 5: Ensures TUI/GUI match engine status. | 3: UI lags backend. |
| User Accessibility | 30% | 5: New solvers usable immediately. | 2: Features invisible longer. |
| Reliability (Tests) | 30% | 4: Tests run per component. | 5: Test-first focus. |
| **Weighted Total** | | **4.7** | **3.3** |

### Alternatives Considered
- **Engine-Centric Hardening**: Rejected because it leaves the UI incomplete for too long, contradicting the "Finish It" goal for the end-user.

## 4. Architecture

### Component Overview
- **Engine Layer**: `Solver` Protocol and concrete implementations in `numcore_engine/solvers/`.
- **Application Layer**: `main.py` entry point with Startup Mode Selector.
- **Interface Layer**: `NumericalCLI` (TUI) and `Dashboard` (GUI).
- **Shared Utilities**: `NumericalFormatter` handles all Rich table rendering and CSV output.

### Data Flow
User Input -> Main Entry (Selector) -> Interface (TUI/GUI) -> Engine (Solver) -> Formatter (Display/CSV)

## 5. Agent Team
- **coder**: Lead Implementation (Engine & TUI wiring).
- **design_system_engineer**: GUI & UI Polish (Page completion, result panels, branding).
- **tester**: Quality Assurance (Unit & Contract tests).
- **technical_writer**: Documentation (Docstrings & README).

## 6. Risk Assessment
- **Symbolic Parsing**: New solvers may challenge the current parser. *Mitigation: Input validation and testing.*
- **Wiring Bottlenecks**: Parallel updates could cause merge conflicts. *Mitigation: Sequential UI wiring phases.*
- **Accuracy Deviations**: Gaussian Quadrature errors. *Mitigation: 0.1% analytical verification.*
- **Performance**: Large datasets. *Mitigation: Pure NumPy vectorization.*

## 7. Success Criteria
- All 20+ solvers functional and accessible via BOTH TUI and GUI.
- Working CSV export for all solver runs.
- Professional Startup Mode Selector and clean branding.
- 100% pass rate for contract and unit tests.
- Comprehensive documentation in code and README.md.
