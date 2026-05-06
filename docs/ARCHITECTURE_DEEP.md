# NUM-CORE: Deep Architecture Reference

This document explains the structural design, package layout, and key design decisions of the NUM-CORE project.

---

## 1. Guiding Principles

| Principle | How it's enforced |
|---|---|
| **Separation of concerns** | `numcore_engine` has zero imports from `numcore_cli` or `numcore_gui` |
| **Interface-driven solvers** | All solvers implement the `Solver` protocol from `interfaces.py` |
| **Symbolic-first input** | User strings go through `SymbolicParser` before any numerical work |
| **Traceable computation** | Every iteration is recorded as an immutable `NumericalStep` |
| **Immutable data transfer** | `NumericalStep` and `SimulationData` are frozen dataclasses |

---

## 2. Package Layout

```
NUM-CORE/
│
├── numcore_engine/               ← Pure math layer. No UI.
│   ├── __init__.py
│   ├── interfaces.py             ← Solver protocol definition
│   ├── models.py                 ← NumericalStep, SimulationData, ComparisonResult
│   ├── parser.py                 ← SymbolicParser (SymPy wrapper)
│   └── solvers/
│       ├── __init__.py
│       ├── root_finder.py        ← Bisection, Newton-Raphson, Secant, Simple Iteration
│       ├── network_solver.py     ← Jacobi, Gauss-Seidel, NetworkSolver (wrapper)
│       ├── calculus_engine.py    ← Differentiation, Integration, Interpolation
│       └── comparison.py        ← ComparisonRunner (runs multiple solvers, picks best)
│
├── numcore_cli/                  ← Terminal UI (Rich library)
│   ├── __init__.py
│   ├── terminal.py               ← Interactive menu system and user input loop
│   └── formatter.py              ← Converts NumericalStep lists into Rich tables
│
├── numcore_gui/                  ← Desktop GUI (CustomTkinter + Matplotlib)
│   ├── __init__.py
│   ├── dashboard.py              ← Main window, sidebar navigation, status bar
│   ├── visualization.py          ← PlotManager: Matplotlib embedded in CTk frames
│   ├── equation_input.py         ← EquationInputWidget: live preview + validation
│   ├── result_panel.py           ← ResultPanel: scrollable step table + summary
│   ├── smart_solver_panel.py     ← Comparison popup panel
│   ├── help_system.py            ← Tooltip and info popup system
│   ├── theme.py                  ← Color constants (BLACK, PANEL, ACCENT_BLUE, ...)
│   ├── styles/
│   │   └── numcore_black.mplstyle
│   └── pages/
│       ├── root_finder_page.py
│       ├── network_solver_page.py
│       ├── calculus_page.py
│       ├── interpolation_page.py
│       ├── chapter_1_app.py      ← Beam Stress practical application
│       ├── chapter_2_app.py      ← Circuit Analysis practical application
│       ├── chapter_3_app.py
│       └── chapter_4_app.py      ← Projectile Trajectory practical application
│
├── tests/
│   ├── unit/                     ← Per-solver accuracy tests (pytest)
│   └── integration/              ← CLI/GUI data flow tests
│
├── matlab/                       ← Original MATLAB reference implementations
├── specs/                        ← Spec-Kit SDD artifacts
├── docs/                         ← Documentation (this file lives here)
└── main.py                       ← Entry point (launches CLI or GUI)
```

---

## 3. The Solver Protocol (`interfaces.py`)

Every solver in the engine implements this `typing.Protocol`:

```python
class Solver(Protocol):
    def solve(self, **kwargs: Any) -> SimulationData:
        """Run the algorithm and return final results."""

    def get_steps(self) -> List[NumericalStep]:
        """Return the full iteration history for educational display."""

    def validate_input(self, **kwargs: Any) -> bool:
        """Pre-check inputs before running (missing fields, sign conditions, etc.)."""
```

`typing.Protocol` (structural subtyping) was chosen over `abc.ABC` because:
- No inheritance required — any class with matching methods qualifies
- Easier to test with mock objects
- More flexible when wrapping third-party solvers

All three methods are always called in order: `validate_input → solve → get_steps`.

---

## 4. Data Model (`models.py`)

```
NumericalStep (frozen dataclass)
  ├── step_idx  : int               # 0-based iteration number
  ├── value     : float             # current best approximation (x or error)
  ├── error     : Optional[float]   # convergence error at this step
  └── details   : Dict[str, Any]    # solver-specific: {a, b, f(a), f(b), c, f(c)}
                                    # or {x_n, f(x), f'(x)} for N-R, etc.

SimulationData (frozen dataclass, extends NumericalData)
  ├── title     : str               # display name e.g. "Bisection Convergence"
  ├── x_data    : List[float]       # x-axis: usually iteration numbers
  ├── y_data    : List[float]       # y-axis: usually the approximations
  └── metadata  : Dict[str, Any]    # root, iterations, converged, diverged,
                                    # sdd_check, polynomial_str, etc.

ComparisonResult (frozen dataclass)
  ├── best_method  : Optional[str]  # name of the fastest-converging method
  ├── results      : List[NumericalData]
  ├── recommendation : str
  └── all_diverged : bool
```

