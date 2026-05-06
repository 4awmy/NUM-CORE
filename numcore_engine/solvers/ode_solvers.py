from typing import Any, Dict, List, Optional, Callable
import numpy as np
import sympy

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


class ModifiedEulerSolver(Solver):
    """
    Modified Euler's method (Heun's method) for solving first-order ODEs.
    Predictor: y*_{n+1} = y_n + h * f(x_n, y_n)
    Corrector: y_{n+1} = y_n + (h/2) * [f(x_n, y_n) + f(x_{n+1}, y*_{n+1})]
    """

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute Modified Euler's method.

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
            raise ValueError("Invalid input parameters for ModifiedEulerSolver.")

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
            f_xy = f(curr_x, curr_y)
            y_predict = curr_y + h * f_xy
            next_x = curr_x + h
            f_next = f(next_x, y_predict)

            curr_y = curr_y + (h / 2) * (f_xy + f_next)
            curr_x = next_x

            x_history.append(curr_x)
            y_history.append(curr_y)

            self._steps.append(
                NumericalStep(
                    step_idx=i,
                    value=curr_y,
                    details={
                        "x": curr_x,
                        "y": curr_y,
                        "f_xy": f_xy,
                        "y_predict": y_predict,
                        "f_next": f_next,
                    },
                )
            )

        return SimulationData(
            title="Modified Euler (Heun) ODE Solution",
            x_data=x_history,
            y_data=y_history,
            metadata={
                "method": "Modified Euler",
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


class TaylorSeriesOrder4Solver(Solver):
    """
    Fourth-order Taylor Series method for solving first-order ODEs.
    y_{n+1} = y_n + h*y' + (h^2/2)*y'' + (h^3/6)*y''' + (h^4/24)*y''''
    """

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute Taylor Series Order 4 method.

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
            raise ValueError("Invalid input parameters for TaylorSeriesOrder4Solver.")

        expression = str(kwargs["expression"])
        x0 = float(kwargs["x0"])
        y0 = float(kwargs["y0"])
        h = float(kwargs["h"])
        num_steps = int(kwargs["steps"])

        # Symbolic setup for derivatives
        x_sym, y_sym = sympy.symbols("x y")
        f_sym = sympy.sympify(SymbolicParser.normalize(expression))

        y_p1 = f_sym
        y_p2 = sympy.diff(y_p1, x_sym) + sympy.diff(y_p1, y_sym) * f_sym
        y_p3 = sympy.diff(y_p2, x_sym) + sympy.diff(y_p2, y_sym) * f_sym
        y_p4 = sympy.diff(y_p3, x_sym) + sympy.diff(y_p3, y_sym) * f_sym

        # Create callables
        f1 = sympy.lambdify((x_sym, y_sym), y_p1, modules=["numpy"])
        f2 = sympy.lambdify((x_sym, y_sym), y_p2, modules=["numpy"])
        f3 = sympy.lambdify((x_sym, y_sym), y_p3, modules=["numpy"])
        f4 = sympy.lambdify((x_sym, y_sym), y_p4, modules=["numpy"])

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
            d1 = float(f1(curr_x, curr_y))
            d2 = float(f2(curr_x, curr_y))
            d3 = float(f3(curr_x, curr_y))
            d4 = float(f4(curr_x, curr_y))

            term1 = h * d1
            term2 = (h**2 / 2) * d2
            term3 = (h**3 / 6) * d3
            term4 = (h**4 / 24) * d4

            curr_y = curr_y + term1 + term2 + term3 + term4
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
                        "y_prime": d1,
                        "y_double_prime": d2,
                        "y_triple_prime": d3,
                        "y_quad_prime": d4,
                    },
                )
            )

        return SimulationData(
            title="Taylor Series (Order 4) ODE Solution",
            x_data=x_history,
            y_data=y_history,
            metadata={
                "method": "Taylor Order 4",
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
