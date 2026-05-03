from typing import Any, Dict, List, Optional
from ..interfaces import Solver
from ..models import NumericalStep, SimulationData
from ..parser import SymbolicParser
from .calculus_engine import NumericalDifferentiationSolver


class BisectionSolver(Solver):
    """
    Bisection method for finding roots of a function f(x) = 0.
    Requires an interval [a, b] such that f(a) * f(b) < 0.
    """

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute the Bisection solver.

        Args:
            expression: The string expression of f(x).
            a: Lower bound of the interval.
            b: Upper bound of the interval.
            tolerance: The convergence tolerance (default 1e-6).
            max_iterations: The maximum number of iterations (default 100).

        Returns:
            SimulationData containing the convergence history.
        """
        if not self.validate_input(**kwargs):
            raise ValueError("Invalid input parameters for BisectionSolver.")

        expression = str(kwargs["expression"])
        a = float(kwargs["a"])
        b = float(kwargs["b"])
        tolerance = float(kwargs.get("tolerance", 1e-6))
        max_iterations = int(kwargs.get("max_iterations", 100))

        f = SymbolicParser.parse_expression(expression)

        fa = f(a)
        fb = f(b)

        if fa * fb >= 0:
            raise ValueError("f(a) and f(b) must have opposite signs.")

        self._steps = []
        x_history: List[float] = []
        y_history: List[float] = []

        c = a
        for i in range(max_iterations):
            c = (a + b) / 2
            fc = f(c)

            error = abs(b - a) / 2

            step = NumericalStep(
                step_idx=i,
                value=c,
                error=error,
                details={
                    "a": float(a),
                    "b": float(b),
                    "f(a)": float(fa),
                    "f(b)": float(fb),
                    "c": float(c),
                    "f(c)": float(fc),
                },
            )
            self._steps.append(step)
            x_history.append(float(i))
            y_history.append(float(c))

            if error < tolerance or abs(fc) < 1e-12:
                break

            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc

        return SimulationData(
            title="Bisection Convergence",
            x_data=x_history,
            y_data=y_history,
            metadata={"root": c, "iterations": len(self._steps), "diverged": False},
        )

    def get_steps(self) -> List[NumericalStep]:
        """Return the list of intermediate steps taken by the solver."""
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        """Validate the input parameters for the solver."""
        return "expression" in kwargs and "a" in kwargs and "b" in kwargs


class NewtonRaphsonSolver(Solver):
    """
    Newton-Raphson method for finding roots of a function f(x) = 0.
    Formula: x_{n+1} = x_n - f(x_n) / f'(x_n)
    """

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute the Newton-Raphson solver.

        Args:
            expression: The string expression of f(x).
            initial_guess: The initial value of x.
            tolerance: The convergence tolerance (default 1e-6).
            max_iterations: The maximum number of iterations (default 100).

        Returns:
            SimulationData containing the convergence history.
        """
        if not self.validate_input(**kwargs):
            raise ValueError("Invalid input parameters for NewtonRaphsonSolver.")

        expression = str(kwargs["expression"])
        x_n = float(kwargs["initial_guess"])
        tolerance = float(kwargs.get("tolerance", 1e-6))
        max_iterations = int(kwargs.get("max_iterations", 100))

        # Parse f(x) and its derivative f'(x)
        f = SymbolicParser.parse_expression(expression)
        try:
            derivative_expr = SymbolicParser.get_derivative(expression)
            df = SymbolicParser.parse_expression(derivative_expr)
        except Exception:
            # Fallback to numerical differentiation using calculus_engine
            diff_solver = NumericalDifferentiationSolver()

            def df(x: float) -> float:
                res = diff_solver.solve(f=f, x=x, h=1e-7, method="central")
                return float(res.y_data[0])

        self._steps = []
        x_history: List[float] = []
        y_history: List[float] = []
        error_history: List[float] = []
        diverged = False

        for i in range(max_iterations):
            fx = f(x_n)
            dfx = df(x_n)

            if abs(dfx) < 1e-12:
                # Avoid division by zero
                break

            x_next = x_n - fx / dfx
            error = abs(x_next - x_n)

            step = NumericalStep(
                step_idx=i,
                value=x_next,
                error=error,
                details={"x_n": float(x_n), "f(x)": float(fx), "f'(x)": float(dfx)},
            )
            self._steps.append(step)
            x_history.append(float(i))
            y_history.append(float(x_next))

            # Divergence detection: 5 consecutive increases (needs 6 errors)
            error_history.append(error)
            if len(error_history) >= 6:
                if all(error_history[j] < error_history[j + 1] for j in range(-6, -1)):
                    diverged = True
                    break

            if error < tolerance:
                x_n = x_next
                break

            x_n = x_next

        return SimulationData(
            title="Newton-Raphson Convergence",
            x_data=x_history,
            y_data=y_history,
            metadata={"root": x_n, "iterations": len(self._steps), "diverged": diverged},
        )

    def get_steps(self) -> List[NumericalStep]:
        """Return the list of intermediate steps taken by the solver."""
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        """Validate the input parameters for the solver."""
        return "expression" in kwargs and "initial_guess" in kwargs


