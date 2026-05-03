# Feature Specification: Complete NUM-CORE Numerical Solver Suite

**Feature Branch**: `001-num-core-completion`
**Created**: 2026-04-29
**Status**: Draft
**Input**: Complete NUM-CORE numerical solver suite with dual CLI/GUI interfaces

## Clarifications

### Session 2026-04-29

- Q: Should the GUI Network Solver page support a "Compare Both" mode showing overlaid Jacobi vs Gauss-Seidel error curves, or is comparison mode TUI-only? → A: GUI includes compare mode — method dropdown has "Compare Both", renders overlaid curves.
- Q: When divergence is detected mid-run, does the solver stop immediately and return partial results, or complete all max_iter iterations? → A: Complete all iterations and flag as diverged at the end.
- Q: When GUI input validation fails, should errors appear inline next to the field or as a modal dialog popup? → A: Inline error display below/next to field.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Engineer Solves Root-Finding Problem (Priority: P1)

An engineer needs to find the root of a non-linear equation (e.g., beam stress calculation). They want to:
1. Input a mathematical function via terminal or GUI
2. Choose between Newton-Raphson or Simple Iteration methods
3. Set initial guess and convergence tolerance
4. See convergence progress with iteration count and error tracking
5. Compare how different methods perform on the same problem

**Why this priority**: Core functionality - solves fundamental engineering problem that drives the entire product.

**Independent Test**: Full workflow from function input → method selection → convergence display → result validation.

**Acceptance Scenarios**:

1. **Given** user provides function f(x)=x²-4 and initial guess x₀=1, **When** Newton-Raphson is selected, **Then** system returns root ≈ 2.0 in under 10 iterations with error tracking displayed.
2. **Given** convergence comparison is selected, **When** both methods solve identical problem, **Then** side-by-side iteration count and error curves are shown.
3. **Given** method diverges, **When** error grows for 5 consecutive iterations, **Then** system warns user and suggests correcting initial guess.

---

### User Story 2 - Engineer Solves Linear System Problem (Priority: P1)

An engineer needs to solve a system of linear equations Ax=b (e.g., circuit analysis, pipe networks). They want to:
1. Input coefficient matrix A and vector b
2. Choose between Gauss-Seidel or Jacobi methods
3. System automatically checks for diagonal dominance
4. If not dominant, system reorders equations to achieve dominance
5. View solution vector, iteration count, and convergence status
6. Compare both methods side-by-side

**Why this priority**: Core functionality - solves second fundamental engineering problem.

**Independent Test**: Full workflow from matrix input → method selection → diagonal dominance handling → solution display.

**Acceptance Scenarios**:

1. **Given** non-diagonally-dominant matrix, **When** Gauss-Seidel is attempted, **Then** system automatically reorders rows and solves successfully.
2. **Given** coefficient matrix 3x3 and vector b, **When** solution converges, **Then** solution vector [x₁, x₂, x₃] is displayed with iteration count.
3. **Given** comparison mode is active, **When** Jacobi and Gauss-Seidel solve same system, **Then** metrics (iterations, final error, convergence status) are shown side-by-side.

---

### User Story 3 - Engineer Interpolates Data and Integrates Functions (Priority: P1)

