# NUM-CORE: Unified Numerical Engineering & Simulation Suite

## 📋 Project Overview
NUM-CORE is a dual-interface engineering tool designed to solve complex numerical problems through a Professional CLI and visualize data-heavy simulations through a Modern Desktop Dashboard. 

---

## 📅 Timeline & Progress

### Phase 1: The Root Finder (Completed)
*   **Engineering Problem**: Calculate optimal dimensions for components (e.g., beam thickness/pipe diameter).
*   **Solvers**: Newton-Raphson, Simple Iteration, Bisection, Secant.
*   **Key Feature**: Live Convergence Tracking and Comparison.

### Phase 2: The Network Solver (Completed)
*   **Engineering Problem**: Solve for currents in an electrical circuit or flow rates in a pipe network.
*   **Solvers**: Gauss-Seidel, Jacobi.
*   **Key Feature**: Automatic Diagonal Dominance Check and Row Swapping.

### Phase 3: The Data Predictor & Calculus (Completed)
*   **Engineering Problem**: Predict values from experimental data and calculate cumulative values.
*   **Solvers**: Newton’s Divided Difference, Lagrange, Simpson's (1/3, 3/8), Trapezoidal, Gaussian Quadrature.
*   **Key Feature**: Dynamic Interpolation and Numerical Differentiation.

### Phase 4: Integration & "Wow" Dashboard (Completed)
*   **Engineering Problem**: Solve Initial Volume Problems and visualize system trends.
*   **Solvers**: Least Squares Regression, Euler, RK4.
*   **Key Feature**: CustomTkinter GUI with Matplotlib integration and "True Black" theme.

### Phase 5-11: Polish & Cross-Cutting Concerns (Completed)
*   **Refinements**: Enhanced error handling, divergence detection, and CSV export.
*   **Specialized Apps**: 4 Chapter Apps (Beam Stress, Circuit Analysis, Data Fitting, Work Done).
*   **Quality Assurance**: 80+ unit and integration tests with high coverage.
*   **Documentation**: Comprehensive README and docstrings.

---

## 🛠️ Tech Stack
*   **Core**: Python 3.13
*   **UI (CLI)**: `Rich`
*   **UI (Dashboard)**: `CustomTkinter`
*   **Math/Graphs**: `NumPy`, `Matplotlib`, `SymPy`
*   **Testing**: `pytest`