Using **frozen dataclasses** means:
- Safe to pass across layers — the UI cannot accidentally mutate engine results
- Hashable — can be stored in sets or used as dict keys
- Clear, typed fields with IDE autocomplete

---

## 5. The Parser Layer (`parser.py`)

`SymbolicParser` is a static-method utility class wrapping SymPy. It is the **only place** in the entire codebase where a user's raw string becomes executable code.

```
"x^2 - sin(x)"
      │
      ▼  normalize()
"x**2 - sin(x)"     (^ → **, ln → log)
      │
      ▼  sympy.sympify()
SymPy expression tree
      │
      ├──▶ validate()     → bool (checks for free symbols, parse errors)
      ├──▶ get_symbols()  → ["x"]
      ├──▶ get_derivative() → "2*x - cos(x)"  (symbolic, via sympy.diff)
      └──▶ parse_expression() → Python callable f(x)  (via sympy.lambdify)
```

`sympy.lambdify` converts the expression tree into a NumPy-backed Python function, so the solver's inner loop calls plain `f(x_n)` at native speed — no string evaluation in the hot path.

---

## 6. Data Flow (End-to-End)

```
[User] types "x**3 - 2*x**2 - 5", sets x0=1, tol=1e-4
        │
        │  (CLI: terminal.py reads input())
        │  (GUI: EquationInputWidget.get_expression(), CTkEntry.get())
        ▼
[Validation Layer]
   SymbolicParser.validate(expression)    ← rejects bad syntax immediately
        │
        ▼
[Solver Instantiation]
   solver = NewtonRaphsonSolver()         ← one instance per page (pre-created)
        │
        ▼
[Solver.solve(**kwargs)]
   1. SymbolicParser.parse_expression()  → f callable
   2. SymbolicParser.get_derivative()    → df callable (or numerical fallback)
   3. Iteration loop:
        x_next = x_n - f(x_n) / df(x_n)
        step   = NumericalStep(i, x_next, error, {x_n, f(x), f'(x)})
        self._steps.append(step)
   4. Returns SimulationData
        │
        ▼
[Output Fork]
   ┌────────────────┬──────────────────────────────┐
   │ CLI            │ GUI                          │
   │ formatter.py   │ result_panel.update_result() │
   │ Rich table     │ PlotManager.plot_...()       │
   └────────────────┴──────────────────────────────┘
```

---

## 7. Solver Instances in the GUI

Each GUI page pre-creates solver instances at construction time (`root_finder_page.py:227`):

```python
self.solvers = {
    "Newton-Raphson":  NewtonRaphsonSolver(),
    "Bisection":       BisectionSolver(),
    "Secant":          SecantSolver(),
    "Simple Iteration": SimpleIterationSolver()
}
```

The same instance is reused on every button click — `self._steps` is reset at the start of each `solve()` call, so there is no state leak between runs.

---

## 8. The Comparison Runner (`comparison.py`)

`ComparisonRunner` wraps a dict of solvers and runs all of them on the same input. It:

1. Calls `solver.validate_input(**kwargs)` for each solver — skips those that can't handle the input (e.g. Bisection needs `a` and `b`; if they're absent it's skipped)
2. Runs `solver.solve(**kwargs)` inside a `try/except` for each
3. Compares results by: `converged` flag → number of iterations → final error
4. Returns a `ComparisonResult` with the best method identified

Used by the GUI's **"Smart Solve (Compare)"** button, which displays a `SmartSolverPanel` popup showing all methods side by side.

---

## 9. Why `typing.Protocol` over `abc.ABC`

```python
# With abc.ABC — forces inheritance:
class BisectionSolver(ABC, Solver):  # must explicitly inherit
    ...

# With typing.Protocol — structural:
class BisectionSolver:               # no inheritance needed
    def solve(self, **kwargs): ...   # just needs matching methods
    def get_steps(self): ...
    def validate_input(self, **kwargs): ...
# Python automatically treats this as satisfying Solver
```

This means external or mock solvers can be plugged into the `ComparisonRunner` without modifying any base class.

---

## 10. Extension: Adding a New Solver

To add a new numerical method to the full stack:

1. **Engine** — create `numcore_engine/solvers/my_method.py`:
   ```python
   class MySolver:
       def __init__(self): self._steps = []
       def solve(self, **kwargs) -> SimulationData: ...
       def get_steps(self) -> List[NumericalStep]: return self._steps
       def validate_input(self, **kwargs) -> bool: ...
   ```

2. **Export** — add it to `numcore_engine/solvers/__init__.py`

3. **GUI** — create `numcore_gui/pages/my_method_page.py` with a `ctk.CTkFrame` subclass

4. **Dashboard** — register the page in `numcore_gui/dashboard.py` sidebar

5. **CLI** — add a menu entry in `numcore_cli/terminal.py`

6. **Tests** — add `tests/unit/test_my_method.py` with known-answer test cases
