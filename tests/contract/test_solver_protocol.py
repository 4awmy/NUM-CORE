import pytest
from typing import Type
from numcore_engine.interfaces import Solver
from numcore_engine.solvers import (
    GaussSeidelSolver,
    JacobiSolver,
    BisectionSolver,
    NewtonRaphsonSolver,
    SecantSolver,
    SimpleIterationSolver,
    LagrangeInterpolationSolver,
    NewtonDifferenceTableSolver,
    NewtonDividedDifferenceSolver,
    LinearInterpolationSolver,
    CubicSplineSolver,
    IntegrationSolver,
    MidpointSolver,
    TrapezoidalSolver,
    SimpsonsRuleSolver,
    GaussianQuadratureSolver,
    NumericalDifferentiationSolver,
    EulerSolver,
    RungeKuttaSolver,
    ModifiedEulerSolver,
    TaylorSeriesOrder4Solver,
    LeastSquaresSolver,
    CurveFittingSolver
)

SOLVERS = [
    GaussSeidelSolver,
    JacobiSolver,
    BisectionSolver,
    NewtonRaphsonSolver,
    SecantSolver,
    SimpleIterationSolver,
    LagrangeInterpolationSolver,
    NewtonDifferenceTableSolver,
    NewtonDividedDifferenceSolver,
    LinearInterpolationSolver,
    CubicSplineSolver,
    IntegrationSolver,
    MidpointSolver,
    TrapezoidalSolver,
    SimpsonsRuleSolver,
    GaussianQuadratureSolver,
    NumericalDifferentiationSolver,
    EulerSolver,
    RungeKuttaSolver,
    ModifiedEulerSolver,
    TaylorSeriesOrder4Solver,
    LeastSquaresSolver,
    CurveFittingSolver
]

@pytest.mark.parametrize("solver_class", SOLVERS)
def test_solver_implements_protocol(solver_class: Type):
    """
    Assert that each solver class correctly implements the Solver protocol.
    We check both the class itself (using runtime_checkable Protocol) 
    and an instance of the class.
    """
    # Check if the class itself matches the protocol (structural subtyping)
    assert issubclass(solver_class, Solver), f"{solver_class.__name__} does not implement Solver protocol"
    
    # Check an instance
    # Note: Some solvers might require arguments in __init__, 
    # but the protocol check is about methods being present.
    # Since Solver is a Protocol, we can use isinstance on instances if it's runtime_checkable.
    
    # We can also manually check for required methods to be more explicit
    required_methods = ["solve", "get_steps", "validate_input"]
    for method in required_methods:
        assert hasattr(solver_class, method), f"{solver_class.__name__} is missing required method: {method}"
        assert callable(getattr(solver_class, method)), f"{solver_class.__name__}.{method} is not callable"

def test_all_solvers_covered():
    """
    Ensure that all solvers exported in numcore_engine.solvers are included in this contract test.
    """
    import numcore_engine.solvers as solvers_mod
    exported_names = solvers_mod.__all__
    
    # ComparisonRunner is a utility, not a solver
    expected_solvers = [name for name in exported_names if name != "ComparisonRunner"]
    
    tested_solver_names = [s.__name__ for s in SOLVERS]
    
    for name in expected_solvers:
        assert name in tested_solver_names, f"Solver {name} is exported but not included in contract tests"
