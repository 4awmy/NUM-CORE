# Quickstart: NUM-CORE Development Setup

**Feature**: `001-num-core-completion`

## Prerequisites

- Python 3.10+
- `uv` package manager

## Setup

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Launch application
uv run python main.py          # startup menu (TUI or GUI)
uv run python main.py --tui    # force TUI
uv run python main.py --gui    # force GUI
```

## Development Workflow

Implement in dependency order:

1. **Phase A** (Engine): Add `JacobiSolver` + divergence detection to all solvers
   ```bash
   # Test after Phase A
   uv run pytest tests/unit/test_network_solver.py tests/unit/test_root_finder.py -v
   ```

2. **Phase B** (TUI): Add comparison mode + CSV export + divergence warnings
   ```bash
   uv run python main.py --tui
   ```

3. **Phase C+D** (GUI Wiring + Redesign): Wire pages to real solvers, clean up layout
   ```bash
   uv run python main.py --gui
   ```

4. **Phase E** (Visualization): Add all plot methods, connect to pages
   ```bash
   uv run python main.py --gui  # test plots interactively
   ```

5. **Phase F** (Startup): Implement `main.py` mode selector + argparse flags

## Key File Reference

### Engine
| File | What to do |
|------|-----------|
| `numcore_engine/solvers/network_solver.py` | Add `JacobiSolver` class |
| `numcore_engine/solvers/root_finder.py` | Add divergence detection to both solvers |

### CLI
| File | What to do |
|------|-----------|
| `numcore_cli/formatter.py` | Add `export_steps_to_csv()` static method |
| `numcore_cli/terminal.py` | Add comparison mode option 3 + CSV prompt |

### GUI — Solver Pages
| File | What to do |
|------|-----------|
| `numcore_gui/dashboard.py` | Redesign sidebar labels, set 1280x800, dark theme |
| `numcore_gui/visualization.py` | Add 5 new `plot_*` methods to `PlotManager` |
| `numcore_gui/pages/root_finder_page.py` | Wire to real solver, add result panel |
| `numcore_gui/pages/network_solver_page.py` | Wire to real solver, add result panel |
| `numcore_gui/pages/calculus_page.py` | Wire to real solver, add result panel |

### GUI — Scientific Applications (NEW)
| File | What to do |
|------|-----------|
| `numcore_gui/pages/root_finder_app.py` | Create applications showcase page (beam thickness, etc.) |
| `numcore_gui/pages/network_solver_app.py` | Create applications showcase page (circuit analysis, etc.) |
| `numcore_gui/pages/calculus_app.py` | Create applications showcase page (interpolation + integration) |

### Main Entry
| File | What to do |
|------|-----------|
| `main.py` | Add startup menu + argparse |

## Solver Usage Examples

```python
from numcore_engine.solvers.root_finder import NewtonRaphsonSolver

solver = NewtonRaphsonSolver()
result = solver.solve(func_str="x**2 - 4", x0=1.0, tol=1e-6, max_iter=100)
print(result.metadata["solution"])    # ≈ 2.0
print(result.metadata["converged"])   # True
print(result.metadata["diverged"])    # False
print(result.metadata["iterations"])  # e.g. 4

steps = solver.get_steps()
for step in steps:
    print(step.step_idx, step.value, step.error)
```
