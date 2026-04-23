import pytest
from numcore_engine.solvers.root_finder import NewtonRaphsonSolver, SimpleIterationSolver
from numcore_engine.interfaces import Solver


def test_newton_raphson_solver_protocol():
    solver = NewtonRaphsonSolver()
    assert isinstance(solver, Solver)


def test_simple_iteration_solver_protocol():
    solver = SimpleIterationSolver()
    assert isinstance(solver, Solver)


def test_newton_raphson_solve():
    solver = NewtonRaphsonSolver()
    # f(x) = x^2 - 4, root at x=2
    result = solver.solve(expression="x**2 - 4", initial_guess=3.0, tolerance=1e-6)
    
    assert result.title == "Newton-Raphson Convergence"
    assert pytest.approx(result.metadata["root"], rel=1e-5) == 2.0
    assert len(result.x_data) > 0
    assert len(result.y_data) == len(result.x_data)
    
    steps = solver.get_steps()
    assert len(steps) == result.metadata["iterations"]
    assert steps[-1].value == result.metadata["root"]


def test_simple_iteration_solve():
    solver = SimpleIterationSolver()
    # x = cos(x), root approx 0.739085
    result = solver.solve(expression="cos(x)", initial_guess=0.5, tolerance=1e-6)
    
    assert result.title == "Simple Iteration Convergence"
    assert pytest.approx(result.metadata["root"], rel=1e-5) == 0.739085
    assert len(result.x_data) > 0
    
    steps = solver.get_steps()
    assert len(steps) == result.metadata["iterations"]


def test_newton_raphson_invalid_input():
    solver = NewtonRaphsonSolver()
    with pytest.raises(ValueError):
        solver.solve(expression="x**2")  # Missing initial_guess


def test_simple_iteration_invalid_input():
    solver = SimpleIterationSolver()
    with pytest.raises(ValueError):
        solver.solve(initial_guess=1.0)  # Missing expression
