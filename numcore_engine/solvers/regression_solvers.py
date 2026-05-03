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
            SimulationData containing the regression line and original points.
        """
        if not self.validate_input(**kwargs):
            raise ValueError("Invalid input parameters for LeastSquaresSolver.")

        x = np.array(kwargs["x_points"], dtype=float)
        y = np.array(kwargs["y_points"], dtype=float)
        n = len(x)

        sum_x = np.sum(x)
        sum_y = np.sum(y)
        sum_xx = np.sum(x * x)
        sum_xy = np.sum(x * y)

        denominator = n * sum_xx - sum_x**2
        if abs(denominator) < 1e-12:
            raise ValueError("Denominator is zero; cannot perform linear regression.")

        m = (n * sum_xy - sum_x * sum_y) / denominator
        c = (sum_y - m * sum_x) / n

        self._steps = [
            NumericalStep(
                step_idx=0,
                value=m,
                details={
                    "slope": m,
                    "intercept": c,
                    "sum_x": sum_x,
                    "sum_y": sum_y,
                    "sum_xx": sum_xx,
                    "sum_xy": sum_xy,
                },
            )
        ]

        # Generate regression line points for visualization
        x_min, x_max = np.min(x), np.max(x)
        x_line = np.linspace(x_min, x_max, 100)
        y_line = m * x_line + c

        return SimulationData(
            title="Least Squares Linear Regression",
            x_data=x_line.tolist(),
            y_data=y_line.tolist(),
            metadata={
                "method": "Least Squares",
                "slope": m,
                "intercept": c,
                "equation": f"y = {m:.4g}x + {c:.4g}",
                "original_x": x.tolist(),
                "original_y": y.tolist(),
            },
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        if "x_points" not in kwargs or "y_points" not in kwargs:
            return False
        x = kwargs["x_points"]
        y = kwargs["y_points"]
        return len(x) == len(y) and len(x) >= 2
