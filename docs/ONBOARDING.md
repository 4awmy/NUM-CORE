# Project Onboarding: NUM-CORE

Welcome to the **NUM-CORE** project! This guide will help you understand the architecture, key components, and how to navigate the codebase.

## Project Overview
- **Name**: NUM-CORE (Numerical Methods Core Engine and GUI)
- **Description**: A comprehensive suite of numerical methods implemented in Python and MATLAB, featuring both a graphical user interface (GUI) and a command-line interface (CLI).
- **Languages**: Python, MATLAB, Markdown, JSON, YAML
- **Frameworks**: NumPy, Matplotlib, Pytest

---

## Architecture Layers

The project is organized into several distinct layers, each with a specific responsibility:

| Layer | Description |
|-------|-------------|
| **Engine Layer** | Core numerical solvers and mathematical logic implemented in Python. |
| **GUI Layer** | User interface components, pages, and visualization logic using Matplotlib. |
| **MATLAB Layer** | MATLAB implementation of the numerical methods suite with interactive menus. |
| **Specs Layer** | Technical specifications, data models, and implementation plans. |
| **Documentation Layer** | General documentation, architecture guides, and issue tracking. |
| **Infrastructure Layer** | Configuration, build scripts, logs, and automation tools. |
| **Test Layer** | Comprehensive test suite including unit, integration, and contract tests. |

---

## Key Files Map

### Engine Layer
- `numcore_engine/solvers/root_finder.py`: Implementations of root-finding algorithms (Bisection, Newton-Raphson, etc.)
- `numcore_engine/solvers/regression_solvers.py`: Implementations of curve fitting and regression models
- `numcore_engine/solvers/__init__.py`: Package initializer for engine solvers

### GUI Layer
- `main.py`: Application entry point, launches GUI or TUI
- `numcore_gui/dashboard.py`: Main GUI dashboard controller and layout
- `numcore_gui/visualization.py`: Handles Matplotlib integration and dynamic animations
- `numcore_gui/result_panel.py`: GUI component for displaying numerical results in tables
- `numcore_gui/equation_input.py`: Specialized widget for mathematical equation entry
- `numcore_gui/smart_solver_panel.py`: GUI panel for smart solver recommendations
- `numcore_gui/theme.py`: Central theme configuration for the application
- `numcore_gui/help_system.py`: Manages in-app help and info popups

### MATLAB Layer
- `matlab/main.m`: Main entry point for MATLAB edition
- `matlab/root_finding_menu.m`: MATLAB menu for root finding methods
- `matlab/gauss_seidel_solve.m`: MATLAB implementation of Gauss-Seidel solver
- `matlab/numerical_integration.m`: MATLAB numerical integration (Trapezoidal/Simpson)
- `matlab/ndd_interpolation.m`: MATLAB Newton's Divided Difference implementation

### Specs Layer
- `PROJECT_PLAN.md`: High-level implementation and completion plan
- `specs/001-num-core-completion/spec.md`: Feature specification for the complete solver suite
- `specs/001-num-core-completion/contracts/solver-interface.md`: Python protocol and solver contract definition

### Test Layer
- `tests/integration/test_app_flow.py`: Integration tests for the full numerical flow
- `tests/unit/test_root_finder.py`: Unit tests for root-finding algorithms
- `tests/unit/test_calculus_engine.py`: Unit tests for the calculus engine
- `tests/conftest.py`: Pytest configuration and shared fixtures

---

## Guided Tour

Follow these steps to get familiar with the project:

1.  **Welcome to NUM-CORE**: Start by reading the `README.md` to understand the project's purpose: a core engine for numerical methods with both GUI and CLI interfaces.
2.  **Application Entry Point**: The main entry point for the Python application is `main.py`. It initializes the environment and launches either the GUI dashboard or the Terminal interface.
3.  **Core Numerical Engine**: The numerical engine contains specialized solvers for root finding, regression, and calculus. These are found in the `numcore_engine/solvers` directory.
4.  **GUI Dashboard**: The graphical interface is built with PyQt/PySide. The `dashboard.py` file manages the main layout and navigation between different numerical method pages.
5.  **Visualization and Plotting**: Visualization is key for numerical methods. The `visualization.py` module handles dynamic Matplotlib plots and animations for root finding and interpolation.
6.  **MATLAB Edition**: For users preferring MATLAB, a complete implementation is available in the `matlab/` directory, featuring its own menu-driven UI and equivalent solver implementations.
7.  **Verification and Testing**: The project includes an extensive test suite. `integration/test_app_flow.py` verifies the complete application lifecycle across both CLI and GUI paths.

---

## Complexity Hotspots

These files have been identified as having higher complexity and may require more time to understand:

- `numcore_engine/solvers/root_finder.py` (Complex): Core logic for multiple root-finding algorithms.
- `numcore_engine/solvers/regression_solvers.py` (Complex): Mathematical implementations of various regression models.
- `numcore_gui/dashboard.py` (Complex): Orchestrates the main UI layout and state.
- `numcore_gui/visualization.py` (Complex): Complex Matplotlib integration and animation logic.
- `numcore_gui/result_panel.py` (Complex): Handles dynamic table generation and result formatting.
- `docs/ARCHITECTURE_DEEP.md` (Complex): Extensive technical documentation.
- `.specify/extensions/git/scripts/bash/create-new-feature.sh` (Complex): Advanced Git automation script.
- `main.py` (Moderate): Application initialization and routing.
- `matlab/main.m` (Moderate): Entry point for the MATLAB implementation.
- `numcore_gui/equation_input.py` (Moderate): Custom widget for math input.
