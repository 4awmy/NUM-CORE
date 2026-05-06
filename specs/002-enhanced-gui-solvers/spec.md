# Feature Specification: Enhanced GUI, Auto-Solver Comparison, and Course-Complete Solver Suite

**Feature Branch**: `002-enhanced-gui-solvers`
**Created**: 2026-05-03
**Status**: Draft
**Input**: GUI enhancements, auto-solver comparison, black theme, equation input UX, lecturer-methodology compliance, and course-complete solver suite through Week 10 (post-Week 10 methods added later via TUI)

## Clarifications

### Session 2026-05-03

- Q: What visual style of equation input should the GUI provide? → A: Smart text field with live preview — user types in a single text box using standard notation (e.g., `x^2 + sin(x)`); a formatted preview renders below the field in styled math notation (e.g., x² + sin(x)). Input stays as text; preview is display-only.
- Q: Does the auto-solver comparison mode apply to all chapters (root finding, linear systems, interpolation, integration) or only root finding? → Assumption: applies to any chapter where ≥2 methods solve the same problem type; each chapter page includes an "Auto-Compare All Methods" action.
- Q: What should happen to Simple Iteration in auto-compare mode (it requires a separate g(x) formula)? → A: Replace "Auto-Compare" with a **Smart Solver** mode that runs all applicable methods automatically, compares their performance, and explains *why* it recommends the winner (e.g., "Newton-Raphson converged in 4 iterations vs Bisection's 23. Recommended: fast convergence for smooth, differentiable functions"). For Simple Iteration, the Smart Solver either auto-derives g(x) from f(x) symbolically where possible, or excludes it with a note explaining why.
- Q: What should the Smart Solver recommendation panel show when every method diverges (no winner)? → A: Show a **diagnostic panel** listing the likely cause per method and actionable suggestions to fix inputs (e.g., "Bisection: f(a)·f(b) > 0 — root may not be in [a,b]; try wider interval. Newton-Raphson: derivative near zero — try a different x₀."). No blank panel or silent failure.
- Q: How should lecturer-format compliance (SC-003) be verified in tests? → A: **Automated unit test assertions** on exact column names and formula correctness per method (e.g., assert Bisection step data keys == {n, a, b, c, f_a, f_b, f_c, error} and error value == |b−a|/2). No manual review required for CI.
- Q: Is the programming language fixed to Python, or can it change if a different language produces better graphics and solving performance? → A: **Language change is permitted** if it demonstrably improves graphics quality or solver performance. The architecture (engine-first, dual interface, protocol-driven contracts) must be preserved regardless of language choice.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Equation Input via Visual Interface (Priority: P1)

A student needs to enter a mathematical equation (e.g., x³ − 7x² + 14x − 6 = 0) into the solver. Currently, raw Python expression strings are error-prone and unfamiliar. The user wants a clean, visual input experience where they can type or construct the equation naturally and see a rendered preview before solving.

**Why this priority**: Equation input is the entry point to every solver. If it is hard to use, the entire application fails. This is the single most impactful UX improvement.

**Independent Test**: A user with no programming background can enter `x^3 - 7x^2 + 14x - 6 = 0` using the input interface and see it rendered correctly as a formatted equation before clicking Solve.

**Acceptance Scenarios**:

1. **Given** user opens any chapter solver page, **When** they type a mathematical expression using standard notation (e.g., `x^2`, `sin(x)`, `e^x`), **Then** a live preview renders the expression in formatted mathematical notation below the input field.
2. **Given** user enters an invalid expression (e.g., `x^^2`), **When** they attempt to solve, **Then** an inline error appears explaining the syntax issue with a correction hint.
3. **Given** the user has entered a valid equation, **When** they click Solve, **Then** the expression is correctly parsed and passed to the selected solver without additional transformation by the user.

---

### User Story 2 — Smart Solver Mode (Priority: P1)

A student has an equation and wants the application to automatically determine the best solution method. They click "Smart Solve", the system runs all applicable methods for the chapter, compares their performance, and presents a recommendation panel explaining *why* the winning method is best — in plain language tied to the method's mathematical properties (e.g., "Newton-Raphson: fastest convergence for smooth differentiable functions").

