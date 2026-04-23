---
design_depth: deep
task_complexity: complex
---

# NUM-CORE: Unified Numerical Engineering & Simulation Suite - Design Document

## 1. Problem Statement
**Title**: NUM-CORE: Unified Numerical Engineering & Simulation Suite

**Problem Overview**: Engineering students and professionals often need to solve complex numerical problems—such as root-finding, linear systems, and calculus. While solving these problems is the core task, visualizing their **real-world applications** (e.g., beam stress distribution, circuit node voltages, projectile trajectories) is essential for truly understanding and communicating the results.

**The Solution**: NUM-CORE addresses this by providing a dual-interface tool. The **Command Center (CLI)** handles rapid calculations and provides step-by-step numerical output for any function. The **Mission Control Dashboard (GUI)** is specifically designed to showcase the **practical applications** of these numerical methods through high-fidelity, interactive simulations and simulations. As each phase is completed, the unified suite is updated on GitHub to provide a continuous, well-documented project history.

**Key Decisions**:
- **GUI for Practical Applications** — Specifically focused on real-world simulations to make the numerical data "come alive." *Rationale: This makes the tool highly valuable for students and professionals to visualize the impact of their numerical solutions.*
- **Unified Suite with Continuous Updates** — Provides a professional, all-in-one experience with a clear development history on GitHub. *Rationale: This ensures the project is well-organized and reflects its progress across the 4 phases.*

## 2. Requirements

