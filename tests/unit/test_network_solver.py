import pytest
import numpy as np
from numcore_engine.solvers.network_solver import GaussSeidelSolver
from numcore_engine.models import SimulationData

def test_gauss_seidel_simple_2x2():
    solver = GaussSeidelSolver()
    A = [[4, 1], [1, 3]]
    b = [1, 2]
    # Solution: 4x + y = 1, x + 3y = 2 => x = 1/11, y = 7/11
    expected_x = [1/11, 7/11]
    
    result = solver.solve(A=A, b=b, tol=1e-8)
    
    assert isinstance(result, SimulationData)
    assert np.allclose(result.y_data, expected_x, atol=1e-7)
    assert result.metadata["converged"] is True

def test_gauss_seidel_row_swapping():
    solver = GaussSeidelSolver()
    # Not diagonally dominant, but can be made so by swapping rows
    A = [[1, 3], [4, 1]]
    b = [2, 1]
    # Swapped: [[4, 1], [1, 3]], b = [1, 2] -> same as above
    expected_x = [1/11, 7/11]
    
    result = solver.solve(A=A, b=b, tol=1e-8)
    
    assert np.allclose(result.y_data, expected_x, atol=1e-7)
    assert result.metadata["converged"] is True

def test_gauss_seidel_3x3():
    solver = GaussSeidelSolver()
    A = [[10, -1, 0], [-1, 10, -2], [0, -2, 10]]
    b = [9, 7, 8]
    # Solution: x=1, y=1, z=1
    expected_x = [1.0, 1.0, 1.0]
    
    result = solver.solve(A=A, b=b, tol=1e-8)
    
    assert np.allclose(result.y_data, expected_x, atol=1e-7)
    assert result.metadata["converged"] is True

def test_gauss_seidel_invalid_input():
    solver = GaussSeidelSolver()
    
    # Missing A or b
    with pytest.raises(ValueError):
        solver.solve(A=[[1, 2]])
    
    # Non-square matrix
    with pytest.raises(ValueError):
        solver.solve(A=[[1, 2, 3], [4, 5, 6]], b=[1, 2])
    
    # Dimension mismatch
    with pytest.raises(ValueError):
        solver.solve(A=[[1, 2], [3, 4]], b=[1, 2, 3])

def test_gauss_seidel_singular_matrix():
    solver = GaussSeidelSolver()
    # Matrix with zero column cannot be made diagonally dominant and will have zero diagonal
    A = [[0, 1], [0, 1]]
    b = [1, 1]
    
    with pytest.raises(ValueError, match="Zero diagonal element"):
        solver.solve(A=A, b=b)

def test_gauss_seidel_steps():
    solver = GaussSeidelSolver()
    A = [[4, 1], [1, 3]]
    b = [1, 2]
    
    solver.solve(A=A, b=b, max_iter=5)
    steps = solver.get_steps()
    
    assert len(steps) > 0
    assert steps[0].step_idx == 0
    assert "x" in steps[0].details
