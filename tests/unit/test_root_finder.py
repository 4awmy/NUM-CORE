import pytest
from numcore_engine.solvers.root_finder import (
    BisectionSolver,
    NewtonRaphsonSolver,
    SecantSolver,
    SimpleIterationSolver,
)
from numcore_engine.interfaces import Solver


def test_bisection_solver_protocol():
    solver = BisectionSolver()
    assert isinstance(solver, Solver)


def test_newton_raphson_solver_protocol():
    solver = NewtonRaphsonSolver()
    assert isinstance(solver, Solver)


def test_secant_solver_protocol():
    solver = SecantSolver()
    assert isinstance(solver, Solver)


def test_simple_iteration_solver_protocol():
    solver = SimpleIterationSolver()
    assert isinstance(solver, Solver)


def test_bisection_solve():
    solver = BisectionSolver()
    # f(x) = x^2 - 4, root at x=2, interval [1, 3]
    result = solver.solve(expression="x**2 - 4", a=1.0, b=3.0, tolerance=1e-6)

    assert result.title == "Bisection Convergence"
    assert pytest.approx(result.metadata["root"], abs=1e-5) == 2.0
    assert result.metadata["diverged"] is False
    assert len(result.x_data) > 0


def test_newton_raphson_solve():
    solver = NewtonRaphsonSolver()
    # f(x) = x^2 - 4, root at x=2
    result = solver.solve(expression="x**2 - 4", initial_guess=3.0, tolerance=1e-6)

    assert result.title == "Newton-Raphson Convergence"
    assert pytest.approx(result.metadata["root"], rel=1e-5) == 2.0
    assert result.metadata["diverged"] is False
    assert len(result.x_data) > 0

    steps = solver.get_steps()
    assert len(steps) == result.metadata["iterations"]
    assert steps[-1].value == result.metadata["root"]


def test_secant_solve():
    solver = SecantSolver()
    # f(x) = x^2 - 4, root at x=2, guesses 1.0, 3.0
    result = solver.solve(expression="x**2 - 4", x0=1.0, x1=3.0, tolerance=1e-6)

    assert result.title == "Secant Convergence"
    assert pytest.approx(result.metadata["root"], rel=1e-5) == 2.0
    assert result.metadata["diverged"] is False
    assert len(result.x_data) > 0


def test_simple_iteration_solve():
    solver = SimpleIterationSolver()
    # x = cos(x), root approx 0.739085
    result = solver.solve(expression="cos(x)", initial_guess=0.5, tolerance=1e-6)

    assert result.title == "Simple Iteration Convergence"
    assert pytest.approx(result.metadata["root"], rel=1e-5) == 0.739085
    assert result.metadata["diverged"] is False
    assert len(result.x_data) > 0

    steps = solver.get_steps()
    assert len(steps) == result.metadata["iterations"]


def test_divergence_detection():
    solver = SimpleIterationSolver()
    # x = 1.1 * x, will diverge slowly
    result = solver.solve(expression="1.1 * x", initial_guess=1.0, max_iterations=20)

    assert result.metadata["diverged"] is True
    assert result.metadata["iterations"] < 20
    assert len(result.x_data) == result.metadata["iterations"]


def test_newton_raphson_divergence_breaks_early():
    from unittest.mock import patch
    from numcore_engine.parser import SymbolicParser

    solver = NewtonRaphsonSolver()

    with patch.object(SymbolicParser, "get_derivative", return_value="dummy"), patch.object(
        SymbolicParser,
        "parse_expression",
        side_effect=[lambda x: -2 * x, lambda x: 1.0],
    ):
        result = solver.solve(expression="x", initial_guess=1.0, max_iterations=50)

    assert result.metadata["diverged"] is True
    assert result.metadata["iterations"] == 6
    assert len(solver.get_steps()) == 6


def test_bisection_invalid_interval():
    solver = BisectionSolver()
    # f(x) = x^2 - 4, f(3)=5, f(4)=12, same sign
    with pytest.raises(ValueError, match="opposite signs"):
        solver.solve(expression="x**2 - 4", a=3.0, b=4.0)


def test_newton_raphson_invalid_input():
    solver = NewtonRaphsonSolver()
    with pytest.raises(ValueError):
        solver.solve(expression="x**2")  # Missing initial_guess


def test_bisection_details():
    solver = BisectionSolver()
    result = solver.solve(expression="x**2 - 4", a=1.0, b=3.0, tolerance=1e-6)
    steps = solver.get_steps()
    assert "f(a)" in steps[0].details
    assert "f(b)" in steps[0].details
    assert "f(c)" in steps[0].details


def test_simple_iteration_convergence_check():
    solver = SimpleIterationSolver()
    # x = cos(x), g'(x) = -sin(x), |g'(0.5)| = sin(0.5) approx 0.479 < 1
    result = solver.solve(expression="cos(x)", initial_guess=0.5)
    assert result.metadata["convergence_check_passed"] is True

    # x = x^2 + x - 2, g(x) = x^2 + x - 2, g'(x) = 2x + 1, |g'(2)| = 5 > 1
    result = solver.solve(expression="x**2 + x - 2", initial_guess=2.0)
    assert result.metadata["convergence_check_passed"] is False


def test_newton_raphson_fallback():
    from unittest.mock import patch
    from numcore_engine.parser import SymbolicParser
    
    with patch.object(SymbolicParser, "get_derivative", side_effect=Exception("Symbolic fail")):
        solver = NewtonRaphsonSolver()
        # Should still work using numerical differentiation
        result = solver.solve(expression="x**2 - 4", initial_guess=3.0, tolerance=1e-6)
        assert pytest.approx(result.metadata["root"], rel=1e-5) == 2.0