**Functional Requirements**:
- **REQ-1: Root-finding Module** — Implement **Newton-Raphson** and **Simple Iteration** for non-linear equations. (Traces To: Phase 1)
- **REQ-2: Network Solver Module** — Implement a **Gauss-Seidel** solver with automatic **Diagonal Dominance Check** and row-swapping logic. (Traces To: Phase 2)
- **REQ-3: Calculus & Predictor Module** — Implement **Newton’s Divided Difference** for interpolation and **Numerical Integration** (Simpson's/Trapezoidal). (Traces To: Phase 3)
- **REQ-4: Calculus Results Mode** — Provide **step-by-step numerical output** in the CLI for all calculus problems. (Traces To: Phase 3)
- **REQ-5: Mission Launch Dashboard** — Develop a **CustomTkinter GUI** that displays interactive, dynamic, and static Matplotlib simulations for practical applications. (Traces To: Phase 4)
- **REQ-6: Hybrid Function Input** — Support both a catalog of **common engineering equations** and a **custom symbolic mode** using `sympy`. (Traces To: All phases)
- **REQ-7: In-App Help System** — Include helpful **info popups and tooltips** directly in the GUI to explain the numerical methods in real-time. (Traces To: Phase 4)

**Non-Functional Requirements**:
- **REQ-8: High Numerical Accuracy** — Ensure 100% accuracy through a robust **Test-Driven Development (TDD)** workflow. (Traces To: All phases)
- **REQ-9: Performance & Responsiveness** — Maintain a high-performance experience, especially for live trajectory animations in the GUI. (Traces To: Phase 4)
- **REQ-10: Professional Architecture** — Use a **modular, plugin-based** project structure for maintainability and extensibility. (Traces To: All phases)

**Constraints**:
- **REQ-11: Tech Stack** — Python 3.10+, `CustomTkinter`, `Rich`, `NumPy`, `Matplotlib`, `SymPy`.
- **REQ-12: GitHub Updates** — The unified suite must be updated on GitHub after each phase is completed and tested.

## 3. Approach

**Selected Approach: The Modular Engineering Suite (Approach 1)**

**Summary**: A highly structured, plugin-based architecture designed for 100% accuracy, extensibility, and professional engineering use.

**Decision Matrix**:

| Criterion | Weight | Approach 1 (Modular) | Approach 2 (Integrated) |
|-----------|--------|----------------------|-------------------------|
| **Accuracy & Reliability** | 30% | **5**: TDD and modular testing ensure 100% accuracy. | **3**: Basic tests provide some confidence but less robust. |
| **Extensibility** | 20% | **5**: Plugin system makes adding new solvers trivial. | **2**: Hardcoded logic makes expansion difficult. |
| **User Experience** | 25% | **4**: Clean CLI and GUI with integrated in-app help. | **4**: Similar UI/UX, but potentially harder to refine. |
| **Development Speed** | 15% | **3**: More upfront design work required. | **5**: Faster to get results on the screen. |
| **Maintainability** | 10% | **5**: Clean separation of concerns and clear structure. | **2**: Tightly coupled logic is harder to maintain. |
| **Weighted Total** | | **4.5** | **3.3** |

**Rationale Annotations**:
- **Modular Plugin-based Architecture** — Each numerical solver is a separate Python module with a common `Solver` interface. *Rationale: This makes it very easy to test, add new solvers, and swap them out (Traces To: REQ-10).*
- **Test-Driven Development (TDD)** — Implement robust automated tests using `pytest` for each solver. *Rationale: Accuracy is non-negotiable for engineering tools (Traces To: REQ-8).*
- **Shared Data Models** — Use common data structures for functions, matrices, and data points between the CLI and GUI. *Rationale: Ensures consistency in results across different interfaces (Traces To: REQ-6).*
- **GitHub Update Strategy** — The unified suite is updated on GitHub after each phase is completed and tested. *Rationale: This provides a continuous and well-documented project history (Traces To: REQ-12).*

**Per-decision Alternatives**:
- **Solver Interface** — *(considered: `abc.ABC` — rejected because `typing.Protocol` is more flexible; considered: `dict`-based config — rejected because it lacks type safety)*.
- **Plotting Engine** — *(considered: `plotly` — rejected because it's harder to integrate into `CustomTkinter` than `Matplotlib`)*.
- **Symbolic Parser** — *(considered: custom regex parser — rejected because it's less robust than `sympy`)*.

## 4. Architecture

**Architecture Overview**:
NUM-CORE is structured as a **Modular Package** with clear separation between its numerical engine and its user interfaces.

**Component Diagram**:
- **`numcore_engine` (Core Engine Package)**
  - `solvers` (Module for each numerical method: `root_finder.py`, `network_solver.py`, etc.)
  - `models` (Data classes for functions, matrices, and simulation data)
  - `parser` (Symbolic logic using `sympy` for user-defined equations)
- **`numcore_cli` (Command Center)**
  - `terminal` (CLI menu system using `rich`)
  - `output` (Logic for step-by-step numerical formatting)
- **`numcore_gui` (Mission Control Dashboard)**
  - `dashboard` (CustomTkinter GUI layout)
  - `visualization` (Matplotlib integration for interactive, dynamic, and static plots)
  - `help` (Info popups and tooltips system)
- **`tests` (Automated Test Suite)**
  - `unit` (Tests for each solver in the engine)
  - `integration` (Tests for CLI/GUI data flow)

**Data Flow**:
1. **User Input** — User provides a function, matrix, or data points through the CLI or GUI.
2. **Symbolic Parsing** — The `parser` module uses `sympy` to convert input strings into executable Python functions (Traces To: REQ-6).
3. **Numerical Solver** — The appropriate `Solver` module executes the algorithm (Newton-Raphson, Gauss-Seidel, etc.) using the parsed function and initial guesses (Traces To: REQ-1, REQ-2).
4. **Step-by-Step Generation** — The solver generates a trace of intermediate steps for educational purposes (Traces To: REQ-4).
5. **Output & Visualization** — The results are formatted for the terminal or plotted in the dashboard as interactive, dynamic, or static simulations (Traces To: REQ-5).

**Key Interfaces**:
- **`Solver` Protocol** — Defines the common methods for all numerical solvers: `solve(input_data)`, `get_steps()`, and `validate_input()`. *Rationale: Ensures consistency across all numerical modules.*
- **`SimulationData` Class** — A standard format for storing simulation results (X, Y points, time series, error metrics) for plotting. *Rationale: Allows any solver to provide data for the dashboard visualizations.*

**Per-decision Alternatives**:
- **State Management** — *(considered: `Redux`-like store — rejected because it's overkill for a Python desktop app; considered: global variables — rejected because it's brittle and hard to test; selected: shared `AppContext` object)*.
- **Plotting Integration** — *(considered: embedding Matplotlib in a separate window — rejected because it breaks the "Mission Control" feel; selected: embedding Matplotlib directly in `CustomTkinter` frames)*.

## 5. Agent Team

**Role: Architect**
- **Focus**: Overall system design, defining the `Solver` interface, and ensuring the modular package structure is maintainable (Traces To: REQ-10).
- **Key Task**: Set up the `numcore_engine` package and initial project skeleton.

**Role: Coder**
- **Focus**: Implementation of all numerical solvers (Newton-Raphson, Gauss-Seidel, etc.) and the CLI/GUI interfaces (Traces To: REQ-1, REQ-2, REQ-3).
- **Key Task**: Build the core numerical logic and the Command Center (CLI).

**Role: Tester**
- **Focus**: Automated unit and integration tests (TDD) for every solver module (Traces To: REQ-8).
- **Key Task**: Create a robust `pytest` suite and verify 100% numerical accuracy.

**Role: UX Designer**
- **Focus**: Dashboard layout in `CustomTkinter`, interactive plotting in Matplotlib, and the in-app help system (Traces To: REQ-5, REQ-7).
- **Key Task**: Build the "Wow" Dashboard and the high-fidelity visualizations.

**Role: Technical Writer**
- **Focus**: Comprehensive README and user guide with screenshots and examples (Traces To: REQ-12).
- **Key Task**: Document the project, instructions, and numerical methods for students.

## 6. Risk Assessment

**Risk 1: Numerical Divergence & Stability (High Impact)**
- **Issue**: Algorithms like **Gauss-Seidel** and **Newton-Raphson** can fail to converge if the initial guess is poor or if the system is not diagonally dominant (Traces To: REQ-2).
- **Mitigation**: Implement robust **automatic checks for convergence** and provide clear error messages to the user. For Gauss-Seidel, we'll automatically attempt **row-swapping** to achieve diagonal dominance.

**Risk 2: GUI Dashboard Performance (Medium Impact)**
- **Issue**: High-fidelity, dynamic Matplotlib animations in **CustomTkinter** can become slow or laggy, especially with many data points (Traces To: REQ-9).
- **Mitigation**: Use efficient **NumPy arrays** for data processing and Matplotlib's `animation.FuncAnimation` or `blitting` techniques for smooth, high-performance visualization.

**Risk 3: Symbolic Parsing Errors (Medium Impact)**
- **Issue**: User-defined symbolic functions (e.g., `sin(x) + e^x`) can be complex to parse and evaluate safely (Traces To: REQ-6).
- **Mitigation**: Leverage the well-tested **`sympy` library** for robust symbolic parsing and include validation checks to catch invalid mathematical expressions.

**Risk 4: GitHub Sync & Merge Conflicts (Low Impact)**
- **Issue**: Frequent updates across multiple phases can lead to a cluttered GitHub history or potential merge conflicts (Traces To: REQ-12).
- **Mitigation**: Follow a clean **Git workflow** (e.g., using feature branches for each phase) and perform a final cleanup of the repository before project completion.

**Risk 5: Complexity of "Both (Hybrid)" Function Input (Low Impact)**
- **Issue**: Managing both a catalog of predefined equations and a custom symbolic mode can be difficult to implement and test.
- **Mitigation**: Use a common **`Solver` interface** that can handle both predefined formulas and symbolic functions through the `parser` module.

## 7. Success Criteria

**1. Robust Numerical Engine**
- **Criteria**: All 4 phases of numerical solvers are implemented and 100% accurate (Traces To: REQ-1, REQ-2, REQ-3).
- **Verification**: All `pytest` cases pass with accurate numerical results for known engineering problems.

**2. Professional Command Center (CLI)**
- **Criteria**: A clean, menu-driven terminal UI (`main.py`) using `rich` for all 4 phases, providing clear, step-by-step numerical output (Traces To: REQ-4).
- **Verification**: Users can solve complex problems in the CLI with minimal effort and understand the intermediate steps.

**3. "Wow" Mission Control Dashboard (GUI)**
- **Criteria**: A modern `CustomTkinter` desktop application that visualizes the **practical applications** of the numerical results through interactive, dynamic, and static Matplotlib plots (Traces To: REQ-5).
- **Verification**: The dashboard provides a high-fidelity experience with "live" animations for simulations (e.g., trajectory tracking).

**4. Continuous GitHub History**
- **Criteria**: The project repository is updated on GitHub after each of the 4 phases is completed and tested (Traces To: REQ-12).
- **Verification**: A clear, well-documented commit history on GitHub reflects the progress through the phases.

**5. Comprehensive Documentation**
- **Criteria**: A detailed Markdown **README.md** with screenshots, instructions, and examples for students (Traces To: REQ-12).
- **Verification**: New users can install and use NUM-CORE correctly by following the instructions in the README.

**6. User-friendly In-App Help**
- **Criteria**: Helpful info popups and tooltips are available directly in the GUI to explain the numerical methods in real-time (Traces To: REQ-7).
- **Verification**: Users can understand the numerical concepts behind the simulations by clicking on the help icons.
