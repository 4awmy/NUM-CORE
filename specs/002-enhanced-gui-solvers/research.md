# Research: Enhanced GUI, Auto-Solver Comparison, and Course-Complete Solver Suite

**Feature**: `002-enhanced-gui-solvers` | **Date**: 2026-05-03

---

## Decision 1: Live Equation Preview Rendering (FR-001)

**Decision**: Use matplotlib's built-in MathText renderer (`matplotlib.mathtext`) via a small embedded `FigureCanvasTkAgg` figure for the live preview.

**Rationale**:
- MathText handles standard math notation (superscripts, Greek letters, fractions, function names) without requiring a full LaTeX installation.
- The same matplotlib canvas infrastructure is already used throughout the project — no new dependencies.
- Renders `$x^2 + \sin(x)$` as styled math in real-time with a debounce delay.
- Alternative (unicode substitution) was rejected: cannot handle fractions, nested expressions, or function notation reliably.
- Alternative (full LaTeX render) was rejected: requires external LaTeX install, slow, adds setup friction for students.

**Implementation pattern**:
```python
# In EquationInputWidget
fig, ax = plt.figure(figsize=(4, 0.5)), ...
ax.text(0.5, 0.5, f"$f(x) = {normalized_expr}$", transform=ax.transAxes,
        ha='center', va='center', fontsize=12, color='white')
canvas = FigureCanvasTkAgg(fig, master=preview_frame)
```

**Alternatives considered**: PIL/Pillow rendering (no math support), tkinter `Label` with unicode (limited), web rendering (excessive dependency).

---

## Decision 2: Pure Black Matplotlib Theme (FR-010, FR-012)

**Decision**: Create a custom `.mplstyle` file (`numcore_black.mplstyle`) registered at app startup that sets all matplotlib backgrounds to `#000000` and text/axes to white/accent colors.

**Rationale**:
- `plt.style.use('dark_background')` produces dark gray (~#1c1c1c), not pure black.
- A custom style file gives precise control over every element: `figure.facecolor`, `axes.facecolor`, `axes.edgecolor`, `text.color`, `xtick.color`, `ytick.color`, `grid.color`.
- Registered once at startup via `matplotlib.style.core.USER_LIBRARY_PATHS` or `mpl.rcParams`.

**Key style parameters**:
```ini
figure.facecolor: #000000
axes.facecolor:   #000000
axes.edgecolor:   #444444
text.color:       #ffffff
xtick.color:      #aaaaaa
ytick.color:      #aaaaaa
grid.color:       #222222
lines.color:      #4fc3f7
```

**Alternatives considered**: `plt.style.use('dark_background')` (rejected: not pure black), per-figure rcParams overrides (harder to maintain consistently).

---

## Decision 3: Interactive Plot Zoom/Pan in CustomTkinter (FR-013)

**Decision**: Use `matplotlib.backends.backend_tkagg.FigureCanvasTkAgg` with `NavigationToolbar2Tk` embedded in a CTk frame.

**Rationale**:
- Standard Tkinter matplotlib backend works inside CTk since CTk is built on top of Tkinter.
- `NavigationToolbar2Tk` provides Home, Pan, Zoom, Save buttons out of the box.
- No additional libraries needed.
- The toolbar can be styled to match the black theme by setting its background color after initialization.

**Implementation pattern**:
```python
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
toolbar = NavigationToolbar2Tk(canvas, plot_frame, pack_toolbar=False)
toolbar.configure(background="#000000")
toolbar.update()
toolbar.pack(side=tk.BOTTOM, fill=tk.X)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
```

**Alternatives considered**: plotly (requires a web server or browser, too heavy), bokeh (same issue), pyqtgraph (requires PyQt dependency, conflicts with CTk).

---

## Decision 4: Auto-Solver Comparison Architecture (FR-005–009)

**Decision**: A `ComparisonRunner` class in `numcore_engine/comparison.py` that accepts a problem dict and a list of instantiated `Solver` objects, runs each solver, collects results, and returns a `ComparisonResult` model.

**Rationale**:
- Keeps comparison logic in the engine layer (Engine-First constitution principle).
- The GUI/TUI simply call `ComparisonRunner.run(solvers, problem)` and receive a unified result.
- Each `Solver` is instantiated with its method-specific parameters before passing to the runner.
- The runner determines the "best method" by fewest iterations among converged solvers.
- Diverged solvers are included in output with `converged=False` flag — not hidden.

**Input consolidation strategy for GUI**:
- Show a superset input form: interval `[a, b]` AND initial guess `x₀` simultaneously.
- `ComparisonRunner` passes `a, b` only to Bisection; passes `x₀` only to Newton/Simple Iteration; passes both `x₀, x₁` to Secant.
- Chapter-specific wrapper functions (`chapter_1_compare()`) handle this routing.

**Alternatives considered**: Having each chapter page run solvers independently (rejected: duplicates comparison logic in UI layer, violates Engine-First principle).

---

## Decision 5: Convergence Check Display for Simple Iteration (FR-021)

**Decision**: Compute `|g′(x₀)|` symbolically using sympy at solve time and include it in `SimulationData.metadata` as `{"convergence_check": value, "convergence_check_passed": bool}`. The formatter and GUI display this above the iteration table.

**Rationale**: Lecturer methodology requires showing the convergence check before iteration begins. Computing it symbolically is consistent with how Newton-Raphson already uses sympy for derivatives. If `|g′(x₀)| ≥ 1`, the solver still runs (user chose to proceed) but flags `convergence_check_passed=False` with a warning.

---

## Decision 6: Divided Difference Table Storage (FR-025)

**Decision**: Store the full 2D divided difference table as a nested list in `SimulationData.metadata["dd_table"]` — rows are data points, columns are difference orders. The formatter reconstructs the triangular display from this.

**Rationale**: The `SimulationData` model already supports arbitrary metadata. Storing the table as a 2D list is portable (works for both Rich TUI tables and CTk GUI tables). The triangular display is a formatting concern, not a data model concern.

---

## Decision 7: Post-Week 10 Solver Delivery (FR-044–047)

**Decision**: Post-Week 10 solvers (Gaussian Quadrature, Numerical Differentiation, Curve Fitting, ODE solvers) are engine-implemented but exposed only via TUI in Phase I. GUI pages for these remain as placeholder pages with a "Coming Soon" label.

**Rationale**: Avoids delaying the core MVP (Weeks 1–10 GUI) while keeping the implementation timeline realistic. Constitution Principle III (Dual Interface Parity) is formally deferred for these solvers, documented in the Constitution Check deviation table.