**Why this priority**: This is the core learning differentiator — it doesn't just give answers, it teaches *which method to use and why*, directly mirroring exam-level reasoning. It replaces the need for a separate "Compare All Methods" button with a smarter, guided experience.

**Independent Test**: User enters `f(x) = x³ − 2x² − 5` with interval [2, 3] in the root-finding chapter and clicks "Smart Solve". All applicable methods run. A recommendation card appears: "✓ Recommended: Newton-Raphson (4 iterations, error 1.2e-8). Fastest convergence for smooth differentiable functions. Bisection: 23 iterations. Secant: 6 iterations." Simple Iteration is either included or listed as "Excluded: could not derive convergent g(x) automatically."

**Acceptance Scenarios**:

1. **Given** user has entered valid inputs on any chapter page, **When** they click "Smart Solve", **Then** all applicable solvers for that chapter run automatically on the same input without further configuration.
2. **Given** Smart Solve completes, **When** the recommendation panel appears, **Then** it states: (a) the recommended method name, (b) its iteration count and final error, (c) a 1–2 sentence plain-language explanation of why this method is best for this problem type.
3. **Given** the comparison table is shown, **When** user inspects it, **Then** each row shows method name, iterations, final error, convergence status, and solution value — with the recommended method visually highlighted.
4. **Given** a method diverges during Smart Solve, **When** results display, **Then** its row shows "Diverged" with a brief actionable note (e.g., "Try a closer initial guess") and the remaining methods' results are unaffected.
5. **Given** Simple Iteration is in scope (Chapter 1), **When** Smart Solve runs, **Then** the engine attempts to derive a convergent g(x) symbolically; if successful it is included; if not, its row reads "Excluded — g(x) could not be auto-derived. Use manual mode to provide g(x)."
6. **Given** Smart Solve completes, **When** user clicks any method row, **Then** the full lecturer-format result table for that method expands inline below the comparison panel.

---

### User Story 3 — True Black Theme and Enhanced Visual Design (Priority: P1)

