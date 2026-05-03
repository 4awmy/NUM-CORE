# Contract: Equation Input Widget

**Feature**: `002-enhanced-gui-solvers` | **File**: `numcore_gui/equation_input.py`

## EquationInputWidget

A reusable CTk composite widget for equation entry with live preview.

```python
class EquationInputWidget(ctk.CTkFrame):
    def __init__(self, master, label: str = "f(x) =", on_change: Callable = None): ...

    def get_expression(self) -> str:
        """Return the normalized Python expression (^ → **). Empty string if invalid."""

    def get_raw(self) -> str:
        """Return the raw text the user typed."""

    def set_expression(self, expr: str) -> None:
        """Programmatically set the input field (e.g., for pre-filled examples)."""

    def is_valid(self) -> bool:
        """True if the current expression parses without error."""

    def show_error(self, message: str) -> None:
        """Display an external error (e.g., from solver validation) below the field."""

    def clear_error(self) -> None:
        """Clear any displayed error message."""
```

## Layout Structure

```
┌─────────────────────────────────────────────┐
│ Label: "f(x) ="                             │
│ ┌─────────────────────────────────────────┐ │
│ │  Text input field                       │ │
│ └─────────────────────────────────────────┘ │
│ [sin] [cos] [tan] [ln] [exp] [√] [π] [e]   │
│ Preview: ┌──────────────────────────────┐   │
│          │  x² + sin(x)  (matplotlib)   │   │
│          └──────────────────────────────┘   │
│ Error: ⚠ [error message if invalid]         │
└─────────────────────────────────────────────┘
```

## Normalization Rules

| User input | Normalized output |
|------------|------------------|
| `x^2` | `x**2` |
| `e^x` | `exp(x)` |
| `ln(x)` | `log(x)` |
| `pi` | `pi` (sympy constant) |
| `2x` | `2*x` (implicit multiplication — if feasible) |

## Preview Rendering

- Triggered by `after(300)` debounce on `<KeyRelease>` event.
- Converts normalized expression to MathText: `$f(x) = x^{2} + \sin(x)$`.
- Renders in a 4×0.6 inch matplotlib figure with black background.
- On parse failure: preview shows `⚠ Invalid expression` in red.
