<!-- SYNC IMPACT REPORT
Version: 0.0.0 → 1.0.0 (initial ratification)
Principles: 5 core principles defined
Sections: Quality Gates + Development Workflow added
New version reflects first formal constitution adoption
Templates flagged for alignment validation: plan-template.md, spec-template.md, tasks-template.md
-->

# NUM-CORE Constitution

## Core Principles

### I. Engine-First Design

Every numerical solver is implemented in `numcore_engine/` as a standalone, independently testable module. The engine has **zero dependencies** on CLI or GUI code. Solvers are pure mathematical implementations—presentation layers (TUI/GUI) depend on the engine, never reverse.

**Mandatory rules**:
- New solvers MUST be added to `numcore_engine/solvers/` and implement the `Solver` Protocol.
- Engine code is never modified to accommodate UI-specific requirements; UI adapts to engine contracts.
- No circular imports between engine ↔ UI modules.

---

### II. Protocol-Driven Contracts

All solver classes MUST implement the frozen `Solver` Protocol defined in `numcore_engine/interfaces.py`:

```python
class Solver(Protocol):
    def solve(self, **kwargs: Any) -> SimulationData: ...
    def get_steps(self) -> List[NumericalStep]: ...
    def validate_input(self, **kwargs: Any) -> bool: ...
```

**Rationale**: Uniform interface enables seamless swapping of solver implementations and ensures both CLI and GUI can invoke any solver identically. No solver-specific branching logic in UI code.

---

### III. Dual Interface Parity

Every solver feature accessible via TUI MUST be equally accessible via GUI within the same feature release. This includes comparison modes, visualization, and data export.

**Mandatory rules**:
- New solver methods (e.g., Jacobi) appear in both CLI and GUI in the same sprint.
- Feature flags/toggles are prohibited; both interfaces ship complete features together.
- Documentation and examples must cover both interfaces.

**Rationale**: Students and engineers should have consistent experience regardless of interface choice. Prevents fragmentation and reduces support burden.

---

### IV. Test-First (Non-Negotiable)

TDD is mandatory. All solver implementations follow: **Test → Approval → Red → Green → Refactor**.

**Mandatory rules**:
- Unit tests written before solver code; test structure approved by architect.
- Solvers tested against analytical solutions with known answers (e.g., √4 = 2, linear systems solved correctly).
- Integration tests verify CLI and GUI correctly invoke solvers and display results.
- Minimum coverage: 85% for engine; 70% for UI layers.
- No solver merged without passing all tests + coverage validation.

**Test categories**:
- **Unit** (`tests/unit/`): Individual solver correctness against analytical solutions.
- **Integration** (`tests/integration/`): App flow, engine→CLI→UI data pipeline.
- **Contract** (`tests/contract/`): Solver Protocol compliance, input validation.

---

### V. Convergence & Stability

All iterative solvers MUST detect and communicate divergence to users. Mathematical correctness takes precedence over optimistic output.

**Mandatory rules**:
- Divergence detection: Track error over 5 iterations; if monotonically increasing, flag `metadata["diverged"] = True`.
- Divergent results returned with clear warning; solvers do NOT silently return wrong answers.
- Non-convergent systems (singular matrices) flagged immediately with actionable guidance (e.g., "Check diagonal dominance").
- All edge cases (NaN, division by zero, overflow) caught and reported with user-friendly explanation.

**Rationale**: Educational tool must build trust; accuracy and transparency are non-negotiable.

---

## Quality Gates

*Projects MUST pass all gates before feature merge.*

| Gate | Criteria | Owner |
|------|----------|-------|
| **Solver Correctness** | Analytical validation; ≤0.1% error vs known solution | Coder + Tester |
| **Test Coverage** | ≥85% engine, ≥70% UI; no untested branches in core logic | Test Suite (automated) |
| **Interface Compliance** | Implements Solver Protocol fully; no breaking signature changes | Code Review |
| **Error Handling** | All user inputs validated; all failure modes tested and reported | QA Test |
| **Dual Interface** | Feature works in both CLI and GUI; documented in both | Integration Test |

---

## Development Workflow

### Task Decomposition

Features are broken into **parallel-ready tasks** (marked `[P]` in `tasks.md`):
- Each task ≤4 hours of work; testable independently.
- Tasks with no data dependencies can run in parallel (e.g., adding Jacobi solver and improving GUI styling).
- Sequential dependencies are minimal and explicitly marked in task dependency graph.

**Sprint structure** (per feature):
1. **Engine Phase**: Implement + unit test solver (parallelizable per solver).
2. **CLI Phase**: Wire TUI to solver, add comparison mode if applicable.
3. **GUI Phase**: Wire GUI pages to solver, add visualization.
4. **Polish Phase**: Error messages, edge cases, documentation.

### Code Review Standards

- All PRs reviewed against constitution compliance (engine encapsulation, protocol adherence, test-first discipline).
- No feature merged if gates not passed.
- Complexity justified in review comment if adding >200 LOC to a single file.

---

## Observability & User Feedback

### Required Signals

- **Errors**: Inline messages in GUI (below field); stderr in CLI. Never silent failures.
- **Convergence**: Iteration count, final error, status (converged/diverged/max_iterations) displayed after solve.
- **Plots**: Live matplotlib plots in GUI; ASCII-art iteration tables in CLI (Rich formatted).

### Logging (Internal Debug Only)

- Solvers log step data for debugging (e.g., x_n, error per iteration) to in-memory list.
- No external logging framework required; `get_steps()` provides debug info.
- File logging out of scope for v1.

---

## Governance

**Constitution Authority**: This constitution supersedes all other development guidance. If a task conflicts with a core principle, the principle takes precedence.

**Amendment Process**:
1. Proposed amendment documented with rationale in a PR.
2. Approved by codebase architect and at least one active contributor.
3. Amendment recorded in `## Clarifications` section (dated) at top of constitution.
4. Version incremented:
   - **MAJOR**: Principle removed or materially redefined.
   - **MINOR**: Principle added or significantly expanded.
   - **PATCH**: Wording clarification, typo fix, no semantic change.

**Compliance Review**: After each `/speckit-plan`, verify plan adheres to all core principles (Constitution Check gate).

**Guidance File**: See `CLAUDE.md` for agent-specific development workflows and command invocations.

---

## Clarifications

*Amendment history (if any)*

---

**Version**: 1.0.0 | **Ratified**: 2026-04-29 | **Last Amended**: 2026-04-29