A student uses the application in a dark environment (lab, night study). The current dark theme uses dark gray, which causes eye strain and looks unprofessional. They want a true pure-black UI (#000000 background) with high-contrast text and sharp visual hierarchy.

**Why this priority**: Visual quality affects perceived value and sustained usability. Pure black theme is also required for high-contrast accessibility and OLED display efficiency.

**Independent Test**: Launch the application and measure that the main window background, sidebar, and all panel backgrounds use pure black (#000000), not gray variants. All text is legible at minimum 4.5:1 contrast ratio.

**Acceptance Scenarios**:

1. **Given** the application launches, **When** any page is active, **Then** all background surfaces render as pure black (not dark gray), with accent colors and text providing clear contrast.
2. **Given** a plot is rendered, **When** displayed in the GUI, **Then** the plot background is also black, with white/colored axes, labels, and curves that are clearly readable.
3. **Given** buttons, dropdowns, and input fields, **When** rendered on the black background, **Then** they are visually distinct and clearly identifiable as interactive elements.

---

### User Story 4 — Enhanced Solver Result Plots (Priority: P1)

After running a solver, a student wants to see rich, informative visualizations that match the type of problem being solved — not just a basic line chart. They want interactive plots (zoom, pan), proper mathematical labeling, and visual elements that reflect the lecturer's methodology (e.g., showing the bisection interval narrowing, the Newton-Raphson tangent line, the divided difference table visualization).

**Why this priority**: Visual feedback is critical for learning numerical methods. Rich plots make abstract convergence concepts concrete.

**Independent Test**: After running Bisection on `f(x) = x³ − 7x² + 14x − 6`, the plot shows the function curve, the interval brackets narrowing per iteration, and the final root marked — all on a black background with clear labels.

**Acceptance Scenarios**:

1. **Given** root-finding solver completes, **When** plot renders, **Then** function curve is displayed over the domain, root is marked with a distinct point, and convergence error-vs-iteration chart is shown on log scale.
2. **Given** interpolation solver completes, **When** plot renders, **Then** scatter data points and the interpolating polynomial curve are overlaid with a legend distinguishing them.
3. **Given** integration solver completes, **When** plot renders, **Then** the area under the curve is shaded and the computed integral value is annotated on the plot.
4. **Given** any plot, **When** rendered, **Then** the user can zoom and pan interactively within the plot canvas.

---

### User Story 5 — Lecturer Methodology Compliance in Results Display (Priority: P1)

A student needs to verify their solver results against what the lecturer shows on the board. The result tables and step displays must exactly match the lecturer's required format per method — correct column names, correct error formulas, correct intermediate values shown.

**Why this priority**: The primary use case is academic exam preparation. If results don't match the lecturer's format, the tool has zero value for study.

**Independent Test**: Run Bisection on `f(x) = x³ − 7x² + 14x − 6` on [1,2] and verify the result table shows columns: n | a | b | c | f(a) | f(b) | f(c) | Error — with Error calculated as |b−a|/2, matching the lecturer's methodology document exactly.

**Acceptance Scenarios**:

1. **Given** Bisection solver runs, **When** results are displayed, **Then** table shows columns [n, a, b, c, f(a), f(b), f(c), Error] where Error = |b−a|/2 exactly.
2. **Given** Simple Iteration solver runs, **When** results are displayed, **Then** convergence check |g′(x)| < 1 is shown before iteration table, with a warning if condition is not met.
3. **Given** Newton-Raphson solver runs, **When** results are displayed, **Then** f(x) and f′(x) values are shown per iteration, with the recommended x₀ selection criterion (f(x₀)·f″(x₀) > 0) displayed.
4. **Given** any linear systems solver runs, **When** results are displayed, **Then** the diagonal dominance verification is shown first with pass/fail status per row before the iteration table.
5. **Given** Newton's Divided Difference interpolation runs, **When** results are displayed, **Then** the full triangular divided difference table is shown with all intermediate values visible.
6. **Given** any integration solver runs, **When** results are displayed, **Then** step size h is stated, x/y value table is shown, and the weighted-sum formula is written out before the final result.

---

### User Story 6 — Complete Course Solver Suite Through Week 10 (Priority: P2)

A student needs to solve problems from any lecture up to Week 10. The application must support every method taught in the course through that point, so they can check homework and prepare for exams across all covered topics.

**Why this priority**: Academic completeness up to the exam scope. Post-Week 10 methods are lower priority and will be added in a subsequent phase.

**Independent Test**: A student can open the application and find working solvers for: Bisection, Secant (Week 1), Simple Iteration, Newton-Raphson (Week 5), Jacobi, Gauss-Seidel (Week 6), Lagrange Interpolation (Week 7), Newton Forward/Backward Difference, Newton Divided Difference (Week 9), Composite Trapezoidal, Composite Midpoint, Composite Simpson's 1/3 and 3/8 (Week 10).

**Acceptance Scenarios**:

1. **Given** user opens Chapter 1 (Root Finding), **When** they use the method selector, **Then** all four methods are available: Bisection, Secant, Newton-Raphson, Simple Iteration.
2. **Given** user opens Chapter 3 (Interpolation), **When** they select an interpolation method, **Then** Lagrange, Newton Forward Difference, Newton Backward Difference, Newton Forward Divided Difference, and Newton Backward Divided Difference are all available.
3. **Given** user opens Chapter 4 (Integration), **When** they select an integration method, **Then** Composite Trapezoidal, Composite Midpoint, Composite Simpson's 1/3 Rule, and Composite Simpson's 3/8 Rule are all available.
4. **Given** user solves a Week 10 integration problem (e.g., ∫x ln(x) dx on [1,2] with n=4), **When** results display, **Then** answer matches analytical solution within 0.1% error.

---

### User Story 7 — Post-Week 10 Solvers via TUI (Priority: P3)

After the core GUI is complete, a student using the terminal interface wants to access advanced methods from Weeks 12–15: Gaussian Quadrature, Numerical Differentiation, Curve Fitting (regression), and ODE solvers (Taylor Series, Runge-Kutta 4, Modified Euler).

**Why this priority**: These are future-semester content; the GUI is the primary interface. TUI serves power users and those working without a graphical environment.

**Independent Test**: User runs `python main.py --tui` and navigates to find Gaussian Quadrature (Week 12) and Runge-Kutta 4 (Week 15) available in the method list.

**Acceptance Scenarios**:

1. **Given** user launches TUI, **When** they navigate to Chapter 4 advanced methods, **Then** Gaussian 2-point and 3-point quadrature solvers are accessible and functional.
2. **Given** user selects Curve Fitting in TUI, **When** they provide (x,y) data points, **Then** linear regression, quadratic regression, and linearization variants (power, exponential, growth) are available.
3. **Given** user selects ODE solvers in TUI, **When** they input an initial value problem y′ = f(x,y) with y(x₀) = y₀, **Then** Taylor Series Order 4, Runge-Kutta 4, and Modified Euler methods are all available.

---

### Edge Cases

- What happens when user enters `x^2` notation vs `x**2` — are both accepted in the equation input?
- How does auto-compare handle methods with different required inputs (e.g., Bisection needs [a,b]; Newton needs only x₀)?
- What if convergence check fails for Simple Iteration (|g′(x)| ≥ 1) — does the solver still run?
- What happens if n is odd when Simpson's 1/3 Rule (requires even n) is selected?
- What happens if n is not a multiple of 3 for Simpson's 3/8 Rule?
- How does the divided difference table display for large datasets (>10 points)?
- What if the user provides an interpolation equation with coincident x values?
- What if all methods diverge in Smart Solve? → Diagnostic panel shown with per-method cause and fix suggestions (not a blank or generic error).
- How does the plot behave for high-iteration solvers (1000+ points) — performance?

---

## Requirements *(mandatory)*

### Functional Requirements

**Equation Input UX**:
- **FR-001**: System MUST provide a visual equation input field that accepts standard mathematical notation (e.g., `x^2`, `sin(x)`, `e^x`, `ln(x)`) and renders a formatted preview of the expression in real-time
- **FR-002**: System MUST accept both `^` (caret) and `**` (double-star) notation for exponents and normalize internally
- **FR-003**: System MUST display inline syntax error messages with correction hints when invalid expressions are entered
- **FR-004**: System MUST provide a symbol/function reference panel or toolbar listing available mathematical functions (sin, cos, tan, exp, ln, sqrt, etc.) that inserts them into the input field on click

**Smart Solver Mode**:
- **FR-005**: System MUST provide a "Smart Solve" button on every chapter solver page that automatically runs all applicable methods for the chapter on the same input in one click
- **FR-006**: System MUST display a unified comparison table showing per-method: solution value, iterations, final error, convergence status (converged/diverged/max_iterations), and computation time
- **FR-007**: System MUST display a recommendation panel above the comparison table: (a) if ≥1 method converged — identify the best method with a 1–2 sentence plain-language explanation; (b) if all methods diverged — show a diagnostic panel listing the likely cause per method and specific actionable suggestions (e.g., "Newton-Raphson: derivative near zero — try a different x₀")
- **FR-008**: System MUST visually highlight the recommended method row in the comparison table with a distinct accent (border, color, or badge)
- **FR-009**: System MUST show diverged methods in the comparison table with a "Diverged" flag and a brief actionable hint — never hide them
- **FR-048**: System MUST attempt to auto-derive a convergent g(x) for Simple Iteration when Smart Solve is triggered; if derivation fails, Simple Iteration row MUST display "Excluded — provide g(x) manually" rather than erroring
- **FR-049**: System MUST allow the user to click any method row in the Smart Solve comparison table to expand the full lecturer-format iteration table for that method inline

**Visual Theme**:
- **FR-010**: System MUST use pure black (#000000) as the background color for the main window, sidebar, all content panels, and all plot canvas backgrounds
- **FR-011**: System MUST use a consistent accent color scheme with minimum 4.5:1 contrast ratio between text and background across all UI elements
- **FR-012**: Solver result plots MUST render on a black background with colored axes, curves, and labels

**Enhanced Plotter**:
- **FR-013**: All result plots MUST support interactive zoom and pan within the embedded plot canvas
- **FR-014**: Root-finding plots MUST show the function curve over the computed domain, mark the root, and show convergence error on a log-scale chart
- **FR-015**: Bisection plots MUST additionally show the interval [a,b] narrowing animation or step-by-step bracket markers
- **FR-016**: Newton-Raphson plots MUST show tangent line(s) at iteration points illustrating the tangent method visually
- **FR-017**: Integration plots MUST shade the area under the curve and annotate the computed integral value
- **FR-018**: Interpolation plots MUST overlay the polynomial curve on scatter data points with a legend
- **FR-019**: Comparison mode plots MUST overlay all method error curves on one chart with distinct colors per method and a clear legend

**Lecturer Methodology Compliance**:
- **FR-020**: Bisection result table MUST use columns [n, a, b, c, f(a), f(b), f(c), Error] where Error = |b−a|/2
- **FR-021**: Simple Iteration MUST display the convergence condition check |g′(x)| < 1 at the head of results, evaluated at the initial guess, with a pass/fail indicator and warning if divergence is predicted
- **FR-022**: Newton-Raphson MUST display the initial guess recommendation check (f(x₀)·f″(x₀) > 0) in results; show f(xₙ) and f′(xₙ) columns per iteration
- **FR-023**: Linear system solvers MUST display the Strictly Diagonal Dominant (SDD) verification matrix before iteration tables, with per-row pass/fail status
- **FR-024**: Jacobi results MUST label updates as "simultaneous"; Gauss-Seidel results MUST label updates as "successive" with a visible distinction
- **FR-025**: Newton's Divided Difference result MUST display the full triangular divided difference table with all intermediate values, using the layout: x₀ | y₀ | 1st DD | 2nd DD | ...
- **FR-026**: All integration solvers MUST display: (1) step size h = (b−a)/n, (2) x/y value table, (3) the weighted-sum formula expanded with actual values, (4) the final integral result
- **FR-027**: Simpson's 1/3 Rule MUST validate that n is even before solving and display an inline error if n is odd
- **FR-028**: Simpson's 3/8 Rule MUST validate that n is a multiple of 3 before solving and display an inline error if not

**Course Solver Completeness — MVP (Through Week 10)**:
- **FR-029**: System MUST implement Bisection solver (Week 1) with bracket-narrowing approach
- **FR-030**: System MUST implement Secant solver (Week 1) requiring two initial points x₀ and x₁
- **FR-031**: System MUST implement Simple Iteration / Fixed-Point solver (Week 5) accepting iteration formula g(x)
- **FR-032**: System MUST implement Newton-Raphson solver (Week 5) with automatic symbolic derivative computation
- **FR-033**: System MUST implement Jacobi iterative linear solver (Week 6)
- **FR-034**: System MUST implement Gauss-Seidel iterative linear solver (Week 6)
- **FR-035**: System MUST implement Lagrange Interpolation solver (Week 7)
- **FR-036**: System MUST implement Newton Forward Difference interpolation (Week 9)
- **FR-037**: System MUST implement Newton Backward Difference interpolation (Week 9)
- **FR-038**: System MUST implement Newton Forward Divided Difference interpolation (Week 9)
- **FR-039**: System MUST implement Newton Backward Divided Difference interpolation (Week 9)
- **FR-040**: System MUST implement Composite Trapezoidal Rule integration (Week 10)
- **FR-041**: System MUST implement Composite Midpoint Rule integration (Week 10)
- **FR-042**: System MUST implement Composite Simpson's 1/3 Rule integration (Week 10)
- **FR-043**: System MUST implement Composite Simpson's 3/8 Rule integration (Week 10)

**Post-Week 10 Solvers — TUI Phase (Future)**:
- **FR-044**: System MUST implement Gaussian 2-point and 3-point Quadrature via TUI (Week 12)
- **FR-045**: System MUST implement Numerical Differentiation (2-point, 3-point endpoint, 3-point midpoint) via TUI (Week 13)
- **FR-046**: System MUST implement Curve Fitting: linear regression, quadratic regression, and linearization (power, exponential, growth functions) via TUI (Week 14)
- **FR-047**: System MUST implement ODE solvers: Taylor Series Order 4, Runge-Kutta 4th Order, and Modified Euler via TUI (Week 15)

### Key Entities

- **Equation**: User-entered mathematical expression, normalized to an internal callable form; has raw string, display-rendered form, and parsed callable
- **SolverResult**: Output from a single solver run; contains solution value, iteration steps, error history, convergence status, diverged flag, method metadata
- **ComparisonResult**: Collection of SolverResults for the same input across multiple methods; includes best-method designation
- **IterationStep**: Single iteration record with method-specific columns (varies by solver type per lecturer format)
- **DividedDifferenceTable**: Triangular table of divided difference values for Newton interpolation display
- **IntegrationTable**: Step-size h, x/y value table, and weighted-sum breakdown for integration display

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user with no programming background can enter a standard exam equation (e.g., x³ − 7x² + 14x − 6 = 0) and receive a correctly formatted result table matching the lecturer's methodology in under 2 minutes
- **SC-002**: Auto-compare mode runs all applicable methods for a given chapter and displays unified results within 3 seconds for problems up to 500 iterations per method
- **SC-003**: All result tables pass automated unit test assertions verifying exact column names and formula correctness per method (e.g., Bisection error column = |b−a|/2; Newton-Raphson columns include f(xₙ) and f′(xₙ); integration output includes h, x/y table, and weighted-sum string). 100% of these assertions pass with zero failures.
- **SC-004**: All 15 MVP solvers (Weeks 1–10) produce correct answers matching analytical solutions within 0.1% error on the standard course test problems
- **SC-005**: All plots render on a pure black background with clearly readable labels and curves; all background panel surfaces measure #000000
- **SC-006**: Interactive plot features (zoom, pan) respond within 200ms of user gesture
- **SC-007**: Equation input field renders a live preview of the entered expression within 300ms of keystroke
- **SC-008**: Inline error messages for invalid inputs appear within 500ms and include a correction hint specific to the error type
- **SC-009**: Smart Solver correctly identifies the best-performing method (fewest iterations among converged) in 100% of test cases where a clear winner exists, and displays a non-empty recommendation explanation for every supported method type
- **SC-010**: All post-Week 10 solvers (Weeks 12–15) are accessible and functional via TUI, producing results matching course test problems within 0.1% error

---

## Assumptions

- Primary interface is GUI for MVP (through Week 10); TUI is the delivery vehicle for post-Week 10 methods
- **Programming language is not fixed** — if a different language delivers meaningfully better graphics quality or numerical solver performance, migration is permitted. The engine-first architecture, protocol-driven solver contracts, and dual-interface structure must be preserved regardless of language. Language choice is a planning-phase decision.
- "True black" is defined as #000000 RGB for all background surfaces; accent colors (e.g., electric blue, orange) provide interactive element contrast
- Standard mathematical notation accepted: `^` for exponent, `sin()`, `cos()`, `tan()`, `exp()`, `ln()`, `log()`, `sqrt()`, `pi`, `e` as constants
- Equation input renders preview as formatted text notation (e.g., x² displayed) — not a full LaTeX PDF renderer
- Auto-compare for root finders collects interval [a,b] AND initial guess x₀ in a single input form, using [a,b] for Bisection/Secant and x₀ for Newton/Simple Iteration
- g(x) for Simple Iteration must still be manually provided by the user (the system cannot automatically derive a convergent iteration formula)
- Lecturer methodology tables are the primary result display; a summary line (root/solution value) is shown above the table
- Post-Week 10 TUI solvers are out of scope for the GUI phase; GUI pages for those chapters remain placeholders
- All computation remains local and offline-capable
- Platform: Desktop — Windows, macOS, Linux; no mobile support
- Default tolerance: 1e-6; default max iterations: 100
