# Research: NUM-CORE Complete Solver Suite

**Phase**: 0 — Outline & Research
**Date**: 2026-04-29
**Feature**: `specs/001-num-core-completion`

## Findings

### Decision 1: Jacobi Solver Architecture
- **Decision**: Implement `JacobiSolver` as a new class in `network_solver.py` following the exact same pattern as `GaussSeidelSolver`
- **Rationale**: Jacobi and Gauss-Seidel differ only in update timing (Jacobi uses x_old for all updates in iteration; G-S uses x_new immediately). Same input/output contract.
- **Alternatives considered**: Subclassing from a shared base class. Rejected because frozen Protocol-style solvers work better as independent composable classes with identical interfaces.

### Decision 2: Divergence Detection Strategy
- **Decision**: Track last 5 errors in a rolling window; if monotonically increasing for 5 steps, set `metadata["diverged"] = True` and break early
- **Rationale**: 5-step window balances noise tolerance vs early detection. Industry standard for iterative solver safety checks.
- **Alternatives considered**: Single-step error comparison (too noisy), adaptive threshold (over-engineering for this scope).

### Decision 3: Function Parsing for GUI
- **Decision**: Use existing `parser.py` (sympy-based) for GUI function input, same as CLI
- **Rationale**: Parser already handles Python-syntax expressions (x**2 - 4). No duplication needed.
- **Alternatives considered**: eval() — rejected (security risk). A separate GUI parser — rejected (duplication).

### Decision 4: Matrix Input Parsing in GUI
- **Decision**: Use `ast.literal_eval()` for matrix input (e.g., `[[2,1],[1,3]]`) in GUI
- **Rationale**: Safe alternative to eval(); handles Python list syntax natively without external deps.
- **Alternatives considered**: JSON parsing — rejected (uses `null` not `None`, unfamiliar to students). Custom parser — rejected (over-engineering).

### Decision 5: CSV Export Format
- **Decision**: Use Python built-in `csv` module. Columns match displayed Rich table for each method. Filename: `results_<method>_<YYYYMMDD_HHMMSS>.csv`
- **Rationale**: No additional dependencies. Predictable naming enables easy file management.
- **Alternatives considered**: Excel (openpyxl) — rejected (dependency overhead). JSON — rejected (less readable for iteration tables).

### Decision 6: matplotlib Integration in CTk GUI
- **Decision**: Embed matplotlib in CustomTkinter using `FigureCanvasTkAgg` from `matplotlib.backends.backend_tkagg`
- **Rationale**: Standard, well-documented approach for matplotlib embedding in tkinter-based apps. Already partially implemented in `visualization.py`.
- **Alternatives considered**: Saving to PNG and displaying as CTkImage — rejected (static, no interactivity).

### Decision 7: Startup Mode Selector
- **Decision**: Rich Panel + IntPrompt for interactive menu; argparse for `--tui` / `--gui` / `--help` flags
- **Rationale**: Consistent with existing Rich usage in TUI. Argparse is stdlib, no new deps.
- **Alternatives considered**: click — rejected (new dependency). Pure argparse only — rejected (breaks current interactive startup UX).

### Decision 8: GUI Page Redesign Scope
- **Decision**: Rename all mission-themed labels to method names; add method selector dropdown, tolerance/maxiter fields, result panel, status bar. Increase window to 1280x800. Dark default theme.
- **Rationale**: Directly addresses ISSUE #1. Academic context requires clear, professional naming.
- **Alternatives considered**: Full redesign with new layout manager — rejected (too risky, high churn). Minimal rename-only — rejected (doesn't add tolerance/result panel UX which is critical).

## Open Questions (Resolved)

All clarifications resolved. No NEEDS CLARIFICATION items remain.
