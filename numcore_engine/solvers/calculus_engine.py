from typing import Any, Dict, List, Optional, Union
import numpy as np

from ..interfaces import Solver
from ..models import NumericalStep, SimulationData


class LagrangeInterpolationSolver(Solver):
    """Lagrange Interpolation Solver."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute Lagrange interpolation.
        
        Args:
            x_points: List of x coordinates.
            y_points: List of y coordinates.
            target_x: Optional x value(s) to interpolate.
            
        Returns:
            SimulationData containing the interpolation results.
        """
        x_points = np.array(kwargs.get("x_points") or [], dtype=float)
        y_points = np.array(kwargs.get("y_points") or [], dtype=float)
        target_x = kwargs.get("target_x")

        if not self.validate_input(x_points=x_points, y_points=y_points):
            raise ValueError("Invalid input points for interpolation.")

        n = len(x_points)
        self._steps = []

        def evaluate(x: float) -> float:
            total = 0.0
            for i in range(n):
                li = 1.0
                for j in range(n):
                    if i != j:
                        li *= (x - x_points[j]) / (x_points[i] - x_points[j])
                term = y_points[i] * li
                total += term
            return total

        result_y = []
        x_data = []
        if target_x is not None:
            if isinstance(target_x, (int, float)):
                x_data = [float(target_x)]
                result_y = [evaluate(float(target_x))]
            else:
                x_data = [float(x) for x in target_x]
                result_y = [evaluate(x) for x in x_data]
        else:
            x_data = x_points.tolist()
            result_y = y_points.tolist()

        return SimulationData(
            title="Lagrange Interpolation",
            x_data=x_data,
            y_data=result_y,
            metadata={"method": "Lagrange"}
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        x_points = kwargs.get("x_points")
        y_points = kwargs.get("y_points")
        
        if x_points is None or y_points is None:
            return False
        
        try:
            if len(x_points) != len(y_points) or len(x_points) < 2:
                return False
        except TypeError:
            return False
            
        return True


class NewtonDifferenceTableSolver(Solver):
    """Newton Forward Difference Table Solver for equispaced points."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Generate Newton's forward difference table.
        
        Args:
            x_points: List of equispaced x coordinates.
            y_points: List of y coordinates.
            
        Returns:
            SimulationData containing the difference table.
        """
        x_points = np.array(kwargs.get("x_points") or [], dtype=float)
        y_points = np.array(kwargs.get("y_points") or [], dtype=float)

        if not self.validate_input(x_points=x_points, y_points=y_points):
            raise ValueError("Invalid input points for Newton Difference Table (must be equispaced).")

        n = len(x_points)
        table = np.zeros((n, n))
        table[:, 0] = y_points

        for j in range(1, n):
            for i in range(n - j):
                table[i, j] = table[i + 1, j - 1] - table[i, j - 1]

        self._steps = []
        for j in range(1, n):
            self._steps.append(NumericalStep(
                step_idx=j,
                value=0.0,
                details={
                    "description": f"Forward differences of order {j}",
                    "differences": table[:n-j, j].tolist()
                }
            ))

        # Coefficients for Newton Forward Interpolation are table[0, j] / (j! * h^j)
        # But often just the table[0, j] are called coefficients in this context
        coefficients = table[0, :].tolist()

        return SimulationData(
            title="Newton Forward Difference Table",
            x_data=x_points.tolist(),
            y_data=y_points.tolist(),
            metadata={
                "difference_table": table.tolist(),
                "coefficients": coefficients,
                "h_value": float(x_points[1] - x_points[0])
            }
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
        
        h = np.diff(x_points)
        if not np.allclose(h, h[0]):
            return False
            
        return True


class NewtonDividedDifferenceSolver(Solver):
    """Newton's Divided Difference Interpolation Solver."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute Newton's Divided Difference interpolation.
        
        Args:
            x_points: List of x coordinates.
            y_points: List of y coordinates.
            target_x: Optional x value(s) to interpolate.
            
        Returns:
            SimulationData containing the interpolation results.
        """
        x_points = np.array(kwargs.get("x_points") or [], dtype=float)
        y_points = np.array(kwargs.get("y_points") or [], dtype=float)
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

        def evaluate(x: float) -> float:
            res = coef[0]
            for i in range(1, n):
                term = coef[i]
                for j in range(i):
                    term *= (x - x_points[j])
                res += term
            return res

        result_y = []
        x_data = []
        if target_x is not None:
            if isinstance(target_x, (int, float)):
                x_data = [float(target_x)]
                result_y = [evaluate(float(target_x))]
            else:
                x_data = [float(x) for x in target_x]
                result_y = [evaluate(x) for x in x_data]
        else:
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
        
        try:
            if len(x_points) != len(y_points) or len(x_points) < 2:
                return False
        except TypeError:
            return False
            
        return True


class InterpolationSolver(NewtonDividedDifferenceSolver):
    """Alias for NewtonDividedDifferenceSolver for backward compatibility."""
    pass


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
        x_points = np.array(kwargs.get("x_points") or [], dtype=float)
        y_points = np.array(kwargs.get("y_points") or [], dtype=float)
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

        h = np.diff(x_points)
        if not np.allclose(h, h[0]):
            return False

        n = n_points - 1
        if method == "simpson13" and n % 2 != 0:
            return False
        if method == "simpson38" and n % 3 != 0:
            return False

        return True


class MidpointSolver(Solver):
    """Composite Midpoint Rule Solver."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute composite midpoint rule.
        
        Args:
            f: Function to integrate.
            a: Start of interval.
            b: End of interval.
            n: Number of sub-intervals.
            
        Returns:
            SimulationData containing the integration result.
        """
        f = kwargs.get("f")
        a = float(kwargs.get("a", 0))
        b = float(kwargs.get("b", 0))
        n = int(kwargs.get("n", 1))

        if not self.validate_input(**kwargs):
            raise ValueError("Invalid input for Midpoint Rule.")

        h = (b - a) / n
        result = 0.0
        self._steps = []

        for i in range(n):
            mid = a + (i + 0.5) * h
            val = f(mid)
            result += val
            self._steps.append(NumericalStep(
                step_idx=i + 1,
                value=val,
                details={"x_mid": mid, "h": h}
            ))

        result *= h

        return SimulationData(
            title="Composite Midpoint Rule",
            x_data=[a, b],
            y_data=[result],
            metadata={"n": n, "h": h, "total_integral": result}
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        f = kwargs.get("f")
        a = kwargs.get("a")
        b = kwargs.get("b")
        n = kwargs.get("n")
        return callable(f) and a is not None and b is not None and n is not None and n > 0


class TrapezoidalSolver(Solver):
    """Trapezoidal Rule Solver (supports both function and data points)."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        f = kwargs.get("f")
        x_points = kwargs.get("x_points")
        y_points = kwargs.get("y_points")

        if f is not None:
            a = float(kwargs.get("a", 0))
            b = float(kwargs.get("b", 0))
            n = int(kwargs.get("n", 1))
            h = (b - a) / n
            x_data = np.linspace(a, b, n + 1)
            y_data = np.array([f(x) for x in x_data])
        elif x_points is not None and y_points is not None:
            x_data = np.array(x_points, dtype=float)
            y_data = np.array(y_points, dtype=float)
            n = len(x_data) - 1
            h = (x_data[-1] - x_data[0]) / n
        else:
            raise ValueError("Either function 'f' or 'x_points'/'y_points' must be provided.")

        result = (h / 2) * (y_data[0] + 2 * np.sum(y_data[1:-1]) + y_data[-1])
        
        self._steps = [NumericalStep(
            step_idx=1,
            value=result,
            details={"n": n, "h": h}
        )]

        return SimulationData(
            title="Trapezoidal Rule",
            x_data=x_data.tolist(),
            y_data=[result],
            metadata={"total_integral": result}
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        f = kwargs.get("f")
        x_points = kwargs.get("x_points")
        y_points = kwargs.get("y_points")
        
        if f is not None:
            return callable(f) and kwargs.get("a") is not None and kwargs.get("b") is not None and kwargs.get("n", 0) > 0
        
        if x_points is not None and y_points is not None:
            return len(x_points) == len(y_points) and len(x_points) >= 2
            
        return False


class SimpsonsRuleSolver(Solver):
    """Simpson's Rule Solver (1/3 and 3/8)."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        method = kwargs.get("method", "1/3")
        f = kwargs.get("f")
        x_points = kwargs.get("x_points")
        y_points = kwargs.get("y_points")

        if f is not None:
            a = float(kwargs.get("a", 0))
            b = float(kwargs.get("b", 0))
            n = int(kwargs.get("n", 2))
            h = (b - a) / n
            x_data = np.linspace(a, b, n + 1)
            y_data = np.array([f(x) for x in x_data])
        elif x_points is not None and y_points is not None:
            x_data = np.array(x_points, dtype=float)
            y_data = np.array(y_points, dtype=float)
            n = len(x_data) - 1
            h = (x_data[-1] - x_data[0]) / n
        else:
            raise ValueError("Either function 'f' or 'x_points'/'y_points' must be provided.")

        if method == "1/3":
            if n % 2 != 0:
                raise ValueError("Simpson's 1/3 rule requires an even number of intervals.")
            result = (h / 3) * (y_data[0] + 4 * np.sum(y_data[1:-1:2]) + 2 * np.sum(y_data[2:-2:2]) + y_data[-1])
        elif method == "3/8":
            if n % 3 != 0:
                raise ValueError("Simpson's 3/8 rule requires intervals to be a multiple of 3.")
            sum_val = y_data[0] + y_data[-1]
            for i in range(1, n):
                if i % 3 == 0:
                    sum_val += 2 * y_data[i]
                else:
                    sum_val += 3 * y_data[i]
            result = (3 * h / 8) * sum_val
        else:
            raise ValueError(f"Unsupported Simpson's method: {method}")

        self._steps = [NumericalStep(step_idx=1, value=result, details={"method": method, "n": n, "h": h})]

        return SimulationData(
            title=f"Simpson's {method} Rule",
            x_data=x_data.tolist(),
            y_data=[result],
            metadata={"total_integral": result, "method": method}
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        # Similar validation to Trapezoidal but with n constraints
        method = kwargs.get("method", "1/3")
        f = kwargs.get("f")
        x_points = kwargs.get("x_points")
        y_points = kwargs.get("y_points")
        
        n = 0
        if f is not None:
            if not callable(f): return False
            n = kwargs.get("n", 0)
        elif x_points is not None and y_points is not None:
            if len(x_points) != len(y_points) or len(x_points) < 2: return False
            n = len(x_points) - 1
        else:
            return False

        if method == "1/3" and n % 2 != 0: return False
        if method == "3/8" and n % 3 != 0: return False
        return True


class GaussianQuadratureSolver(Solver):
    """Gaussian Quadrature Solver (2-point and 3-point)."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        f = kwargs.get("f")
        a = float(kwargs.get("a", -1))
        b = float(kwargs.get("b", 1))
        points = int(kwargs.get("points", 2))

        if not callable(f):
            raise ValueError("A function 'f' must be provided.")

        if points == 2:
            nodes = [-1/np.sqrt(3), 1/np.sqrt(3)]
            weights = [1.0, 1.0]
        elif points == 3:
            nodes = [-np.sqrt(0.6), 0.0, np.sqrt(0.6)]
            weights = [5/9, 8/9, 5/9]
        else:
            raise ValueError("Only 2-point and 3-point Gaussian Quadrature are supported.")

        # Transform nodes from [-1, 1] to [a, b]
        # x = (b-a)/2 * t + (b+a)/2
        transformed_nodes = [(b - a) / 2 * t + (b + a) / 2 for t in nodes]
        
        result = 0.0
        self._steps = []
        for i, (t_node, w) in enumerate(zip(transformed_nodes, weights)):
            val = f(t_node)
            term = w * val
            result += term
            self._steps.append(NumericalStep(
                step_idx=i + 1,
                value=term,
                details={"node": t_node, "weight": w, "f_val": val}
            ))

        result *= (b - a) / 2

        return SimulationData(
            title=f"Gaussian Quadrature ({points}-point)",
            x_data=transformed_nodes,
            y_data=[result],
            metadata={"points": points, "total_integral": result, "weights": weights, "nodes": nodes}
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        f = kwargs.get("f")
        points = kwargs.get("points", 2)
        return callable(f) and points in [2, 3]


class NumericalDifferentiationSolver(Solver):
    """Numerical Differentiation Solver."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute numerical differentiation.
        
        Args:
            f: Function to differentiate.
            x: Point at which to differentiate.
            h: Step size.
            method: 'forward', 'backward', or 'central'.
            
        Returns:
            SimulationData containing the derivative result.
        """
        f = kwargs.get("f")
        x = float(kwargs.get("x", 0))
        h = float(kwargs.get("h", 1e-5))
        method = kwargs.get("method", "central").lower()

        if not callable(f):
            # Support for data points could be added here
            raise ValueError("A function 'f' must be provided.")

        if method == "forward":
            result = (f(x + h) - f(x)) / h
        elif method == "backward":
            result = (f(x) - f(x - h)) / h
        elif method == "central":
            result = (f(x + h) - f(x - h)) / (2 * h)
        else:
            raise ValueError(f"Unsupported differentiation method: {method}")

        self._steps = [NumericalStep(
            step_idx=1,
            value=result,
            details={"method": method, "x": x, "h": h}
        )]

        return SimulationData(
            title=f"Numerical Differentiation ({method})",
            x_data=[x],
            y_data=[result],
            metadata={"method": method, "derivative": result}
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        f = kwargs.get("f")
        method = kwargs.get("method", "central").lower()
        return callable(f) and method in ["forward", "backward", "central"]
