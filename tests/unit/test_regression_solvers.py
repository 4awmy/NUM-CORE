import pytest
import numpy as np
from numcore_engine.solvers.regression_solvers import LeastSquaresSolver


def test_least_squares_solver_basic():
    solver = LeastSquaresSolver()
    # Points: (1, 2), (2, 4), (3, 6) -> y = 2x + 0
    x = [1, 2, 3]
    y = [2, 4, 6]
    result = solver.solve(x_points=x, y_points=y)

    assert result.metadata["slope"] == pytest.approx(2.0)
    assert result.metadata["intercept"] == pytest.approx(0.0)
    assert result.metadata["method"] == "Least Squares"


def test_least_squares_solver_noisy():
    solver = LeastSquaresSolver()
    # Points: (1, 2.1), (2, 3.9), (3, 6.1) -> roughly y = 2x
    x = [1, 2, 3]
    y = [2.1, 3.9, 6.1]
    result = solver.solve(x_points=x, y_points=y)

    # m = (3*(1*2.1 + 2*3.9 + 3*6.1) - (1+2+3)*(2.1+3.9+6.1)) / (3*(1+4+9) - 6^2)
    # m = (3*(2.1 + 7.8 + 18.3) - 6*12.1) / (3*14 - 36)
    # m = (3*28.2 - 72.6) / (42 - 36)
    # m = (84.6 - 72.6) / 6 = 12 / 6 = 2.0
    # c = (12.1 - 2.0*6) / 3 = (12.1 - 12) / 3 = 0.1 / 3 = 0.0333...
    assert result.metadata["slope"] == pytest.approx(2.0)
    assert result.metadata["intercept"] == pytest.approx(0.03333333333333333)


def test_least_squares_invalid_input():
    solver = LeastSquaresSolver()

    with pytest.raises(ValueError):
        solver.solve(x_points=[1, 2], y_points=[1])  # Mismatched lengths

    with pytest.raises(ValueError):
        solver.solve(x_points=[1, 1], y_points=[1, 2])  # Vertical line (denominator zero)
