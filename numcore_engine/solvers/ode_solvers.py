from typing import Any, Dict, List, Optional, Callable
import numpy as np

from ..interfaces import Solver
from ..models import NumericalStep, SimulationData
from ..parser import SymbolicParser


class EulerSolver(Solver):
    """
    Euler's method for solving first-order Ordinary Differential Equations (ODEs).
    Formula: y_{n+1} = y_n + h * f(x_n, y_n)
    """

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute Euler's method.

        Args:
            expression: The string expression of dy/dx = f(x, y).
            x0: Initial x value.
            y0: Initial y value.
            h: Step size.
            steps: Number of steps to take.

        Returns:
            SimulationData containing the solution trajectory.
        """
        if not self.validate_input(**kwargs):
            raise ValueError("Invalid input parameters for EulerSolver.")

        expression = str(kwargs["expression"])
        x0 = float(kwargs["x0"])
        y0 = float(kwargs["y0"])
        h = float(kwargs["h"])
        num_steps = int(kwargs["steps"])

        f = SymbolicParser.parse_expression(expression, variables=["x", "y"])

        self._steps = []
        x_history = [x0]
        y_history = [y0]

        curr_x = x0
        curr_y = y0

        # Initial step
        self._steps.append(
            NumericalStep(
                step_idx=0,
                value=curr_y,
                details={"x": curr_x, "y": curr_y, "f(x,y)": f(curr_x, curr_y)},
            )
        )

        for i in range(1, num_steps + 1):
            slope = f(curr_x, curr_y)
            curr_y = curr_y + h * slope
            curr_x = curr_x + h

            x_history.append(curr_x)
            y_history.append(curr_y)

            self._steps.append(
                NumericalStep(
                    step_idx=i,
                    value=curr_y,
                    details={"x": curr_x, "y": curr_y, "f(x,y)": f(curr_x, curr_y)},
                )
            )

        return SimulationData(
            title="Euler ODE Solution",
            x_data=x_history,
            y_data=y_history,
            metadata={
                "method": "Euler",
                "expression": expression,
                "h": h,
                "steps": num_steps,
            },
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        required = ["expression", "x0", "y0", "h", "steps"]
        return all(k in kwargs for k in required)


class RungeKuttaSolver(Solver):
    """
    Fourth-order Runge-Kutta (RK4) method for solving first-order ODEs.
    """

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute RK4 method.

        Args:
            expression: The string expression of dy/dx = f(x, y).
            x0: Initial x value.
            y0: Initial y value.
            h: Step size.
            steps: Number of steps to take.

        Returns:
            SimulationData containing the solution trajectory.
        """
        if not self.validate_input(**kwargs):
            raise ValueError("Invalid input parameters for RungeKuttaSolver.")

        expression = str(kwargs["expression"])
        x0 = float(kwargs["x0"])
        y0 = float(kwargs["y0"])
        h = float(kwargs["h"])
        num_steps = int(kwargs["steps"])

        f = SymbolicParser.parse_expression(expression, variables=["x", "y"])

        self._steps = []
        x_history = [x0]
        y_history = [y0]

        curr_x = x0
        curr_y = y0

        # Initial step
        self._steps.append(
            NumericalStep(
                step_idx=0,
                value=curr_y,
                details={"x": curr_x, "y": curr_y},
            )
        )

        for i in range(1, num_steps + 1):
            k1 = h * f(curr_x, curr_y)
            k2 = h * f(curr_x + h / 2, curr_y + k1 / 2)
            k3 = h * f(curr_x + h / 2, curr_y + k2 / 2)
            k4 = h * f(curr_x + h, curr_y + k3)

            curr_y = curr_y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
            curr_x = curr_x + h

            x_history.append(curr_x)
            y_history.append(curr_y)

            self._steps.append(
                NumericalStep(
                    step_idx=i,
                    value=curr_y,
                    details={
                        "x": curr_x,
                        "y": curr_y,
                        "k1": k1,
                        "k2": k2,
                        "k3": k3,
                        "k4": k4,
                    },
                )
            )

        return SimulationData(
            title="Runge-Kutta (RK4) ODE Solution",
            x_data=x_history,
            y_data=y_history,
            metadata={
                "method": "RK4",
                "expression": expression,
                "h": h,
                "steps": num_steps,
            },
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        required = ["expression", "x0", "y0", "h", "steps"]
        return all(k in kwargs for k in required)
