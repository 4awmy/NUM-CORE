# NUM-CORE: GUI Input Flow — From Keypress to Plot

This document traces the complete path of user input through the GUI layer down into the engine and back out as a rendered result.

---

## 1. High-Level Overview

```
User types equation + parameters
           │
           ▼
  EquationInputWidget        ← validates & previews live
           │
           ▼
  RootFinderPage.solve_action()  ← assembles kwargs, calls engine
           │
           ▼
  Solver.solve(**kwargs)     ← pure math, returns frozen dataclasses
           │
     ┌─────┴──────┐
     ▼             ▼
ResultPanel    PlotManager   ← render table + Matplotlib chart
```

---

## 2. Stage 1: Equation Input Widget (`equation_input.py`)

`EquationInputWidget` is a reusable `ctk.CTkFrame` used on every solver page.

### What it contains

```
┌──────────────────────────────────────────┐
│ Label: "Equation f(x):"                 │
│                                          │
│ [sin] [cos] [tan] [ln] [exp] [sqrt] [π] │  ← symbol toolbar
│                                          │
│ ┌────────────────────────────────────┐   │
│ │  x**3 - 2*x**2 - 5              │   │  ← CTkEntry
│ └────────────────────────────────────┘   │
│ (error message in red, if any)           │
│                                          │
│ ┌────────────────────────────────────┐   │
│ │   x³ - 2x² - 5  (LaTeX preview)  │   │  ← Matplotlib mini-canvas
│ └────────────────────────────────────┘   │
└──────────────────────────────────────────┘
```

### Live validation and preview (on every keystroke)

```
KeyRelease event
      │
      ▼
_handle_change()
  └── after(300ms, _process_change)   ← debounced to avoid lag while typing
              │
              ▼
        _process_change()
          ├── _update_preview()
          │     sympy.sympify(expr)         ← parse to expression tree
          │     sympy.latex(expr)           ← convert to LaTeX string
          │     ax.text(0.5, 0.5, "$...$")  ← render in mini Matplotlib canvas
          │     canvas.draw()
          │
          └── on_change(expr) callback (optional, used by some pages)
```

**Validation on demand** (called by the page before solving):
```python
def is_valid(self) -> bool:
    expr = self.get_expression()
    valid = SymbolicParser.validate(expr)   # uses the engine's own parser
    if not valid:
        self.show_error("Invalid expression")
        self.entry.configure(border_color="#f44336")  # red border
    return valid
```

The widget uses `SymbolicParser.validate()` — the same function the engine uses — so the validation is always in sync with what the solver can actually parse.

### Symbol toolbar

Each button calls `_insert_symbol(val)`:
```python
def _insert_symbol(self, symbol: str):
    pos = self.entry.index("insert")   # cursor position
    self.entry.insert(pos, symbol)
    if "()" in symbol:
        self.entry.icursor(pos + symbol.find("(") + 1)  # cursor inside ()
    self._handle_change()              # triggers preview update
```

---

## 3. Stage 2: The Solver Page (`root_finder_page.py`)

### Dynamic input fields

The page has one or two secondary input fields whose labels change based on the selected method:

```
Method dropdown changes → update_inputs(method) called:

  "Bisection"       → label1="Lower Bound (a)"  label2="Upper Bound (b)"  [shown]
  "Secant"          → label1="First Guess (x0)"  label2="Second Guess (x1)" [shown]
  "Newton-Raphson"  → label1="Initial Guess (x0)"  input2 hidden
  "Simple Iteration"→ label1="Initial Guess (x0)"  input2 hidden
                       func_input.label = "Iteration Function g(x):"
```

This is purely cosmetic — the same CTkEntry widgets are reused, just relabeled and shown/hidden.

### Load Example

The page has a pre-built catalog of named problems. Selecting one calls `load_example(name)`:

```python
self.func_input.set_expression(selected["expression"])
self.tol_entry.delete(0, ctk.END)
self.tol_entry.insert(0, selected["tol"])
self.input1_entry.insert(0, selected["a"])  # or x0, etc.
```

This populates all fields instantly so users can explore without typing.

---

## 4. Stage 3: `solve_action()` — the bridge

`solve_action()` is triggered by the "Solve Equation" button. This is the only method that connects the GUI to the engine.

### Step-by-step:

```python
def solve_action(self):
    # 1. Read all input field values
    expression = self.func_input.get_expression()
    tol        = float(self.tol_entry.get() or 1e-6)
    method     = self.method_menu.get()

    # 2. Build the kwargs dict the engine expects
    kwargs = {
        "expression":     expression,
        "tolerance":      tol,
        "max_iterations": 100
    }

    # 3. Add method-specific parameters
    if method == "Bisection":
        kwargs["a"] = float(self.input1_entry.get())
        kwargs["b"] = float(self.input2_entry.get())
    elif method == "Secant":
        kwargs["x0"] = float(self.input1_entry.get())
        kwargs["x1"] = float(self.input2_entry.get())
    elif method in ("Newton-Raphson", "Simple Iteration"):
        kwargs["initial_guess"] = float(self.input1_entry.get())

    # 4. Call the engine (the ONLY line that touches numcore_engine directly)
    data  = solver.solve(**kwargs)      # returns SimulationData
    steps = solver.get_steps()          # returns List[NumericalStep]

    # 5. Route results to output components
    self.result_panel.update_result(data, steps)
    self.plot_manager.plot_solution_path(steps, expression)
```

