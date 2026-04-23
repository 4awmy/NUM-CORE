from typing import Any, Dict, List, Optional
import numpy as np

from ..interfaces import Solver
from ..models import NumericalStep, SimulationData


class InterpolationSolver(Solver):
    """Newton's Divided Difference Interpolation Solver."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute Newton's Divided Difference interpolation.
        
        Args:
            x_points: List of x coordinates.
            y_points: List of y coordinates.
            target_x: Optional x value to interpolate.
            
        Returns:
            SimulationData containing the interpolation results.
        """
        x_points = np.array(kwargs.get("x_points", []), dtype=float)
        y_points = np.array(kwargs.get("y_points", []), dtype=float)
        target_x = kwargs.get("target_x")

        if not self.validate_input(x_points=x_points, y_points=y_points):
            raise ValueError("Invalid input points for interpolation.")

        n = len(x_points)
        memo: Dict[tuple, float] = {}

        def get_divided_diff(indices: tuple) -> float:
            if indices in memo:
                return memo[indices]
            
            if len(indices) == 1:
                res = y_points[indices[0]]
            else:
                res = (get_divided_diff(indices[1:]) - get_divided_diff(indices[:-1])) / \
                      (x_points[indices[-1]] - x_points[indices[0]])
            
            memo[indices] = res
            return res

        self._steps = []
        coef = []
        for j in range(n):
            c = get_divided_diff(tuple(range(j + 1)))
            coef.append(c)
            self._steps.append(NumericalStep(
                step_idx=j,
                value=c,
                details={
                    "description": f"Order {j} divided difference coefficient",
                    "indices": list(range(j + 1))
                }
            ))

        # Newton polynomial evaluation
        def evaluate(x: float) -> float:
            res = coef[0]
            for i in range(1, n):
                term = coef[i]
                for j in range(i):
                    term *= (x - x_points[j])
                res += term
            return res

        result_y = []
        if target_x is not None:
            if isinstance(target_x, (int, float)):
                result_y = [evaluate(float(target_x))]
                x_data = [float(target_x)]
            else:
                x_data = [float(x) for x in target_x]
                result_y = [evaluate(x) for x in x_data]
        else:
            # Default to original points if no target_x
            x_data = x_points.tolist()
            result_y = y_points.tolist()

        return SimulationData(
            title="Newton's Divided Difference Interpolation",
            x_data=x_data,
            y_data=result_y,
            metadata={"coefficients": coef}
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        x_points = kwargs.get("x_points")
        y_points = kwargs.get("y_points")
        
        if x_points is None or y_points is None:
            return False
        
        if len(x_points) != len(y_points) or len(x_points) < 2:
            return False
            
        return True


class IntegrationSolver(Solver):
    """Numerical Integration Solver (Trapezoidal, Simpson's 1/3, 3/8)."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute numerical integration.
        
        Args:
            x_points: List of x coordinates.
            y_points: List of y coordinates.
            method: 'trapezoidal', 'simpson13', or 'simpson38'.
            
        Returns:
            SimulationData containing the integration result.
        """
        x_points = np.array(kwargs.get("x_points", []), dtype=float)
        y_points = np.array(kwargs.get("y_points", []), dtype=float)
        method = kwargs.get("method", "trapezoidal").lower()

        if not self.validate_input(x_points=x_points, y_points=y_points, method=method):
            raise ValueError(f"Invalid input for method {method}.")

        n = len(x_points) - 1
        h = (x_points[-1] - x_points[0]) / n
        self._steps = []

        if method == "trapezoidal":
            result = (h / 2) * (y_points[0] + 2 * np.sum(y_points[1:-1]) + y_points[-1])
            self._steps.append(NumericalStep(
                step_idx=1,
                value=result,
                details={"method": "Trapezoidal Rule", "h": h, "n": n}
            ))
        elif method == "simpson13":
            if n % 2 != 0:
                raise ValueError("Simpson's 1/3 rule requires an even number of intervals.")
            
            result = (h / 3) * (y_points[0] + 4 * np.sum(y_points[1:-1:2]) + 2 * np.sum(y_points[2:-2:2]) + y_points[-1])
            self._steps.append(NumericalStep(
                step_idx=1,
                value=result,
                details={"method": "Simpson's 1/3 Rule", "h": h, "n": n}
            ))
        elif method == "simpson38":
            if n % 3 != 0:
                raise ValueError("Simpson's 3/8 rule requires intervals to be a multiple of 3.")
            
            sum_val = y_points[0] + y_points[-1]
            for i in range(1, n):
                if i % 3 == 0:
                    sum_val += 2 * y_points[i]
                else:
                    sum_val += 3 * y_points[i]
            
            result = (3 * h / 8) * sum_val
            self._steps.append(NumericalStep(
                step_idx=1,
                value=result,
                details={"method": "Simpson's 3/8 Rule", "h": h, "n": n}
            ))
        else:
            raise ValueError(f"Unsupported integration method: {method}")

        return SimulationData(
            title=f"Numerical Integration ({method})",
            x_data=x_points.tolist(),
            y_data=[result],
            metadata={"method": method, "total_integral": result}
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        x_points = kwargs.get("x_points")
        y_points = kwargs.get("y_points")
        method = kwargs.get("method", "trapezoidal").lower()

        if x_points is None or y_points is None:
            return False
        
        n_points = len(x_points)
        if n_points != len(y_points) or n_points < 2:
            return False

        # Check for uniform spacing (required for standard Simpson's)
        h = np.diff(x_points)
        if not np.allclose(h, h[0]):
            return False

        n = n_points - 1
        if method == "simpson13" and n % 2 != 0:
            return False
        if method == "simpson38" and n % 3 != 0:
            return False

        return True
