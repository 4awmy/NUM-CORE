import pytest
import numpy as np
from numcore_engine.solvers.calculus_engine import InterpolationSolver, IntegrationSolver


def test_interpolation_solver_basic():
    solver = InterpolationSolver()
    x = [0, 1, 2]
    y = [1, 3, 2]
    # f(x) = 1 + 2x - 1.5x(x-1) = 1 + 2x - 1.5x^2 + 1.5x = -1.5x^2 + 3.5x + 1
    # f(0.5) = -1.5(0.25) + 3.5(0.5) + 1 = -0.375 + 1.75 + 1 = 2.375
    
    data = solver.solve(x_points=x, y_points=y, target_x=0.5)
    assert np.isclose(data.y_data[0], 2.375)
    assert len(solver.get_steps()) == 3


def test_interpolation_solver_multiple_points():
    solver = InterpolationSolver()
    x = [0, 1, 2]
    y = [1, 3, 2]
    target_x = [0.5, 1.5]
    
    data = solver.solve(x_points=x, y_points=y, target_x=target_x)
    assert len(data.y_data) == 2
    assert np.isclose(data.y_data[0], 2.375)
    # f(1.5) = -1.5(2.25) + 3.5(1.5) + 1 = -3.375 + 5.25 + 1 = 2.875
    assert np.isclose(data.y_data[1], 2.875)


def test_integration_solver_trapezoidal():
    solver = IntegrationSolver()
    x = [0, 1, 2]
    y = [1, 4, 9] # x^2 + 1? No, y = (x+1)^2? No.
    # Trapezoidal: (1/2) * (1 + 2*4 + 9) = 0.5 * 18 = 9
    
    data = solver.solve(x_points=x, y_points=y, method="trapezoidal")
    assert np.isclose(data.y_data[0], 9.0)


def test_integration_solver_simpson13():
    solver = IntegrationSolver()
    x = [0, 1, 2]
    y = [1, 4, 9]
    # Simpson 1/3: (1/3) * (1 + 4*4 + 9) = (1/3) * 26 = 8.666...
    
    data = solver.solve(x_points=x, y_points=y, method="simpson13")
    assert np.isclose(data.y_data[0], 26/3)


def test_integration_solver_simpson38():
    solver = IntegrationSolver()
    x = [0, 1, 2, 3]
    y = [1, 8, 27, 64]
    # h = 1
    # Simpson 3/8: (3*1/8) * (1 + 3*8 + 3*27 + 64) = (3/8) * (1 + 24 + 81 + 64) = (3/8) * 170 = 63.75
    
    data = solver.solve(x_points=x, y_points=y, method="simpson38")
    assert np.isclose(data.y_data[0], 63.75)


def test_integration_solver_invalid_n():
    solver = IntegrationSolver()
    x = [0, 1]
    y = [1, 2]
    
    with pytest.raises(ValueError):
        solver.solve(x_points=x, y_points=y, method="simpson13")
    
    with pytest.raises(ValueError):
        solver.solve(x_points=x, y_points=y, method="simpson38")


def test_integration_solver_non_uniform():
    solver = IntegrationSolver()
    x = [0, 1, 3]
    y = [1, 2, 4]
    
    assert solver.validate_input(x_points=x, y_points=y, method="trapezoidal") is False
