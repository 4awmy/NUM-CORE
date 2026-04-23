# NUM-CORE: Unified Numerical Engineering & Simulation Suite

🚀 **Modern Engineering CLI & High-Fidelity Visualization Dashboard**

NUM-CORE is a professional-grade numerical computation suite designed for engineering students and professionals. It provides a dual-interface experience: a powerful, interactive Command Line Interface (CLI) for rapid calculations and a modern Graphical User Interface (GUI) for data-heavy simulations and trajectory visualizations.

---

## 📋 Key Features

### 1. Root Finding Engine
Solve complex non-linear equations $f(x) = 0$ with high precision.
- **Newton-Raphson Method**: Rapid convergence using derivatives.
- **Simple Iteration Method**: Fixed-point iteration $x = g(x)$.
- **Live Convergence Tracking**: Detailed iteration steps and error analysis.

### 2. Network & Linear Solver
Solve systems of linear equations $Ax = b$, essential for circuit analysis and structural engineering.
- **Gauss-Seidel Solver**: Robust iterative method for large systems.
- **Automatic Diagonal Dominance**: Intelligent row swapping to ensure convergence.
- **Truss & Circuit Examples**: Preloaded engineering scenarios.

### 3. Calculus & Data Predictor
Analyze experimental data and perform numerical calculus.
- **Interpolation**: Newton's Divided Difference for polynomial fitting.
- **Numerical Integration**: Simpson's (1/3 and 3/8) and Trapezoidal rules.
- **Dynamic Data Points**: Add points on the fly and see instant updates.

### 4. Mission Control Dashboard (GUI)
A modern desktop application built with `CustomTkinter`.
- **Matplotlib Integration**: Live plotting of functions and data trends.
- **Theming**: Support for Light, Dark, and System appearance modes.
- **Integrated Help System**: Context-aware documentation for every module.

---

## 🛠️ Installation

### Prerequisites
- Python 3.10 or higher
- `pip` (Python package installer)

### Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/omarh-ossam/NUM-CORE.git
   cd NUM-CORE
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥️ Usage

### Command Line Interface (CLI)
The CLI is the primary entry point for quick numerical tasks. It uses `Rich` for beautiful terminal formatting.

To launch the CLI:
```bash
python main.py
```

**CLI Navigation**:
- Use the numbered menus to select a module.
- Follow the prompts to enter functions or data points.
- Load pre-built **Engineering Examples** to see the solvers in action.

### Graphical User Interface (GUI)
The GUI provides a "Mission Control" experience with live visualizations.

To launch the GUI directly:
```bash
python -m numcore_gui.dashboard
```
*(Note: You can also launch the GUI from within the CLI in future updates)*

---

## 📸 Screenshots

| CLI Main Menu | GUI Dashboard |
| :---: | :---: |
| ![CLI Screenshot Placeholder](docs/screenshots/cli_main.png) | ![GUI Screenshot Placeholder](docs/screenshots/gui_dashboard.png) |

| Root Finding Convergence | Calculus Visualization |
| :---: | :---: |
| ![Convergence Placeholder](docs/screenshots/convergence.png) | ![Calculus Placeholder](docs/screenshots/calculus_plot.png) |

---

## 🧪 Development & Testing

The project uses `pytest` for unit and integration testing.

To run the test suite:
```bash
pytest
```

### Project Structure
- `numcore_engine/`: Core mathematical solvers and logic.
- `numcore_cli/`: Rich-based terminal interface implementation.
- `numcore_gui/`: CustomTkinter dashboard and Matplotlib plots.
- `tests/`: Comprehensive test suite for all modules.

---

## 🎓 Credits
Developed as part of the **Numerical Methods** course.

**Author**: Omar Hossam
**License**: MIT