An engineer has experimental data points (x, y) and needs to:
1. Perform Newton's Divided Difference interpolation to find polynomial passing through points
2. Use numerical integration (Trapezoidal/Simpson's) to compute area under curve
3. See interpolation polynomial displayed as curve overlay on scatter plot
4. Dynamically add/modify points and see polynomial update instantly

**Why this priority**: Core calculus functionality - third fundamental engineering problem.

**Independent Test**: Full workflow from data input → interpolation/integration → visualization.

**Acceptance Scenarios**:

1. **Given** data points (1,2), (2,5), (3,10), **When** interpolation is selected, **Then** polynomial coefficients are computed and displayed.
2. **Given** same data points, **When** integration is selected, **Then** area under polynomial is computed using selected method.
3. **Given** user modifies a data point, **When** update is triggered, **Then** polynomial and integral recalculate instantly.

---

### User Story 4 - User Chooses Interface at Startup (Priority: P1)

A user launches the application and wants flexibility in choosing their interface:
1. Startup screen presents clear choice: Terminal Interface (TUI) or Graphical Dashboard (GUI)
2. User can also bypass menu with command-line flags (--tui or --gui)
3. Selected interface launches with full functionality

**Why this priority**: Critical for usability - determines entire user experience path.

**Independent Test**: Startup menu selection flow and command-line flag handling.

**Acceptance Scenarios**:

1. **Given** user runs `python main.py`, **When** startup menu appears, **Then** user can select TUI or GUI.
2. **Given** user runs `python main.py --gui`, **When** no menu is shown, **Then** GUI launches directly.
3. **Given** invalid flag like `--invalid`, **When** provided, **Then** system shows help message and defaults to menu.

---

### User Story 5 - User Sees Live Convergence Visualizations (Priority: P2)

Users solving problems want to understand solver behavior visually:
1. Root finder shows error vs iteration curve on log scale
2. Linear systems show error decay or solution bar chart
3. Interpolation shows scatter plot + polynomial curve overlay
4. Integration shows curve with shaded area underneath

**Why this priority**: Enhances understanding and builds confidence in results; high UX value.

**Independent Test**: Plot generation for each solver type after computation.

**Acceptance Scenarios**:

1. **Given** root finder completes, **When** results are displayed, **Then** log-scale error curve is shown with tolerance threshold line.
2. **Given** linear system solution, **When** visualization is requested, **Then** solution vector bar chart or error curve is displayed.
3. **Given** interpolation data, **When** plot is generated, **Then** scatter points and polynomial curve are overlaid clearly.

---

### User Story 6 - User Exports Results for Analysis (Priority: P2)

Engineers want to save numerical results for documentation and further analysis:
1. After any solver completes, user is offered CSV export option
2. CSV includes step-by-step iteration data with all metrics (x_n, f(x_n), error, etc.)
3. File naming is automatic with method name prefix

**Why this priority**: Enables workflow continuity and documentation; moderate UX value.

**Independent Test**: CSV export workflow and file validation.

**Acceptance Scenarios**:

1. **Given** solver completes, **When** user selects "export to CSV", **Then** file is saved as `results_<method>_<timestamp>.csv`.
2. **Given** exported CSV, **When** opened in spreadsheet, **Then** all iteration steps are visible with proper column headers.

---

### Edge Cases

- What happens when user inputs invalid function syntax (e.g., "x^2++" for derivative)?
- How does system handle division by zero in Newton-Raphson?
- What occurs if user provides singular or near-singular matrix?
- How does GUI respond if solver times out (very large number of iterations)?
- What happens if user cancels operation mid-solve?
- How are floating-point precision errors handled in comparison operations?

## Requirements *(mandatory)*

### Functional Requirements

**Root Finding Solvers**:
- **FR-001**: System MUST support Newton-Raphson method with user-provided function, initial guess, tolerance, and max iterations
- **FR-002**: System MUST support Simple Iteration method with iteration formula and convergence tracking
- **FR-003**: System MUST detect divergence (error growing for 5+ consecutive iterations), continue to max_iter, flag result as diverged, and warn user
- **FR-004**: System MUST display iteration-by-iteration results showing x_n, f(x_n), error, and convergence status

**Linear System Solvers**:
- **FR-005**: System MUST support Gauss-Seidel method with matrix input, vector b, tolerance, and max iterations
- **FR-006**: System MUST support Jacobi method as alternative linear solver
- **FR-007**: System MUST automatically check diagonal dominance and reorder matrix rows if necessary to achieve dominance
- **FR-008**: System MUST warn user if matrix is singular or near-singular
- **FR-009**: System MUST support comparison mode running both Gauss-Seidel and Jacobi on identical input

**Calculus Solvers**:
- **FR-010**: System MUST support Newton's Divided Difference interpolation on provided (x,y) data points
- **FR-011**: System MUST support numerical integration using Trapezoidal and Simpson's rules
- **FR-012**: System MUST display interpolation polynomial coefficients and formula
- **FR-013**: System MUST support dynamic data point addition/modification with instant polynomial recalculation

**User Interfaces**:
- **FR-014**: System MUST provide Terminal Interface (TUI) with Rich formatting for readable tables and output
- **FR-015**: System MUST provide Graphical Interface (GUI) with CustomTkinter for dashboard-style problem solving
- **FR-016**: System MUST display live matplotlib convergence plots in GUI (error vs iteration, solution bars, interpolation curves, integration areas)
- **FR-017**: System MUST include method selector dropdown in GUI (Newton-Raphson vs Simple Iteration, Gauss-Seidel vs Jacobi vs Compare Both, Interpolation vs Integration)
- **FR-018**: System MUST include tolerance and max iterations input fields on all solver pages

**Application Startup**:
- **FR-019**: System MUST display startup menu allowing user to choose TUI or GUI on application launch
- **FR-020**: System MUST accept command-line flags `--tui` or `--gui` to bypass startup menu
- **FR-021**: System MUST show help message if invalid arguments provided

**Data Export**:
- **FR-022**: System MUST offer CSV export option after each solver completes
- **FR-023**: System MUST include all iteration step data in CSV (method-specific columns matching displayed tables)
- **FR-024**: System MUST use automatic naming convention: `results_<method>_<timestamp>.csv`

**Error Handling**:
- **FR-025**: System MUST validate all user inputs (syntax, bounds, singularity) with inline error messages (displayed below/next to the invalid field in GUI, or as console output in TUI)
- **FR-026**: System MUST handle solver timeouts gracefully with user cancellation option
- **FR-027**: System MUST catch and display mathematical errors (division by zero, invalid operations) with guidance

### Key Entities

- **Problem**: Engineering problem instance with selected solver type, input parameters, and solution
- **Solver Result**: Contains solution vector/root, iteration count, error history, convergence status, computation time
- **IterationStep**: Single iteration record with x_n, f(x_n), error, and method-specific metrics
- **Matrix**: Coefficient matrix with diagonal dominance check capability
- **DataPoint**: (x, y) pair for interpolation/integration with polynomial representation

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 7 solver methods (Newton-Raphson, Simple Iteration, Gauss-Seidel, Jacobi, Interpolation, Trapezoidal, Simpson's) successfully solve standard test problems with correct answers
- **SC-002**: Root finder achieves sub-tolerance convergence within advertised iteration count for test cases
- **SC-003**: Linear system solver produces solution vector accurate to 6+ decimal places for well-conditioned matrices
- **SC-004**: Interpolation polynomial passes through all 100% of provided data points (within floating-point precision)
- **SC-005**: Integration results match analytical solutions within 0.1% error for test cases
- **SC-006**: GUI plots render within 1 second of solver completion for problems up to 1000 iterations
- **SC-007**: CSV export produces valid, readable files with all iteration data intact and properly formatted
- **SC-008**: Startup menu and interface switching works reliably 100% of time with no errors
- **SC-009**: Divergence detection triggers correctly for unstable problem instances with user-friendly warnings
- **SC-010**: Terminal interface produces output readable and properly formatted for 80+ column terminals
- **SC-011**: GUI dashboard responsive to user input (dropdown selection, field editing, button clicks) with <500ms latency
- **SC-012**: System supports running comparison mode (method vs method) without performance degradation

## Assumptions

- Users have mathematical background sufficient to understand numerical methods concepts (iterative solvers, convergence, etc.)
- Input functions are provided in Python expression syntax (e.g., "x**2 - 4" for x²-4)
- Matrix input uses Python list format: [[1,2],[3,4]] for safe parsing via ast.literal_eval
- Diagonal dominance definition: |A[i,i]| > sum(|A[i,j]| for j≠i)
- Default tolerance for convergence: 1e-6; default max iterations: 100
- CSV export uses UTF-8 encoding and standard comma separators
- GUI window minimum size: 1280x800 for comfortable viewing of plots and controls
- Dark theme is default for GUI (light theme optional enhancement)
- All numerical computations use Python's float (double precision, ~15-16 decimal digits)
- No network/cloud dependencies - all computation is local and offline-capable
- Mobile support is out of scope for v1 (desktop only: Windows, macOS, Linux)
