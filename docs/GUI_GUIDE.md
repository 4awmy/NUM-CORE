# NUM-CORE GUI Guide

The `numcore_gui` package provides a modern, "True Black" dashboard for interacting with numerical methods and visualizing their real-world applications.

---

## 🎨 Design Philosophy

- **Professional Aesthetic**: Uses a high-contrast dark theme (True Black) designed for engineering workstations.
- **Dynamic Feedback**: Real-time plotting and status updates keep the user informed during long computations.
- **Visual Learning**: Every solver includes a visualization component to bridge the gap between abstract math and practical results.

---

## 🏗️ Structure

### 1. The Dashboard (`dashboard.py`)
The main window of the application. It features:
- **Sidebar Navigation**: Organized by solver categories (Root Finding, Linear Systems, Calculus, etc.).
- **Content Area**: Dynamically switches between different solver pages.
- **Status Bar**: Displays system messages and computation performance metrics.

### 2. Plotting System (`visualization.py`)
Managed by the `PlotManager` class, this system handles the embedding of Matplotlib into the CustomTkinter UI.
- **Dark Mode Sync**: Automatically matches Matplotlib's colors to the app's theme.
- **Interactive Toolbar**: Allows users to zoom, pan, and save generated plots.
- **Animation Support**: Supports dynamic plotting for iterative methods (e.g., watching a root-finder converge).

### 3. Specialized Pages (`pages/`)
Each numerical method has its own page class to keep the code modular:
- `RootFinderPage`: Input fields for equations, bounds, and method selection.
- `NetworkSolverPage`: Matrix and vector input for linear systems.
- `CalculusPage`: Data table input for integration and differentiation.

---

## 🚀 Practical Application Apps (Chapter Apps)

One of NUM-CORE's unique features is the "Chapter Apps"—specialized tools that apply numerical methods to specific engineering scenarios:

- **Beam Stress App (Ch 1)**: Uses root-finding to calculate critical stress points on structural beams.
- **Circuit Analysis App (Ch 2)**: Solves complex circuit node voltages using the Network Solver.
- **Projectile Trajectory (Ch 4)**: Uses ODE solvers to simulate physics-based trajectories.

---

## 🛠️ UI Components

- **`equation_input.py`**: A specialized widget for symbolic equation entry.
- **`smart_solver_panel.py`**: A side panel that provides context-aware parameter suggestions.
- **`help_system.py`**: Manages the integrated tooltips and info popups that explain each mathematical concept.
- **`theme.py`**: Centralizes the color palette (e.g., `ACCENT_BLUE`, `ACCENT_ORANGE`) and fonts.
