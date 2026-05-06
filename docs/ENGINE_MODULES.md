# NUM-CORE Engine Modules

The `numcore_engine` package contains the mathematical implementations of various numerical methods. Each module is designed to be independent and follows the core `Solver` protocol.

---

## 🔬 Available Solvers

### 1. Root Finder (`root_finder.py`)
Provides methods for finding the roots of non-linear equations $f(x) = 0$.
- **Bisection**: A robust bracketing method.
- **False Position**: An improved bracketing method using linear interpolation.
- **Simple Iteration**: Fixed-point iteration $x_{n+1} = g(x_n)$.
- **Newton-Raphson**: Fast convergence using $x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$.
- **Secant**: Approximates the derivative using two points.

### 2. Network Solver (`network_solver.py`)
Specialized in solving systems of linear equations $Ax = b$.
- **Jacobi Method**: Simultanous updates for sparse systems.
- **Gauss-Seidel**: Successive updates with faster convergence.
- **Diagonal Dominance**: Automatic checking and row-swapping to ensure method stability.

### 3. Calculus Engine (`calculus_engine.py`)
Handles numerical differentiation and integration.
- **Differentiation**: Forward, backward, and central difference schemes.
- **Integration**:
  - **Trapezoidal Rule**: Linear approximation.
  - **Simpson's 1/3 Rule**: Quadratic approximation.
  - **Simpson's 3/8 Rule**: Cubic approximation.

### 4. Interpolation & Regression (`regression_solvers.py`)
Fits models to discrete data points.
- **Newton's Divided Difference**: For building interpolating polynomials.
- **Linear Regression**: Least-squares fit for data trends.

### 5. ODE Solvers (`ode_solvers.py`)
Solves Ordinary Differential Equations of the form $\frac{dy}{dx} = f(x, y)$.
- **Euler Method**: Basic first-order integration.
- **Runge-Kutta (RK4)**: High-accuracy fourth-order integration.

---

## 🧪 Comparison Module (`comparison.py`)
This unique module allows running multiple methods on the same problem to compare their performance, convergence speed, and accuracy side-by-side.

---

## 📜 Matlab Reference (`matlab/`)
The project includes a `matlab/` directory containing the original reference implementations of these algorithms. These serve as a baseline for the Python engine's accuracy and are useful for users transitioning from a Matlab environment.
- `main.m`: The primary entry point for the Matlab suite.
- Method-specific files (e.g., `newton_raphson_solve.m`, `gauss_seidel_solve.m`).
