import pytest
from numcore_engine.solvers.ode_solvers import EulerSolver, RungeKuttaSolver


def test_euler_solver_basic():
    solver = EulerSolver()
    # dy/dx = x + y, y(0) = 1, h = 0.1, 2 steps
    # Step 1: y(0.1) = y(0) + 0.1 * (0 + 1) = 1 + 0.1 = 1.1
    # Step 2: y(0.2) = y(0.1) + 0.1 * (0.1 + 1.1) = 1.1 + 0.1 * 1.2 = 1.1 + 0.12 = 1.22
    result = solver.solve(expression="x + y", x0=0, y0=1, h=0.1, steps=2)

    assert len(result.x_data) == 3
    assert len(result.y_data) == 3
    assert pytest.approx(result.x_data[2]) == 0.2
    assert pytest.approx(result.y_data[2]) == 1.22
    assert result.metadata["method"] == "Euler"


def test_rk4_solver_basic():
    solver = RungeKuttaSolver()
    # dy/dx = x + y, y(0) = 1, h = 0.1, 1 step
    # k1 = 0.1 * (0 + 1) = 0.1
    # k2 = 0.1 * (0.05 + 1.05) = 0.11
    # k3 = 0.1 * (0.05 + 1.055) = 0.1105
    # k4 = 0.1 * (0.1 + 1.1105) = 0.12105
    # y(0.1) = 1 + (0.1 + 2*0.11 + 2*0.1105 + 0.12105) / 6
    # y(0.1) = 1 + (0.1 + 0.22 + 0.221 + 0.12105) / 6
    # y(0.1) = 1 + 0.66205 / 6 = 1 + 0.110341666... = 1.110341666...
    result = solver.solve(expression="x + y", x0=0, y0=1, h=0.1, steps=1)

    assert len(result.x_data) == 2
    assert pytest.approx(result.x_data[1]) == 0.1
    assert pytest.approx(result.y_data[1]) == 1.1103416666666667
    assert result.metadata["method"] == "RK4"


def test_ode_solvers_invalid_input():
    euler = EulerSolver()
    rk4 = RungeKuttaSolver()

    with pytest.raises(ValueError):
        euler.solve(expression="x+y", x0=0)  # Missing parameters

    with pytest.raises(ValueError):
        rk4.solve(expression="x+y", x0=0)  # Missing parameters
