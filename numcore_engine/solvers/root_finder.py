from typing import Any, Dict, List, Optional
from ..interfaces import Solver
from ..models import NumericalStep, SimulationData
from ..parser import SymbolicParser


class NewtonRaphsonSolver:
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
        derivative_expr = SymbolicParser.get_derivative(expression)
        df = SymbolicParser.parse_expression(derivative_expr)

        self._steps = []
        x_history: List[float] = []
        y_history: List[float] = []

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
                details={"f(x)": float(fx), "f'(x)": float(dfx)},
            )
            self._steps.append(step)
            x_history.append(float(i))
            y_history.append(float(x_next))

            if error < tolerance:
                x_n = x_next
                break

            x_n = x_next

        return SimulationData(
            title="Newton-Raphson Convergence",
            x_data=x_history,
            y_data=y_history,
            metadata={"root": x_n, "iterations": len(self._steps)},
        )

    def get_steps(self) -> List[NumericalStep]:
        """Return the list of intermediate steps taken by the solver."""
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        """Validate the input parameters for the solver."""
        return "expression" in kwargs and "initial_guess" in kwargs


class SimpleIterationSolver:
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

        self._steps = []
        x_history: List[float] = []
        y_history: List[float] = []

        for i in range(max_iterations):
            x_next = g(x_n)
            error = abs(x_next - x_n)

            step = NumericalStep(
                step_idx=i,
                value=x_next,
                error=error,
                details={"g(x)": float(x_next)},
            )
            self._steps.append(step)
            x_history.append(float(i))
            y_history.append(float(x_next))

            if error < tolerance:
                x_n = x_next
                break

            x_n = x_next

        return SimulationData(
            title="Simple Iteration Convergence",
            x_data=x_history,
            y_data=y_history,
            metadata={"root": x_n, "iterations": len(self._steps)},
        )

    def get_steps(self) -> List[NumericalStep]:
        """Return the list of intermediate steps taken by the solver."""
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        """Validate the input parameters for the solver."""
        return "expression" in kwargs and "initial_guess" in kwargs
