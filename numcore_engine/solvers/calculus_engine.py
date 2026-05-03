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

        def get_polynomial_str() -> str:
            terms = []
            for i in range(n):
                if abs(y_points[i]) < 1e-12:
                    continue
                num_parts = []
                den_val = 1.0
                for j in range(n):
                    if i != j:
                        num_parts.append(f"(x - {x_points[j]:.4g})")
                        den_val *= (x_points[i] - x_points[j])
                
                term_coef = y_points[i] / den_val
                if not num_parts:
                    terms.append(f"{term_coef:.4g}")
                else:
                    terms.append(f"{term_coef:.4g} * {' * '.join(num_parts)}")
            return " + ".join(terms) if terms else "0"

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
            metadata={
                "method": "Lagrange",
                "polynomial_str": get_polynomial_str(),
                "target_x": x_data[0] if target_x is not None else None,
                "interpolated_y": result_y[0] if target_x is not None else None
            }
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
        h = float(x_points[1] - x_points[0])
        table = np.zeros((n, n))
        table[:, 0] = y_points

        for j in range(1, n):
            for i in range(n - j):
                table[i, j] = table[i + 1, j - 1] - table[i, j - 1]

        self._steps = []
        for i in range(n):
            row_diffs = {}
            for j in range(1, n):
                if i < n - j:
                    row_diffs[f"diff_{j}"] = table[i, j]
            
            self._steps.append(NumericalStep(
                step_idx=i,
                value=y_points[i],
                details={
                    "x": x_points[i],
                    "y": y_points[i],
                    **row_diffs
                }
            ))

        # Calculate divided difference table for metadata requirement

        # Coefficients for Newton Forward Interpolation are table[0, j] / (j! * h^j)
        # But often just the table[0, j] are called coefficients in this context
        coefficients = table[0, :].tolist()

        return SimulationData(
            title="Newton Forward Difference Table",
            x_data=x_points.tolist(),
            y_data=y_points.tolist(),
            metadata={
                "difference_table": table.tolist(),
                "dd_table": table.tolist(),
                "coefficients": coefficients,
                "h": h
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
        table = np.zeros((n, n))
        table[:, 0] = y_points

        for j in range(1, n):
            for i in range(n - j):
                table[i, j] = (table[i + 1, j - 1] - table[i, j - 1]) / (x_points[i + j] - x_points[i])

        self._steps = []
        for i in range(n):
            row_diffs = {}
            for j in range(1, n):
                if i < n - j:
                    row_diffs[f"dd_{j}"] = table[i, j]
            
            self._steps.append(NumericalStep(
                step_idx=i,
                value=y_points[i],
                details={
                    "x": x_points[i],
                    "y": y_points[i],
                    **row_diffs
                }
            ))

        coef = table[0, :].tolist()

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
            metadata={
                "coefficients": coef,
                "dd_table": table.tolist(),
                "target_x": x_data[0] if target_x is not None else None,
                "interpolated_y": result_y[0] if target_x is not None else None
            }
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


class LinearInterpolationSolver(Solver):
    """Linear Interpolation Solver."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute linear interpolation.
        
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

        # Sort points by x
        sort_idx = np.argsort(x_points)
        x_points = x_points[sort_idx]
        y_points = y_points[sort_idx]

        self._steps = []

        def evaluate(x: float) -> float:
            if x <= x_points[0]:
                i = 0
            elif x >= x_points[-1]:
                i = len(x_points) - 2
            else:
                i = np.searchsorted(x_points, x) - 1
            
            x0, x1 = x_points[i], x_points[i+1]
            y0, y1 = y_points[i], y_points[i+1]
            
            val = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
            return val

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
            title="Linear Interpolation",
            x_data=x_data,
            y_data=result_y,
            metadata={
                "method": "Linear",
                "target_x": x_data[0] if target_x is not None else None,
                "interpolated_y": result_y[0] if target_x is not None else None
            }
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


class CubicSplineSolver(Solver):
    """Natural Cubic Spline Interpolation Solver."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        """
        Execute natural cubic spline interpolation.
        
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
            raise ValueError("Invalid input points for interpolation (need at least 3 points).")

        # Sort points by x
        sort_idx = np.argsort(x_points)
        x = x_points[sort_idx]
        y = y_points[sort_idx]
        n = len(x) - 1

        h = np.diff(x)
        alpha = np.zeros(n)
        for i in range(1, n):
            alpha[i] = 3/h[i] * (y[i+1] - y[i]) - 3/h[i-1] * (y[i] - y[i-1])

        l = np.ones(n+1)
        mu = np.zeros(n+1)
        z = np.zeros(n+1)

        for i in range(1, n):
            l[i] = 2 * (x[i+1] - x[i-1]) - h[i-1] * mu[i-1]
            mu[i] = h[i] / l[i]
            z[i] = (alpha[i] - h[i-1] * z[i-1]) / l[i]

        c = np.zeros(n+1)
        b = np.zeros(n)
        d = np.zeros(n)

        for j in range(n-1, -1, -1):
            c[j] = z[j] - mu[j] * c[j+1]
            b[j] = (y[j+1] - y[j]) / h[j] - h[j] * (c[j+1] + 2*c[j]) / 3
            d[j] = (c[j+1] - c[j]) / (3 * h[j])

        a = y[:-1]

        self._steps = []

        def evaluate(tx: float) -> float:
            if tx <= x[0]:
                i = 0
            elif tx >= x[-1]:
                i = n - 1
            else:
                i = np.searchsorted(x, tx) - 1
                if i < 0: i = 0
                if i >= n: i = n - 1
            
            dx = tx - x[i]
            return a[i] + b[i]*dx + c[i]*dx**2 + d[i]*dx**3

        result_y = []
        x_data = []
        if target_x is not None:
            if isinstance(target_x, (int, float)):
                x_data = [float(target_x)]
                result_y = [evaluate(float(target_x))]
            else:
                x_data = [float(tx) for tx in target_x]
                result_y = [evaluate(tx) for x in x_data]
        else:
            x_data = x.tolist()
            result_y = y.tolist()

        return SimulationData(
            title="Cubic Spline Interpolation",
            x_data=x_data,
            y_data=result_y,
            metadata={
                "method": "Cubic Spline",
                "a": a.tolist(),
                "b": b.tolist(),
                "c": c[:-1].tolist(),
                "d": d.tolist(),
                "target_x": x_data[0] if target_x is not None else None,
                "interpolated_y": result_y[0] if target_x is not None else None
            }
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        x_points = kwargs.get("x_points")
        y_points = kwargs.get("y_points")
        
        if x_points is None or y_points is None:
            return False
        
        try:
            if len(x_points) != len(y_points) or len(x_points) < 3:
                return False
        except TypeError:
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
        method = kwargs.get("method", "trapezoidal").lower()
        
        if method == "trapezoidal":
            solver: Solver = TrapezoidalSolver()
        elif method == "simpson13":
            solver = SimpsonOneThirdSolver()
        elif method == "simpson38":
            solver = SimpsonThreeEighthsSolver()
        else:
            raise ValueError(f"Unsupported integration method: {method}")

        result = solver.solve(**kwargs)
        self._steps = solver.get_steps()
        return result

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        method = kwargs.get("method", "trapezoidal").lower()
        if method == "trapezoidal":
            return TrapezoidalSolver().validate_input(**kwargs)
        elif method == "simpson13":
            return SimpsonOneThirdSolver().validate_input(**kwargs)
        elif method == "simpson38":
            return SimpsonThreeEighthsSolver().validate_input(**kwargs)
        return False


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
        
        # Construct weighted sum string
        terms = [f"{y_data[0]:.4f}"]
        for y in y_data[1:-1]:
            terms.append(f"2*({y:.4f})")
        terms.append(f"{y_data[-1]:.4f}")
        weighted_sum_str = f"({h:.4f}/2) * [" + " + ".join(terms) + "]"

        self._steps = []
        for i in range(n + 1):
            weight = 1 if (i == 0 or i == n) else 2
            self._steps.append(NumericalStep(
                step_idx=i,
                value=y_data[i],
                details={
                    "x": x_data[i],
                    "y": y_data[i],
                    "weight": weight,
                    "weighted_y": weight * y_data[i]
                }
            ))

        return SimulationData(
            title="Trapezoidal Rule",
            x_data=x_data.tolist(),
            y_data=[result],
            metadata={
                "total_integral": result,
                "h_value": h,
                "weighted_sum_str": weighted_sum_str
            }
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
            if len(x_points) != len(y_points) or len(x_points) < 2:
                return False
            h = np.diff(x_points)
            return np.allclose(h, h[0])
            
        return False


class SimpsonOneThirdSolver(Solver):
    """Simpson's 1/3 Rule Solver."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
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

        if n % 2 != 0:
            raise ValueError("Simpson's 1/3 rule requires an even number of intervals (n).")

        result = (h / 3) * (y_data[0] + 4 * np.sum(y_data[1:-1:2]) + 2 * np.sum(y_data[2:-2:2]) + y_data[-1])
        
        # Construct weighted sum string
        terms = [f"{y_data[0]:.4f}"]
        for i in range(1, n):
            weight = 4 if i % 2 != 0 else 2
            terms.append(f"{weight}*({y_data[i]:.4f})")
        terms.append(f"{y_data[-1]:.4f}")
        weighted_sum_str = f"({h:.4f}/3) * [" + " + ".join(terms) + "]"

        self._steps = []
        for i in range(n + 1):
            if i == 0 or i == n:
                weight = 1
            elif i % 2 != 0:
                weight = 4
            else:
                weight = 2
            
            self._steps.append(NumericalStep(
                step_idx=i,
                value=y_data[i],
                details={
                    "x": x_data[i],
                    "y": y_data[i],
                    "weight": weight,
                    "weighted_y": weight * y_data[i]
                }
            ))

        return SimulationData(
            title="Simpson's 1/3 Rule",
            x_data=x_data.tolist(),
            y_data=[result],
            metadata={
                "total_integral": result,
                "h_value": h,
                "weighted_sum_str": weighted_sum_str,
                "n_even_check": True
            }
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
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
            h = np.diff(x_points)
            if not np.allclose(h, h[0]): return False
        else:
            return False

        return n > 0 and n % 2 == 0


class SimpsonThreeEighthsSolver(Solver):
    """Simpson's 3/8 Rule Solver."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        f = kwargs.get("f")
        x_points = kwargs.get("x_points")
        y_points = kwargs.get("y_points")

        if f is not None:
            a = float(kwargs.get("a", 0))
            b = float(kwargs.get("b", 0))
            n = int(kwargs.get("n", 3))
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

        if n % 3 != 0:
            raise ValueError("Simpson's 3/8 rule requires intervals (n) to be a multiple of 3.")

        sum_val = y_data[0] + y_data[-1]
        terms = [f"{y_data[0]:.4f}"]
        for i in range(1, n):
            if i % 3 == 0:
                sum_val += 2 * y_data[i]
                terms.append(f"2*({y_data[i]:.4f})")
            else:
                sum_val += 3 * y_data[i]
                terms.append(f"3*({y_data[i]:.4f})")
        terms.append(f"{y_data[-1]:.4f}")
        
        result = (3 * h / 8) * sum_val
        weighted_sum_str = f"(3*{h:.4f}/8) * [" + " + ".join(terms) + "]"

        self._steps = []
        for i in range(n + 1):
            if i == 0 or i == n:
                weight = 1
            elif i % 3 == 0:
                weight = 2
            else:
                weight = 3
            
            self._steps.append(NumericalStep(
                step_idx=i,
                value=y_data[i],
                details={
                    "x": x_data[i],
                    "y": y_data[i],
                    "weight": weight,
                    "weighted_y": weight * y_data[i]
                }
            ))

        return SimulationData(
            title="Simpson's 3/8 Rule",
            x_data=x_data.tolist(),
            y_data=[result],
            metadata={
                "total_integral": result,
                "h_value": h,
                "weighted_sum_str": weighted_sum_str,
                "n_mod3_check": True
            }
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
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
            h = np.diff(x_points)
            if not np.allclose(h, h[0]): return False
        else:
            return False

        return n > 0 and n % 3 == 0


class SimpsonsRuleSolver(Solver):
    """Simpson's Rule Solver (1/3 and 3/8)."""

    def __init__(self) -> None:
        self._steps: List[NumericalStep] = []

    def solve(self, **kwargs: Any) -> SimulationData:
        method = kwargs.get("method", "1/3")
        
        if method == "1/3":
            solver: Solver = SimpsonOneThirdSolver()
        elif method == "3/8":
            solver = SimpsonThreeEighthsSolver()
        else:
            raise ValueError(f"Unsupported Simpson's method: {method}")

        result = solver.solve(**kwargs)
        self._steps = solver.get_steps()
        return result

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        method = kwargs.get("method", "1/3")
        if method == "1/3":
            return SimpsonOneThirdSolver().validate_input(**kwargs)
        elif method == "3/8":
            return SimpsonThreeEighthsSolver().validate_input(**kwargs)
        return False


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
            metadata={
                "method": method,
                "derivative": result,
                "h_value": h
            }
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps

    def validate_input(self, **kwargs: Any) -> bool:
        f = kwargs.get("f")
        method = kwargs.get("method", "central").lower()
        return callable(f) and method in ["forward", "backward", "central"]
