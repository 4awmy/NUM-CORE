"""
Contract tests verifying that all solver classes comply with the Solver Protocol
defined in numcore_engine/interfaces.py.

Per NUM-CORE Constitution Principle II:
    All solver classes MUST implement the frozen Solver Protocol.

Per NUM-CORE Constitution Principle IV (Test-First):
    Contract tests required in tests/contract/.
"""
import pytest
from numcore_engine.interfaces import Solver
from numcore_engine.solvers.root_finder import (
    BisectionSolver,
    NewtonRaphsonSolver,
    SecantSolver,
    SimpleIterationSolver,
)
from numcore_engine.solvers.network_solver import (
    GaussSeidelSolver,
    JacobiSolver,
)
from numcore_engine.solvers.calculus_engine import (
    LagrangeInterpolationSolver,
    NewtonDifferenceTableSolver,
    NewtonDividedDifferenceSolver,
    IntegrationSolver,
    MidpointSolver,
    TrapezoidalSolver,
    SimpsonOneThirdSolver,
    SimpsonThreeEighthsSolver,
    SimpsonsRuleSolver,
    GaussianQuadratureSolver,
    NumericalDifferentiationSolver,
    LinearInterpolationSolver,
    CubicSplineSolver,
)

ALL_SOLVER_CLASSES = [
    BisectionSolver,
    NewtonRaphsonSolver,
    SecantSolver,
    SimpleIterationSolver,
    GaussSeidelSolver,
    JacobiSolver,
    LagrangeInterpolationSolver,
    NewtonDifferenceTableSolver,
    NewtonDividedDifferenceSolver,
    IntegrationSolver,
    MidpointSolver,
    TrapezoidalSolver,
    SimpsonOneThirdSolver,
    SimpsonThreeEighthsSolver,
    SimpsonsRuleSolver,
    GaussianQuadratureSolver,
    NumericalDifferentiationSolver,
    LinearInterpolationSolver,
    CubicSplineSolver,
]


@pytest.mark.parametrize("solver_cls", ALL_SOLVER_CLASSES)
def test_solver_protocol_isinstance(solver_cls):
    """All solver instances must satisfy the Solver Protocol via isinstance check."""
    solver = solver_cls()
    assert isinstance(solver, Solver), (
        f"{solver_cls.__name__} does not satisfy the Solver Protocol. "
        "Ensure it implements solve(), get_steps(), and validate_input()."
    )


@pytest.mark.parametrize("solver_cls", ALL_SOLVER_CLASSES)
def test_solver_has_solve_method(solver_cls):
    """All solvers must have a callable solve() method."""
    solver = solver_cls()
    assert callable(getattr(solver, "solve", None)), (
        f"{solver_cls.__name__} missing callable 'solve' method."
    )


@pytest.mark.parametrize("solver_cls", ALL_SOLVER_CLASSES)
def test_solver_has_get_steps_method(solver_cls):
    """All solvers must have a callable get_steps() method that returns a list."""
    solver = solver_cls()
    assert callable(getattr(solver, "get_steps", None)), (
        f"{solver_cls.__name__} missing callable 'get_steps' method."
    )
    steps = solver.get_steps()
    assert isinstance(steps, list), (
        f"{solver_cls.__name__}.get_steps() must return a list before any solve call."
    )


@pytest.mark.parametrize("solver_cls", ALL_SOLVER_CLASSES)
def test_solver_has_validate_input_method(solver_cls):
    """All solvers must have a callable validate_input() method that returns bool."""
    solver = solver_cls()
    assert callable(getattr(solver, "validate_input", None)), (
        f"{solver_cls.__name__} missing callable 'validate_input' method."
    )
    result = solver.validate_input()
    assert isinstance(result, bool), (
        f"{solver_cls.__name__}.validate_input() must return a bool."
    )


@pytest.mark.parametrize("solver_cls", ALL_SOLVER_CLASSES)
def test_solver_validate_input_rejects_empty(solver_cls):
    """All solvers must return False from validate_input() when called with no args."""
    solver = solver_cls()
    assert solver.validate_input() is False, (
        f"{solver_cls.__name__}.validate_input() must return False for empty input."
    )


def test_bisection_solve_returns_simulation_data():
    """BisectionSolver.solve() returns SimulationData with required metadata keys."""
    from numcore_engine.models import SimulationData
    solver = BisectionSolver()
    result = solver.solve(expression="x**2 - 4", a=1.0, b=3.0)
    assert isinstance(result, SimulationData)
    assert "root" in result.metadata
    assert "iterations" in result.metadata
    assert "diverged" in result.metadata


def test_newton_raphson_solve_returns_simulation_data():
    """NewtonRaphsonSolver.solve() returns SimulationData with required metadata keys."""
    from numcore_engine.models import SimulationData
    solver = NewtonRaphsonSolver()
    result = solver.solve(expression="x**2 - 4", initial_guess=3.0)
    assert isinstance(result, SimulationData)
    assert "root" in result.metadata
    assert "iterations" in result.metadata
    assert "diverged" in result.metadata
    assert "convergence_check_passed" in result.metadata


def test_simple_iteration_solve_returns_simulation_data():
    """SimpleIterationSolver.solve() returns SimulationData with convergence_passed key."""
    from numcore_engine.models import SimulationData
    solver = SimpleIterationSolver()
    result = solver.solve(expression="cos(x)", initial_guess=0.5)
    assert isinstance(result, SimulationData)
    assert "convergence_passed" in result.metadata


def test_jacobi_solve_returns_simulation_data():
    """JacobiSolver.solve() returns SimulationData with SDD metadata keys."""
    from numcore_engine.models import SimulationData
    solver = JacobiSolver()
    result = solver.solve(A=[[4, 1], [1, 3]], b=[1, 2])
    assert isinstance(result, SimulationData)
    assert "sdd_check" in result.metadata
    assert "sdd_reordered" in result.metadata
    assert "diverged" in result.metadata
    assert result.metadata["method_type"] == "simultaneous"


def test_gauss_seidel_solve_returns_simulation_data():
    """GaussSeidelSolver.solve() returns SimulationData with SDD metadata keys."""
    from numcore_engine.models import SimulationData
    solver = GaussSeidelSolver()
    result = solver.solve(A=[[4, 1], [1, 3]], b=[1, 2])
    assert isinstance(result, SimulationData)
    assert "sdd_check" in result.metadata
    assert "sdd_reordered" in result.metadata
    assert "diverged" in result.metadata
    assert result.metadata["method_type"] == "successive"
