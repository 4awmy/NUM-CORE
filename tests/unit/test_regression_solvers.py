import pytest
import numpy as np
from numcore_engine.solvers.regression_solvers import LeastSquaresSolver, CurveFittingSolver


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

    assert result.metadata["slope"] == pytest.approx(2.0)
    assert result.metadata["intercept"] == pytest.approx(0.03333333333333333)


def test_least_squares_invalid_input():
    solver = LeastSquaresSolver()

    with pytest.raises(ValueError):
        solver.solve(x_points=[1, 2], y_points=[1])  # Mismatched lengths

    with pytest.raises(ValueError):
        solver.solve(x_points=[1, 1], y_points=[1, 2])  # Vertical line (denominator zero)


def test_curve_fitting_quadratic():
    solver = CurveFittingSolver()
    x = [0, 1, 2]
    y = [1, 3, 7]
    result = solver.solve(x_points=x, y_points=y, model="quadratic")
    assert result.metadata["a0"] == pytest.approx(1.0)
    assert result.metadata["a1"] == pytest.approx(1.0)
    assert result.metadata["a2"] == pytest.approx(1.0)


def test_curve_fitting_power():
    solver = CurveFittingSolver()
    x = [1, 2, 3, 4, 5]
    a, b = 2.0, 1.5
    y = [a * (xi**b) for xi in x]
    result = solver.solve(x_points=x, y_points=y, model="power")
    assert result.metadata["a"] == pytest.approx(a)
    assert result.metadata["b"] == pytest.approx(b)


def test_curve_fitting_exponential():
    solver = CurveFittingSolver()
    x = [1, 2, 3, 4, 5]
    a, b = 2.0, 0.5
    y = [a * np.exp(b * xi) for xi in x]
    result = solver.solve(x_points=x, y_points=y, model="exponential")
    assert result.metadata["a"] == pytest.approx(a)
    assert result.metadata["b"] == pytest.approx(b)


def test_curve_fitting_growth():
    solver = CurveFittingSolver()
    x = [1, 2, 3, 4, 5]
    a, b = 2.0, 0.5
    y = [xi / (a + b * xi) for xi in x]
    result = solver.solve(x_points=x, y_points=y, model="growth")
    assert result.metadata["a"] == pytest.approx(a)
    assert result.metadata["b"] == pytest.approx(b)
