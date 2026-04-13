# NUM-CORE: Unified Numerical Engineering & Simulation Suite

## 📋 Project Overview
NUM-CORE is a dual-interface engineering tool designed to solve complex numerical problems through a Professional CLI and visualize data-heavy simulations through a Modern Desktop Dashboard. 

---

## 📅 Timeline: 1 Week (7 Days)

### Phase 1: The Root Finder (Days 1-2)
*   **Engineering Problem**: Calculate optimal dimensions for components (e.g., beam thickness/pipe diameter) given a complex non-linear stress equation.
*   **Core Tasks**: Implement **Newton-Raphson** and **Simple Iteration** solvers.
*   **Key Feature**: User input for functions and initial guesses, with a live **Convergence Comparison** (iteration counts) between both methods.

### Phase 2: The Network Solver (Days 3-4)
*   **Engineering Problem**: Solve for currents in an electrical circuit or flow rates in a pipe network using linear systems ($Ax=b$).
*   **Core Tasks**: Implement a robust **Gauss-Seidel** solver.
*   **Key Feature**: Automatic **Diagonal Dominance Check**. If the matrix is non-convergent, the system attempts to swap rows to achieve dominance.

### Phase 3: The Data Predictor & Calculus (Days 5-6)
*   **Engineering Problem**: Predict values from experimental data (e.g., Temp vs. Pressure) and calculate cumulative values (e.g., total fuel volume).
*   **Core Tasks**: Implement **Newton’s Divided Difference** and **Numerical Integration** (Simpson's/Trapezoidal).
*   **Key Feature**: **Dynamic Interpolation**. Allow users to add data points on the fly and see the interpolating polynomial update instantly, showcasing Newton's recursive efficiency.

### Phase 4: Integration & "Wow" Dashboard (Day 7)
*   **Engineering Problem**: Solve **Initial Volume Problems** and visualize system trends.
*   **Core Tasks**: Implement **Curve Fitting** (Least Squares Regression) and the **CustomTkinter GUI Bridge**.
*   **Key Feature**: The `launch` command opens a high-fidelity dashboard with live **Matplotlib** plotting for trajectory visualization and simulation data.

---

## 🛠️ Tech Stack
*   **Core**: Python 3.10+
*   **UI (CLI)**: `rich` or `argparse`
*   **UI (Dashboard)**: `CustomTkinter`
*   **Math/Graphs**: `NumPy`, `Matplotlib`
*   **Documentation**: Markdown (GitHub Flavored)
