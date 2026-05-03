import pytest
import numpy as np
from numcore_engine.solvers.calculus_engine import (
    LagrangeInterpolationSolver,
    NewtonDifferenceTableSolver,
    NewtonDividedDifferenceSolver,
    InterpolationSolver,
    IntegrationSolver,
    MidpointSolver,
    TrapezoidalSolver,
    SimpsonOneThirdSolver,
    SimpsonThreeEighthsSolver,
    SimpsonsRuleSolver,
    GaussianQuadratureSolver,
    NumericalDifferentiationSolver
)


def test_simpson_one_third_solver():
    solver = SimpsonOneThirdSolver()
    f = lambda x: x**2
    # Integral of x^2 from 0 to 2 is 8/3
    data = solver.solve(f=f, a=0, b=2, n=2)
    assert np.isclose(data.y_data[0], 8/3)
    assert data.metadata["n_even_check"] is True
    assert "weighted_sum_str" in data.metadata

    # Data points
    x = [0, 1, 2]
    y = [0, 1, 4]
    data_pts = solver.solve(x_points=x, y_points=y)
    assert np.isclose(data_pts.y_data[0], 8/3)

    # Invalid n
    with pytest.raises(ValueError):
        solver.solve(f=f, a=0, b=2, n=3)


def test_simpson_three_eighths_solver():
    solver = SimpsonThreeEighthsSolver()
    f = lambda x: x**3
    # Integral of x^3 from 0 to 3 is 3^4 / 4 = 81/4 = 20.25
    data = solver.solve(f=f, a=0, b=3, n=3)
    assert np.isclose(data.y_data[0], 20.25)
    assert data.metadata["n_mod3_check"] is True
    assert "weighted_sum_str" in data.metadata

    # Data points
    x = [0, 1, 2, 3]
    y = [0, 1, 8, 27]
    data_pts = solver.solve(x_points=x, y_points=y)
    assert np.isclose(data_pts.y_data[0], 20.25)

    # Invalid n
    with pytest.raises(ValueError):
        solver.solve(f=f, a=0, b=3, n=2)


def test_lagrange_interpolation_basic():
    solver = LagrangeInterpolationSolver()
    x = [0, 1, 2]
    y = [1, 3, 2]
    # f(x) = -1.5x^2 + 3.5x + 1
    # f(0.5) = 2.375
    
    data = solver.solve(x_points=x, y_points=y, target_x=0.5)
    assert np.isclose(data.y_data[0], 2.375)


def test_newton_divided_difference_basic():
    solver = NewtonDividedDifferenceSolver()
    x = [0, 1, 2]
    y = [1, 3, 2]
    
    data = solver.solve(x_points=x, y_points=y, target_x=0.5)
    assert np.isclose(data.y_data[0], 2.375)
    assert len(solver.get_steps()) == 3
    assert "coefficients" in data.metadata


def test_newton_difference_table_basic():
    solver = NewtonDifferenceTableSolver()
    x = [0, 1, 2, 3]
    y = [1, 8, 27, 64] # y = (x+1)^3? No, y = x^3 + ... wait.
    # y = [1, 8, 27, 64]
    # diff1: [7, 19, 37]
    # diff2: [12, 18]
    # diff3: [6]
    
    data = solver.solve(x_points=x, y_points=y)
    table = data.metadata["difference_table"]
    assert table[0][1] == 7
    assert table[0][2] == 12
    assert table[0][3] == 6
    assert len(solver.get_steps()) == 3


def test_interpolation_solver_alias():
    solver = InterpolationSolver()
    assert isinstance(solver, NewtonDividedDifferenceSolver)


def test_integration_solver_trapezoidal():
    solver = IntegrationSolver()
    x = [0, 1, 2]
    y = [1, 4, 9]
    # Trapezoidal: (1/2) * (1 + 2*4 + 9) = 9
    
    data = solver.solve(x_points=x, y_points=y, method="trapezoidal")
    assert np.isclose(data.y_data[0], 9.0)


def test_integration_solver_simpson13():
    solver = IntegrationSolver()
    x = [0, 1, 2]
    y = [1, 4, 9]
    # Simpson 1/3: (1/3) * (1 + 4*4 + 9) = 26/3
    
    data = solver.solve(x_points=x, y_points=y, method="simpson13")
    assert np.isclose(data.y_data[0], 26/3)


def test_integration_solver_simpson38():
    solver = IntegrationSolver()
    x = [0, 1, 2, 3]
    y = [1, 8, 27, 64]
    # Simpson 3/8: (3/8) * (1 + 3*8 + 3*27 + 64) = 63.75
    
    data = solver.solve(x_points=x, y_points=y, method="simpson38")
    assert np.isclose(data.y_data[0], 63.75)


