from typing import Any, Dict, List, Optional
import numpy as np

from ..interfaces import Solver
from ..models import NumericalStep, SimulationData


class LeastSquaresSolver(Solver):
    """
    Least Squares Regression for linear fitting (y = mx + c).
    """

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute Least Squares linear regression.

        Args:
            x_points: List of x coordinates.
            y_points: List of y coordinates.

        Returns:
            SimulationData containing the fitted linear curve and original points.
        """
        solver = CurveFittingSolver()
        kwargs["model"] = "linear"
        result = solver.solve(**kwargs)
        
        # Map back to old metadata for compatibility
        new_metadata = dict(result.metadata)
        new_metadata["slope"] = result.metadata["a1"]
        new_metadata["intercept"] = result.metadata["a0"]
        new_metadata["method"] = "Least Squares"
        
        # Update steps details too
        steps = solver.get_steps()
        if steps:
            step = steps[0]
            new_details = dict(step.details)
            new_details["slope"] = result.metadata["a1"]
            new_details["intercept"] = result.metadata["a0"]
            self._steps = [NumericalStep(
                step_idx=step.step_idx,
                value=step.value,
                error=step.error,
                details=new_details,
                check_name=step.check_name,
                check_passed=step.check_passed
            )]
        else:
            self._steps = []

        return SimulationData(
            title="Least Squares Linear Regression",
            x_data=result.x_data,
            y_data=result.y_data,
            metadata=new_metadata
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        return CurveFittingSolver().validate_input(**kwargs)


class CurveFittingSolver(Solver):
    """
    Curve Fitting Solver supporting multiple regression models.
    Models: linear, quadratic, power, exponential, growth.
    """

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute curve fitting regression.

        Args:
            x_points: List of x coordinates.
            y_points: List of y coordinates.
            model: Type of model ("linear", "quadratic", "power", "exponential", "growth").

        Returns:
            SimulationData containing the fitted curve and original points.
        """
        if not self.validate_input(**kwargs):
            raise ValueError("Invalid input parameters for CurveFittingSolver.")

        x = np.array(kwargs["x_points"], dtype=float)
        y = np.array(kwargs["y_points"], dtype=float)
        model = kwargs.get("model", "linear").lower()

        if model == "linear":
            return self._solve_linear(x, y)
        elif model == "quadratic":
            return self._solve_quadratic(x, y)
        elif model == "power":
            return self._solve_power(x, y)
        elif model == "exponential":
            return self._solve_exponential(x, y)
        elif model == "growth":
            return self._solve_growth(x, y)
        else:
            raise ValueError(f"Unsupported model: {model}")

    def _solve_linear(self, x: np.ndarray, y: np.ndarray) -> SimulationData:
        n = len(x)
        sum_x = np.sum(x)
        sum_y = np.sum(y)
        sum_xx = np.sum(x * x)
        sum_xy = np.sum(x * y)

        denominator = n * sum_xx - sum_x**2
        if abs(denominator) < 1e-12:
            raise ValueError("Denominator is zero; cannot perform linear regression.")

        a1 = (n * sum_xy - sum_x * sum_y) / denominator
        a0 = (sum_y - a1 * sum_x) / n

        details = {
            "n": n,
            "sum_x": sum_x,
            "sum_y": sum_y,
            "sum_xx": sum_xx,
            "sum_xy": sum_xy,
            "a0": a0,
            "a1": a1,
            "equation": f"y = {a0:.4g} + {a1:.4g}x"
        }

        self._steps = [NumericalStep(step_idx=0, value=a1, details=details)]

        x_line = np.linspace(np.min(x), np.max(x), 100)
        y_line = a0 + a1 * x_line

        return SimulationData(
            title="Linear Regression",
            x_data=x_line.tolist(),
            y_data=y_line.tolist(),
            metadata={
                "model": "linear",
                "a0": a0,
                "a1": a1,
                "equation": details["equation"],
                "original_x": x.tolist(),
                "original_y": y.tolist(),
            }
        )

    def _solve_quadratic(self, x: np.ndarray, y: np.ndarray) -> SimulationData:
        n = len(x)
        sum_x = np.sum(x)
        sum_x2 = np.sum(x**2)
        sum_x3 = np.sum(x**3)
        sum_x4 = np.sum(x**4)
        sum_y = np.sum(y)
        sum_xy = np.sum(x * y)
        sum_x2y = np.sum(x**2 * y)

        A = np.array([
            [n, sum_x, sum_x2],
            [sum_x, sum_x2, sum_x3],
            [sum_x2, sum_x3, sum_x4]
        ])
        B = np.array([sum_y, sum_xy, sum_x2y])

        try:
            coeffs = np.linalg.solve(A, B)
        except np.linalg.LinAlgError:
            raise ValueError("System of equations for quadratic regression is singular.")

        a0, a1, a2 = coeffs

        details = {
            "n": n,
            "sum_x": sum_x,
            "sum_x2": sum_x2,
            "sum_x3": sum_x3,
            "sum_x4": sum_x4,
            "sum_y": sum_y,
            "sum_xy": sum_xy,
            "sum_x2y": sum_x2y,
            "a0": a0,
            "a1": a1,
            "a2": a2,
            "equation": f"y = {a0:.4g} + {a1:.4g}x + {a2:.4g}x^2"
        }

        self._steps = [NumericalStep(step_idx=0, value=a2, details=details)]

        x_line = np.linspace(np.min(x), np.max(x), 100)
        y_line = a0 + a1 * x_line + a2 * x_line**2

        return SimulationData(
            title="Quadratic Regression",
            x_data=x_line.tolist(),
            y_data=y_line.tolist(),
            metadata={
                "model": "quadratic",
                "a0": a0,
                "a1": a1,
                "a2": a2,
                "equation": details["equation"],
                "original_x": x.tolist(),
                "original_y": y.tolist(),
            }
        )

    def _solve_power(self, x: np.ndarray, y: np.ndarray) -> SimulationData:
        if np.any(x <= 0) or np.any(y <= 0):
            raise ValueError("Power model requires positive x and y values.")

        ln_x = np.log(x)
        ln_y = np.log(y)

        n = len(x)
        sum_X = np.sum(ln_x)
        sum_Y = np.sum(ln_y)
        sum_XX = np.sum(ln_x**2)
        sum_XY = np.sum(ln_x * ln_y)

        denominator = n * sum_XX - sum_X**2
        if abs(denominator) < 1e-12:
            raise ValueError("Denominator is zero; cannot perform power regression.")

        b = (n * sum_XY - sum_X * sum_Y) / denominator
        A = (sum_Y - b * sum_X) / n
        a = np.exp(A)

        details = {
            "n": n,
            "sum_ln_x": sum_X,
            "sum_ln_y": sum_Y,
            "sum_ln_x_sq": sum_XX,
            "sum_ln_x_ln_y": sum_XY,
            "a": a,
            "b": b,
            "equation": f"y = {a:.4g} * x^{b:.4g}"
        }

        self._steps = [NumericalStep(step_idx=0, value=a, details=details)]

        x_line = np.linspace(np.min(x), np.max(x), 100)
        y_line = a * x_line**b

        return SimulationData(
            title="Power Regression",
            x_data=x_line.tolist(),
            y_data=y_line.tolist(),
            metadata={
                "model": "power",
                "a": a,
                "b": b,
                "equation": details["equation"],
                "original_x": x.tolist(),
                "original_y": y.tolist(),
            }
        )

    def _solve_exponential(self, x: np.ndarray, y: np.ndarray) -> SimulationData:
        if np.any(y <= 0):
            raise ValueError("Exponential model requires positive y values.")

        ln_y = np.log(y)

        n = len(x)
        sum_x = np.sum(x)
        sum_Y = np.sum(ln_y)
        sum_xx = np.sum(x**2)
        sum_xY = np.sum(x * ln_y)

        denominator = n * sum_xx - sum_x**2
        if abs(denominator) < 1e-12:
            raise ValueError("Denominator is zero; cannot perform exponential regression.")

        b = (n * sum_xY - sum_x * sum_Y) / denominator
        A = (sum_Y - b * sum_x) / n
        a = np.exp(A)

        details = {
            "n": n,
            "sum_x": sum_x,
            "sum_ln_y": sum_Y,
            "sum_xx": sum_xx,
            "sum_x_ln_y": sum_xY,
            "a": a,
            "b": b,
            "equation": f"y = {a:.4g} * e^({b:.4g}x)"
        }

        self._steps = [NumericalStep(step_idx=0, value=a, details=details)]

        x_line = np.linspace(np.min(x), np.max(x), 100)
        y_line = a * np.exp(b * x_line)

        return SimulationData(
            title="Exponential Regression",
            x_data=x_line.tolist(),
            y_data=y_line.tolist(),
            metadata={
                "model": "exponential",
                "a": a,
                "b": b,
                "equation": details["equation"],
                "original_x": x.tolist(),
                "original_y": y.tolist(),
            }
        )

    def _solve_growth(self, x: np.ndarray, y: np.ndarray) -> SimulationData:
        if np.any(x == 0) or np.any(y == 0):
            raise ValueError("Growth model requires non-zero x and y values.")

        inv_x = 1.0 / x
        inv_y = 1.0 / y

        n = len(x)
        sum_X = np.sum(inv_x)
        sum_Y = np.sum(inv_y)
        sum_XX = np.sum(inv_x**2)
        sum_XY = np.sum(inv_x * inv_y)

        denominator = n * sum_XX - sum_X**2
        if abs(denominator) < 1e-12:
            raise ValueError("Denominator is zero; cannot perform growth regression.")

        a = (n * sum_XY - sum_X * sum_Y) / denominator
        b = (sum_Y - a * sum_X) / n

        details = {
            "n": n,
            "sum_inv_x": sum_X,
            "sum_inv_y": sum_Y,
            "sum_inv_x_sq": sum_XX,
            "sum_inv_x_inv_y": sum_XY,
            "a": a,
            "b": b,
            "equation": f"y = x / ({a:.4g} + {b:.4g}x)"
        }

        self._steps = [NumericalStep(step_idx=0, value=a, details=details)]

        x_line = np.linspace(np.min(x), np.max(x), 100)
        y_line = x_line / (a + b * x_line)

        return SimulationData(
            title="Growth Model Regression",
            x_data=x_line.tolist(),
            y_data=y_line.tolist(),
            metadata={
                "model": "growth",
                "a": a,
                "b": b,
                "equation": details["equation"],
                "original_x": x.tolist(),
                "original_y": y.tolist(),
            }
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        if "x_points" not in kwargs or "y_points" not in kwargs:
            return False
        x = kwargs["x_points"]
        y = kwargs["y_points"]
        if not (isinstance(x, (list, np.ndarray)) and isinstance(y, (list, np.ndarray))):
            return False
        if len(x) != len(y):
            return False

        model = kwargs.get("model", "linear").lower()
        if model == "quadratic":
            return len(x) >= 3
        return len(x) >= 2
