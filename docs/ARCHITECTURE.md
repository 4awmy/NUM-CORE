# NUM-CORE Architecture

NUM-CORE is designed with a strictly modular architecture, separating numerical computation logic from presentation layers. This ensures that the core mathematical engine is reliable, testable, and reusable across different interfaces (CLI and GUI).

---

## 🏗️ Design Principles

1.  **Separation of Concerns**: Numerical logic stays in `numcore_engine`, CLI logic in `numcore_cli`, and GUI logic in `numcore_gui`.
2.  **Interface-Driven Solvers**: All numerical solvers implement a common `Solver` protocol, allowing the UIs to treat them polymorphically.
3.  **Symbolic Core**: User equations are parsed and manipulated using `SymPy` before being converted to fast `NumPy` functions for computation.
4.  **Traceable Computation**: Solvers generate a list of `NumericalStep` objects, enabling step-by-step educational output in both TUI and GUI.

---

## 🧩 System Components

### 1. `numcore_engine` (The Core)
The engine is the heart of the application. It contains no UI-specific code.
- **`solvers/`**: Individual numerical modules (e.g., `root_finder.py`, `network_solver.py`).
- **`interfaces.py`**: Defines the `Solver` protocol that all solvers must follow.
- **`models.py`**: Immutable dataclasses (`NumericalStep`, `SimulationData`) used to pass data between the engine and UIs.
- **`parser.py`**: Handles mathematical string normalization, validation, and differentiation using `SymPy`.

### 2. `numcore_cli` (The Command Center)
A lightweight terminal interface using the `Rich` library.
- **`terminal.py`**: Manages the interactive menu system and user input flow.
- **`formatter.py`**: Converts engine `NumericalStep` lists into beautiful, color-coded tables.

### 3. `numcore_gui` (The Mission Control)
A high-fidelity desktop application built with `CustomTkinter`.
- **`dashboard.py`**: The main layout controller with a sidebar navigation system.
- **`visualization.py`**: Encapsulates `Matplotlib` logic for static, dynamic, and interactive plotting.
- **`pages/`**: Individual UI views for each solver category, keeping the dashboard code clean.
- **`styles/`**: Custom Matplotlib styles (e.g., `numcore_black.mplstyle`) for a professional look.

---

## 🔄 Data Flow

1.  **Input Acquisition**: The UI (CLI or GUI) collects parameters (equation, matrix, tolerances).
2.  **Validation & Parsing**: `SymbolicParser` validates the equation and converts it to a Python callable.
3.  **Solver Execution**: The UI instantiates the appropriate `Solver` and calls `.solve()`.
4.  **Result Propagation**: The solver returns a `SimulationData` object and stores a history of `NumericalStep` objects.
5.  **Output Generation**:
    -   **CLI**: Prints tables using `formatter.py`.
    -   **GUI**: Renders graphs using `visualization.py` and updates result panels.

---

## 🛠️ Solver Interface

Every solver in `numcore_engine/solvers` follows this protocol:

```python
class Solver(Protocol):
    def solve(self, **kwargs: Any) -> SimulationData:
        """Executes the method and returns final results."""
        ...

    def get_steps(self) -> List[NumericalStep]:
        """Returns the iteration history for educational display."""
        ...

    def validate_input(self, **kwargs: Any) -> bool:
        """Pre-check to ensure numerical stability (e.g., diagonal dominance)."""
        ...
```

---

## 📐 Extension Guide

To add a new numerical method:
1.  Create a new solver class in `numcore_engine/solvers/`.
2.  Implement the `Solver` protocol.
3.  Add a corresponding page in `numcore_gui/pages/`.
4.  Register the new solver in the `numcore_cli/terminal.py` menu.