def test_integration_solver_invalid_n():
    solver = IntegrationSolver()
    x = [0, 1]
    y = [1, 2]
    
    with pytest.raises(ValueError):
        solver.solve(x_points=x, y_points=y, method="simpson13")


def test_lagrange_interpolation_multiple_points():
    solver = LagrangeInterpolationSolver()
    x = [0, 1, 2]
    y = [1, 3, 2]
    target_x = [0.5, 1.5]
    
    data = solver.solve(x_points=x, y_points=y, target_x=target_x)
    assert len(data.y_data) == 2
    assert np.isclose(data.y_data[0], 2.375)
    assert np.isclose(data.y_data[1], 2.875)


def test_lagrange_interpolation_no_target():
    solver = LagrangeInterpolationSolver()
    x = [0, 1, 2]
    y = [1, 3, 2]
    
    data = solver.solve(x_points=x, y_points=y)
    assert data.x_data == x
    assert data.y_data == y


def test_lagrange_interpolation_invalid_input():
    solver = LagrangeInterpolationSolver()
    with pytest.raises(ValueError):
        solver.solve(x_points=[0], y_points=[1])
    with pytest.raises(ValueError):
        solver.solve(x_points=None, y_points=None)


def test_newton_difference_table_invalid_input():
    solver = NewtonDifferenceTableSolver()
    # Non-equispaced
    with pytest.raises(ValueError):
        solver.solve(x_points=[0, 1, 3], y_points=[1, 2, 4])
    # Mismatched lengths
    with pytest.raises(ValueError):
        solver.solve(x_points=[0, 1, 2], y_points=[1, 2])


def test_newton_divided_difference_multiple_points():
    solver = NewtonDividedDifferenceSolver()
    x = [0, 1, 2]
    y = [1, 3, 2]
    target_x = [0.5, 1.5]
    
    data = solver.solve(x_points=x, y_points=y, target_x=target_x)
    assert len(data.y_data) == 2
    assert np.isclose(data.y_data[0], 2.375)
    assert np.isclose(data.y_data[1], 2.875)


def test_newton_divided_difference_no_target():
    solver = NewtonDividedDifferenceSolver()
    x = [0, 1, 2]
    y = [1, 3, 2]
    
    data = solver.solve(x_points=x, y_points=y)
    assert data.x_data == x
    assert data.y_data == y


def test_newton_divided_difference_invalid_input():
    solver = NewtonDividedDifferenceSolver()
    with pytest.raises(ValueError):
        solver.solve(x_points=[0], y_points=[1])


def test_integration_solver_unsupported_method():
    solver = IntegrationSolver()
    with pytest.raises(ValueError):
        solver.solve(x_points=[0, 1, 2], y_points=[1, 2, 3], method="invalid")


def test_integration_solver_simpson13_odd_n():
    solver = IntegrationSolver()
    # n = 3 (4 points)
    x = [0, 1, 2, 3]
    y = [1, 2, 3, 4]
    with pytest.raises(ValueError):
        solver.solve(x_points=x, y_points=y, method="simpson13")


def test_integration_solver_simpson38_invalid_n():
    solver = IntegrationSolver()
    # n = 2 (3 points)
    x = [0, 1, 2]
    y = [1, 2, 3]
    with pytest.raises(ValueError):
        solver.solve(x_points=x, y_points=y, method="simpson38")


def test_integration_solver_validate_input_none():
    solver = IntegrationSolver()
    assert solver.validate_input(x_points=None, y_points=None) is False


def test_midpoint_solver():
    solver = MidpointSolver()
    f = lambda x: x**2
    # Integral of x^2 from 0 to 1 is 1/3
    # Midpoint with n=1: h=1, mid=0.5, f(0.5)=0.25, result=0.25
    # Midpoint with n=2: h=0.5, mid1=0.25, mid2=0.75, f(0.25)=0.0625, f(0.75)=0.5625, result=0.5*(0.0625+0.5625)=0.3125
    
    data = solver.solve(f=f, a=0, b=1, n=100)
    assert np.isclose(data.y_data[0], 1/3, atol=1e-4)


def test_trapezoidal_solver_function():
    solver = TrapezoidalSolver()
    f = lambda x: x**2
    data = solver.solve(f=f, a=0, b=1, n=100)
    assert np.isclose(data.y_data[0], 1/3, atol=1e-4)


def test_simpsons_solver_function():
    solver = SimpsonsRuleSolver()
    f = lambda x: x**2
    data = solver.solve(f=f, a=0, b=1, n=100, method="1/3")
    assert np.isclose(data.y_data[0], 1/3, atol=1e-10) # Simpson is exact for quadratics


def test_gaussian_quadrature_solver():
    solver = GaussianQuadratureSolver()
    f = lambda x: x**2
    # 2-point Gaussian quadrature is exact for polynomials up to degree 3
    data = solver.solve(f=f, a=0, b=1, points=2)
    assert np.isclose(data.y_data[0], 1/3)
    
    data3 = solver.solve(f=f, a=0, b=1, points=3)
    assert np.isclose(data3.y_data[0], 1/3)


