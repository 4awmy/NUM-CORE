# NUM-CORE: Unified Numerical Engineering & Simulation Suite
## 📋 Project Overview
NUM-CORE is a dual-interface engineering tool designed to solve complex numerical problems through a Professional CLI and visualize data-heavy simulations through a Modern Desktop Dashboard. 

---

## 📅 Timeline: 1 Week (7 Days)

### Phase 1: Foundation & CLI Core (Days 1-2)
*   **Deliverable**: Functional CLI with input parsing and basic math engine.
*   **Milestones**:
    *   [ ] Set up `main.py` entry point and command-line menu.
    *   [ ] Implement **Newton-Raphson** & **Simple Iteration** solvers for root finding.
    *   [ ] Implement **Gauss-Seidel** solver for linear systems (with diagonal dominance check).

### Phase 2: Post-Midterm Solvers (Days 3-4)
*   **Deliverable**: Integration of advanced calculus-based methods.
*   **Milestones**:
    *   [ ] **Interpolation Module**: Implement **Newton's Divided Difference** & **Lagrange** formulas.
    *   [ ] **Calculus Module**: Implement **Simpson's 1/3** and **Trapezoidal Rule** for Numerical Integration.
    *   [ ] **Differentiation Module**: Implement **Central/Forward/Backward Difference** formulas.

### Phase 3: The "Wow" Dashboard (Days 5-6)
*   **Deliverable**: Graphical interface for "Mission Launch" simulations.
*   **Milestones**:
    *   [ ] **Curve Fitting**: Implement **Least Squares Regression** for sensor data analysis.
    *   [ ] **Initial Volume Problem (IVP)**: Implement numerical solvers for Initial Value/Volume problems.
    *   [ ] **GUI Bridge**: Connect the `launch` command in CLI to open the `dashboard.py` (using CustomTkinter).
    *   [ ] **Visualization**: Add live `Matplotlib` plotting for curve fitting and integration results.

### Phase 4: Final Review & Delivery (Day 7)
*   **Deliverable**: Polished repository with full documentation.
*   **Milestones**:
    *   [ ] Write unit tests for each numerical module.
    *   [ ] Finalize `README.md` with engineering math explanations.
    *   [ ] Package for GitHub and finalize the project board.

---

## 🛠️ Tech Stack
*   **Core**: Python 3.10+
*   **UI (CLI)**: `rich` or `argparse`
*   **UI (Dashboard)**: `CustomTkinter`
*   **Math/Graphs**: `NumPy`, `Matplotlib`
*   **Documentation**: Markdown (GitHub Flavored)

---

## 📈 Key Deliverables
1. **NCC-Terminal**: A professional CLI for solving engineering math on the fly.
2. **NUM-CORE Dashboard**: A modern GUI for data visualization and "Mission" simulation.
3. **Engineering Math Engine**: A modular Python package containing all course-related algorithms.