The entire engine interaction is in **lines 4 and 5**. Everything above assembles the input; everything below renders the output.

---

## 5. Stage 4: Inside the Engine

When `solver.solve(**kwargs)` is called, this happens (using Newton-Raphson as an example):

```
kwargs = {expression: "x**3-2*x**2-5", initial_guess: 1.0, tolerance: 1e-4}
    │
    ▼
validate_input(**kwargs)
  checks: "expression" in kwargs ✓, "initial_guess" in kwargs ✓
    │
    ▼
SymbolicParser.parse_expression("x**3-2*x**2-5")
  normalize:  "x**3-2*x**2-5"  (no change needed here)
  sympify:    SymPy tree
  lambdify:   f = lambda x: x**3 - 2*x**2 - 5
    │
    ▼
SymbolicParser.get_derivative("x**3-2*x**2-5")
  sympy.diff(expr, x) → "3*x**2 - 4*x"
  lambdify:   df = lambda x: 3*x**2 - 4*x
    │
    ▼
Iteration loop:
  i=0: x_n=1.0
       fx  = f(1.0)  = 1 - 2 - 5    = -6.0
       dfx = df(1.0) = 3 - 4         = -1.0
       x_next = 1.0 - (-6.0)/(-1.0) = -5.0
       error  = |(-5.0) - 1.0|       = 6.0
       → NumericalStep(0, -5.0, 6.0, {x_n:1.0, f(x):-6.0, f'(x):-1.0})

  i=1: x_n=-5.0
       ... continues until error < 1e-4
    │
    ▼
Returns SimulationData(
  title="Newton-Raphson Convergence",
  x_data=[0, 1, 2, ...],           ← iteration numbers
  y_data=[-5.0, 2.31, ...],        ← x approximations
  metadata={"root": 2.6906, "iterations": 8, "diverged": False}
)
```

---

## 6. Stage 5: Rendering the Results

### ResultPanel (`result_panel.py`)

`update_result(data, steps)` does two things:

**Summary text** (reads from `data.metadata`):
```
Method: Newton-Raphson Convergence
Root: 2.69065080
Iterations: 8
```

**Step table** (reads from `steps[i].details`):

The table headers are **dynamically discovered** from the union of all `details` dicts:
```python
all_keys = set()
for s in steps:
    all_keys.update(s.details.keys())
# → {"x_n", "f(x)", "f'(x)"}
```

This means the same `ResultPanel` class works for every solver type without any custom code per solver — Bisection produces `{a, b, f(a), f(b), c, f(c)}` columns; Gauss-Seidel produces `{x:[...]}` columns; they all render correctly automatically.

| Step | x_n | f(x) | f'(x) | Value | Error |
|------|-----|------|-------|-------|-------|
| 0 | 1.000000 | -6.000000 | -1.000000 | -5.000000 | 6.00e+00 |
| 1 | -5.000000 | ... | ... | ... | ... |

### PlotManager (`visualization.py`)

The `PlotManager` owns a Matplotlib `Figure` embedded in the CTk frame via `FigureCanvasTkAgg`.

```python
self.figure = Figure(figsize=(5, 4), dpi=100)
self.ax     = self.figure.add_subplot(111)
self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
self.canvas_widget.pack(fill="both", expand=True)
```

**`plot_solution_path(steps, expression)`**:
- Evaluates `f(x)` over a range to draw the curve
- Plots arrows showing how `x_n` moves toward the root each iteration
- Marks the final root with a point

**`plot_iteration_history(steps)`**:
- Plots error vs. iteration number on a log scale
- Shows how fast the method converges

After any plot update: `self.canvas.draw()` repaints the embedded Matplotlib widget.

---

## 7. Smart Solve Path

The "Smart Solve (Compare)" button uses a slightly different path:

```
smart_solve_action()
    │
    ▼
ComparisonRunner(self.solvers)      ← wraps all 4 solver instances
    │
    ▼
runner.run_comparison(**kwargs)
    │
    For each solver:
      validate_input(**kwargs) → skip if can't handle inputs
      solver.solve(**kwargs)   → catch divergence/errors
    │
    ▼
ComparisonResult(best_method, results, recommendation)
    │
    ▼
SmartSolverPanel(self, comparison_result)  ← popup window showing all methods side-by-side
```

---

## 8. Error Handling

All exceptions from the engine are caught in `solve_action()`:

```python
except Exception as e:
    self.error_label.configure(text=f"Error: {str(e)}")
```

This means the GUI never crashes — it displays the engine's own error messages inline (e.g. `"f(a) and f(b) must have opposite signs"`, `"Zero diagonal element after row swapping"`).

---

## 9. Component Responsibility Summary

| Component | Owns | Does NOT own |
|---|---|---|
| `EquationInputWidget` | Live preview, symbol toolbar, input validation UI | Whether the expression is valid for a specific solver |
| Solver page (e.g. `RootFinderPage`) | Reading fields, building kwargs, calling engine, routing results | Any math |
| `numcore_engine` solvers | All numerical computation | Any UI state |
| `ResultPanel` | Rendering step tables | Which solver ran or what the columns mean |
| `PlotManager` | Matplotlib embedding and drawing | What data to draw (receives it from the page) |
