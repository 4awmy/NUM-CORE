import pytest
import numpy as np
from numcore_engine.solvers.calculus_engine import (
    LagrangeInterpolationSolver,
    NewtonDividedDifferenceSolver,
    LinearInterpolationSolver,
    CubicSplineSolver,
    NewtonDifferenceTableSolver
)

def test_lagrange_metadata():
    solver = LagrangeInterpolationSolver()
    x = [0, 1, 2]
    y = [1, 3, 2]
    data = solver.solve(x_points=x, y_points=y)
    assert "polynomial_str" in data.metadata
    assert isinstance(data.metadata["polynomial_str"], str)
    # f(x) = 1*L0 + 3*L1 + 2*L2
    # L0 = (x-1)(x-2)/(0-1)(0-2) = 0.5(x-1)(x-2)
    # L1 = (x-0)(x-2)/(1-0)(1-2) = -x(x-2)
    # L2 = (x-0)(x-1)/(2-0)(2-1) = 0.5x(x-1)
    # P(x) = 0.5(x-1)(x-2) - 3x(x-2) + x(x-1)
    # P(x) = 0.5(x^2-3x+2) - 3(x^2-2x) + (x^2-x)
    # P(x) = 0.5x^2 - 1.5x + 1 - 3x^2 + 6x + x^2 - x
    # P(x) = -1.5x^2 + 3.5x + 1
    print(data.metadata["polynomial_str"])

def test_newton_divided_difference_table():
    solver = NewtonDividedDifferenceSolver()
    x = [0, 1, 2]
    y = [1, 3, 2]
    data = solver.solve(x_points=x, y_points=y)
    assert "dd_table" in data.metadata
    table = data.metadata["dd_table"]
    assert len(table) == 3
    assert table[0][0] == 1
    assert table[1][0] == 3
    assert table[2][0] == 2
    # f[0,1] = (3-1)/(1-0) = 2
    # f[1,2] = (2-3)/(2-1) = -1
    # f[0,1,2] = (-1-2)/(2-0) = -1.5
    assert table[0][1] == 2
    assert table[1][1] == -1
    assert table[0][2] == -1.5

def test_linear_interpolation():
    solver = LinearInterpolationSolver()
    x = [0, 1, 2]
    y = [0, 2, 0]
    # x=0.5 -> y=1
    # x=1.5 -> y=1
    data = solver.solve(x_points=x, y_points=y, target_x=[0.5, 1.5])
    assert np.isclose(data.y_data[0], 1.0)
    assert np.isclose(data.y_data[1], 1.0)
    
    # Out of bounds
    data_out = solver.solve(x_points=x, y_points=y, target_x=[-1, 3])
    assert np.isclose(data_out.y_data[0], -2.0) # Extrapolation 0 + (2-0)*( -1 - 0)/(1-0) = -2
    assert np.isclose(data_out.y_data[1], -2.0) # Extrapolation 2 + (0-2)*( 3 - 1)/(2-1) = 2 - 4 = -2

def test_cubic_spline_interpolation():
    solver = CubicSplineSolver()
    x = [0, 1, 2]
    y = [0, 1, 0]
    # Natural spline: S''(0) = S''(2) = 0
    data = solver.solve(x_points=x, y_points=y, target_x=0.5)
    # For x=[0,1,2], y=[0,1,0], natural spline:
    # h0=1, h1=1
    # alpha1 = 3/1*(0-1) - 3/1*(1-0) = -3 - 3 = -6
    # l0=1, mu0=0, z0=0
    # l1 = 2*(2-0) - 1*0 = 4
    # mu1 = 1/4 = 0.25
    # z1 = (-6 - 1*0)/4 = -1.5
    # l2 = 1
    # c2 = 0
    # c1 = z1 - mu1*c2 = -1.5
    # c0 = z0 - mu0*c1 = 0
    # b0 = (1-0)/1 - 1*(c1 + 2*c0)/3 = 1 - (-1.5)/3 = 1 + 0.5 = 1.5
    # d0 = (c1 - c0)/(3*1) = -1.5/3 = -0.5
    # S0(x) = 0 + 1.5x + 0x^2 - 0.5x^3 = 1.5x - 0.5x^3
    # S0(0.5) = 1.5*0.5 - 0.5*0.125 = 0.75 - 0.0625 = 0.6875
    assert np.isclose(data.y_data[0], 0.6875)


def test_cubic_spline_interpolation_list_target():
    solver = CubicSplineSolver()
    x = [0, 1, 2]
    y = [0, 1, 0]
    # S0(0.5) = 0.6875, S1(1.5) = symmetric = 0.6875
    data = solver.solve(x_points=x, y_points=y, target_x=[0.5, 1.5])
    assert len(data.y_data) == 2
    assert np.isclose(data.y_data[0], 0.6875)
    assert np.isclose(data.y_data[1], 0.6875)


def test_cubic_spline_invalid():
    solver = CubicSplineSolver()
    # Need at least 3 points
    with pytest.raises(ValueError):
        solver.solve(x_points=[0, 1], y_points=[0, 1])