class SecantSolver(Solver):
    """
    Secant method for finding roots of a function f(x) = 0.
    Formula: x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))
    """

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute the Secant solver.

        Args:
            expression: The string expression of f(x).
            x0: First initial guess.
            x1: Second initial guess.
            tolerance: The convergence tolerance (default 1e-6).
            max_iterations: The maximum number of iterations (default 100).

        Returns:
            SimulationData containing the convergence history.
        """
        if not self.validate_input(**kwargs):
            raise ValueError("Invalid input parameters for SecantSolver.")

        expression = str(kwargs["expression"])
        x0 = float(kwargs["x0"])
        x1 = float(kwargs["x1"])
        tolerance = float(kwargs.get("tolerance", 1e-6))
        max_iterations = int(kwargs.get("max_iterations", 100))

        f = SymbolicParser.parse_expression(expression)

        self._steps = []
        x_history: List[float] = []
        y_history: List[float] = []
        error_history: List[float] = []
        diverged = False

        for i in range(max_iterations):
            fx0 = f(x0)
            fx1 = f(x1)

            if abs(fx1 - fx0) < 1e-12:
                break

            x_next = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            error = abs(x_next - x1)

            step = NumericalStep(
                step_idx=i,
                value=x_next,
                error=error,
                details={
                    "x0": float(x0),
                    "x1": float(x1),
                    "f(x0)": float(fx0),
                    "f(x1)": float(fx1),
                    "x2": float(x_next),
                },
            )
            self._steps.append(step)
            x_history.append(float(i))
            y_history.append(float(x_next))

            # Divergence detection: 5 consecutive increases (needs 6 errors)
            error_history.append(error)
            if len(error_history) >= 6:
                if all(error_history[j] < error_history[j + 1] for j in range(-6, -1)):
                    diverged = True
                    break

            if error < tolerance:
                x1 = x_next
                break

            x0, x1 = x1, x_next

        return SimulationData(
            title="Secant Convergence",
            x_data=x_history,
            y_data=y_history,
            metadata={"root": x1, "iterations": len(self._steps), "diverged": diverged},
        )

    def get_steps(self) -> List[NumericalStep]:
        """Return the list of intermediate steps taken by the solver."""
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        """Validate the input parameters for the solver."""
        return "expression" in kwargs and "x0" in kwargs and "x1" in kwargs


class SimpleIterationSolver(Solver):
    """
    Simple Iteration (Fixed Point) method for finding roots of x = g(x).
    Formula: x_{n+1} = g(x_n)
    """

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute the Simple Iteration solver.

        Args:
            expression: The string expression of g(x).
            initial_guess: The initial value of x.
            tolerance: The convergence tolerance (default 1e-6).
            max_iterations: The maximum number of iterations (default 100).

        Returns:
            SimulationData containing the convergence history.
        """
        if not self.validate_input(**kwargs):
            raise ValueError("Invalid input parameters for SimpleIterationSolver.")

        expression = str(kwargs["expression"])
        x_n = float(kwargs["initial_guess"])
        tolerance = float(kwargs.get("tolerance", 1e-6))
        max_iterations = int(kwargs.get("max_iterations", 100))

        # Parse g(x)
        g = SymbolicParser.parse_expression(expression)

        # Convergence check: |g'(x)| < 1
        convergence_passed = True
        try:
            dg_expr = SymbolicParser.get_derivative(expression)
            dg = SymbolicParser.parse_expression(dg_expr)
            if abs(dg(x_n)) >= 1:
                convergence_passed = False
        except Exception:
            # Fallback to numerical derivative for check
            diff_solver = NumericalDifferentiationSolver()
            res = diff_solver.solve(f=g, x=x_n, h=1e-7, method="central")
            if abs(res.y_data[0]) >= 1:
                convergence_passed = False

        self._steps = []
        x_history: List[float] = []
        y_history: List[float] = []
        error_history: List[float] = []
        diverged = False

        for i in range(max_iterations):
            x_next = g(x_n)
            error = abs(x_next - x_n)

            step = NumericalStep(
                step_idx=i,
                value=x_next,
                error=error,
                details={"x_n": float(x_n), "g(x)": float(x_next)},
            )
            self._steps.append(step)
            x_history.append(float(i))
            y_history.append(float(x_next))

            # Divergence detection: 5 consecutive increases (needs 6 errors)
            error_history.append(error)
            if len(error_history) >= 6:
                if all(error_history[j] < error_history[j + 1] for j in range(-6, -1)):
                    diverged = True
                    break

            if error < tolerance:
                x_n = x_next
                break

            x_n = x_next

        return SimulationData(
            title="Simple Iteration Convergence",
            x_data=x_history,
            y_data=y_history,
            metadata={
                "root": x_n,
                "iterations": len(self._steps),
                "diverged": diverged,
                "convergence_check_passed": convergence_passed,
            },
        )

    def get_steps(self) -> List[NumericalStep]:
        """Return the list of intermediate steps taken by the solver."""
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        """Validate the input parameters for the solver."""
        return "expression" in kwargs and "initial_guess" in kwargs