def test_get_steps_all_solvers():
    # Lagrange
    s1 = LagrangeInterpolationSolver()
    s1.solve(x_points=[0, 1], y_points=[1, 2])
    assert isinstance(s1.get_steps(), list)
    
    # Newton Table
    s2 = NewtonDifferenceTableSolver()
    s2.solve(x_points=[0, 1], y_points=[1, 2])
    assert len(s2.get_steps()) > 0
    
    # Newton Divided
    s3 = NewtonDividedDifferenceSolver()
    s3.solve(x_points=[0, 1], y_points=[1, 2])
    assert len(s3.get_steps()) > 0
    
    # Integration
    s4 = IntegrationSolver()
    s4.solve(x_points=[0, 1, 2], y_points=[1, 2, 3], method="trapezoidal")
    assert len(s4.get_steps()) > 0
    
    # Midpoint
    s5 = MidpointSolver()
    s5.solve(f=lambda x: x, a=0, b=1, n=2)
    assert len(s5.get_steps()) == 2
    
    # Trapezoidal (Function)
    s6 = TrapezoidalSolver()
    s6.solve(f=lambda x: x, a=0, b=1, n=2)
    assert len(s6.get_steps()) > 0
    
    # Simpson
    s7 = SimpsonsRuleSolver()
    s7.solve(f=lambda x: x, a=0, b=1, n=2, method="1/3")
    assert len(s7.get_steps()) > 0

    # Simpson 1/3
    s10 = SimpsonOneThirdSolver()
    s10.solve(f=lambda x: x, a=0, b=1, n=2)
    assert len(s10.get_steps()) > 0

    # Simpson 3/8
    s11 = SimpsonThreeEighthsSolver()
    s11.solve(f=lambda x: x, a=0, b=1, n=3)
    assert len(s11.get_steps()) > 0
    
    # Gaussian
    s8 = GaussianQuadratureSolver()
    s8.solve(f=lambda x: x, a=0, b=1, points=2)
    assert len(s8.get_steps()) == 2
    
    # Differentiation
    s9 = NumericalDifferentiationSolver()
    s9.solve(f=lambda x: x, x=0, h=0.1, method="central")
    assert len(s9.get_steps()) > 0


def test_trapezoidal_solver_data_points():
    solver = TrapezoidalSolver()
    data = solver.solve(x_points=[0, 1, 2], y_points=[1, 2, 3])
    assert np.isclose(data.y_data[0], 4.0)


def test_simpsons_solver_data_points():
    solver = SimpsonsRuleSolver()
    data = solver.solve(x_points=[0, 1, 2], y_points=[1, 4, 9], method="1/3")
    assert np.isclose(data.y_data[0], 26/3)
    
    data38 = solver.solve(x_points=[0, 1, 2, 3], y_points=[1, 8, 27, 64], method="3/8")
    assert np.isclose(data38.y_data[0], 63.75)


def test_trapezoidal_solver_invalid():
    solver = TrapezoidalSolver()
    with pytest.raises(ValueError):
        solver.solve()
    assert solver.validate_input(f=None, x_points=None) is False


def test_simpsons_solver_invalid():
    solver = SimpsonsRuleSolver()
    with pytest.raises(ValueError):
        solver.solve(method="invalid", f=lambda x: x, a=0, b=1, n=2)
    with pytest.raises(ValueError):
        solver.solve()
    assert solver.validate_input(f=None) is False


def test_gaussian_quadrature_invalid():
    solver = GaussianQuadratureSolver()
    with pytest.raises(ValueError):
        solver.solve(f=None)
    with pytest.raises(ValueError):
        solver.solve(f=lambda x: x, points=4)
    assert solver.validate_input(f=None) is False


def test_numerical_differentiation_solver():
    solver = NumericalDifferentiationSolver()
    f = lambda x: np.sin(x)
    # d/dx sin(x) = cos(x)
    # cos(0) = 1
    
    data = solver.solve(f=f, x=0, h=1e-5, method="central")
    assert np.isclose(data.y_data[0], 1.0, atol=1e-7)
    
    data_f = solver.solve(f=f, x=0, h=1e-5, method="forward")
    assert np.isclose(data_f.y_data[0], 1.0, atol=1e-5)
    
    data_b = solver.solve(f=f, x=0, h=1e-5, method="backward")
    assert np.isclose(data_b.y_data[0], 1.0, atol=1e-5)


def test_numerical_differentiation_invalid():
    solver = NumericalDifferentiationSolver()
    with pytest.raises(ValueError):
        solver.solve(f=None)
    with pytest.raises(ValueError):
        solver.solve(f=lambda x: x, method="invalid")
    assert solver.validate_input(f=None) is False
