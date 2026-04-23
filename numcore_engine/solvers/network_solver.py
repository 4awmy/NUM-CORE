import numpy as np
from typing import Any, Dict, List, Optional
from ..interfaces import Solver
from ..models import NumericalStep, SimulationData

class GaussSeidelSolver(Solver):
    def __init__(self):
        self._steps: List[NumericalStep] = []

    def validate_input(self, **kwargs: Any) -> bool:
        A = kwargs.get("A")
        b = kwargs.get("b")
        if A is None or b is None:
            return False
        
        try:
            A_arr = np.array(A, dtype=float)
            b_arr = np.array(b, dtype=float)
            if A_arr.ndim != 2 or A_arr.shape[0] != A_arr.shape[1]:
                return False
            if b_arr.ndim != 1 or b_arr.shape[0] != A_arr.shape[0]:
                return False
            return True
        except (ValueError, TypeError):
            return False

    def _ensure_diagonal_dominance(self, A: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        n = A.shape[0]
        A_new = A.copy()
        b_new = b.copy()
        
        for i in range(n):
            # Find the row with the largest absolute value in column i
            max_row = i + np.argmax(np.abs(A_new[i:, i]))
            if max_row != i:
                A_new[[i, max_row]] = A_new[[max_row, i]]
                b_new[[i, max_row]] = b_new[[max_row, i]]
        
        return A_new, b_new

    def solve(self, **kwargs: Any) -> SimulationData:
        if not self.validate_input(**kwargs):
            raise ValueError("Invalid input for Gauss-Seidel solver.")
        
        A = np.array(kwargs["A"], dtype=float)
        b = np.array(kwargs["b"], dtype=float)
        x0 = kwargs.get("x0")
        tol = kwargs.get("tol", 1e-6)
        max_iter = kwargs.get("max_iter", 100)
        title = kwargs.get("title", "Gauss-Seidel Solution")

        # Row-swapping for diagonal dominance
        A, b = self._ensure_diagonal_dominance(A, b)
        
        n = A.shape[0]
        
        # Check for zero diagonal elements
        for i in range(n):
            if np.abs(A[i, i]) < 1e-12:
                raise ValueError(f"Zero diagonal element at index {i} after row swapping. Matrix might be singular.")

        if x0 is None:
            x = np.zeros(n)
        else:
            x = np.array(x0, dtype=float)
        
        self._steps = []
        
        error = float('inf')
        for k in range(max_iter):
            x_old = x.copy()
            for i in range(n):
                sum_j = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x_old[i+1:])
                x[i] = (b[i] - sum_j) / A[i, i]
            
            error = np.linalg.norm(x - x_old, ord=np.inf)
            self._steps.append(NumericalStep(
                step_idx=k,
                value=float(error),
                error=float(error),
                details={"x": x.tolist()}
            ))
            
            if error < tol:
                break
        
        return SimulationData(
            title=title,
            x_data=list(range(n)),
            y_data=x.tolist(),
            metadata={
                "iterations": len(self._steps),
                "final_error": float(error) if self._steps else 0.0,
                "converged": bool(error < tol) if self._steps else True
            }
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps


class JacobiSolver(Solver):
    """
    Jacobi iterative method for solving linear systems Ax = b.
    Unlike Gauss-Seidel, ALL variables are updated simultaneously using
    only values from the previous iteration.
    Formula: x_i^(k+1) = (b_i - sum_{j≠i} A_ij * x_j^(k)) / A_ii
    """

    def __init__(self):
        self._steps: List[NumericalStep] = []

    def validate_input(self, **kwargs: Any) -> bool:
        A = kwargs.get("A")
        b = kwargs.get("b")
        if A is None or b is None:
            return False

        try:
            A_arr = np.array(A, dtype=float)
            b_arr = np.array(b, dtype=float)
            if A_arr.ndim != 2 or A_arr.shape[0] != A_arr.shape[1]:
                return False
            if b_arr.ndim != 1 or b_arr.shape[0] != A_arr.shape[0]:
                return False
            return True
        except (ValueError, TypeError):
            return False

    def _ensure_diagonal_dominance(self, A: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Row-swap to maximize diagonal dominance."""
        n = A.shape[0]
        A_new = A.copy()
        b_new = b.copy()

        for i in range(n):
            max_row = i + np.argmax(np.abs(A_new[i:, i]))
            if max_row != i:
                A_new[[i, max_row]] = A_new[[max_row, i]]
                b_new[[i, max_row]] = b_new[[max_row, i]]

        return A_new, b_new

    def solve(self, **kwargs: Any) -> SimulationData:
        if not self.validate_input(**kwargs):
            raise ValueError("Invalid input for Jacobi solver.")

        A = np.array(kwargs["A"], dtype=float)
        b = np.array(kwargs["b"], dtype=float)
        x0 = kwargs.get("x0")
        tol = kwargs.get("tol", 1e-6)
        max_iter = kwargs.get("max_iter", 100)
        title = kwargs.get("title", "Jacobi Solution")

        # Row-swapping for diagonal dominance
        A, b = self._ensure_diagonal_dominance(A, b)

        n = A.shape[0]

        # Check for zero diagonal elements
        for i in range(n):
            if np.abs(A[i, i]) < 1e-12:
                raise ValueError(
                    f"Zero diagonal element at index {i} after row swapping. "
                    "Matrix might be singular or not diagonally dominant."
                )

        x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
        self._steps = []

        error = float("inf")
        for k in range(max_iter):
            x_new = np.zeros(n)
            for i in range(n):
                # KEY DIFFERENCE from Gauss-Seidel: use x (old) for ALL j
                sum_j = np.dot(A[i, :], x) - A[i, i] * x[i]
                x_new[i] = (b[i] - sum_j) / A[i, i]

            error = np.linalg.norm(x_new - x, ord=np.inf)
            self._steps.append(NumericalStep(
                step_idx=k,
                value=float(error),
                error=float(error),
                details={"x": x_new.tolist()}
            ))

            x = x_new.copy()  # Replace ALL at once (Jacobi rule)

            if error < tol:
                break

        return SimulationData(
            title=title,
            x_data=list(range(n)),
            y_data=x.tolist(),
            metadata={
                "iterations": len(self._steps),
                "final_error": float(error) if self._steps else 0.0,
                "converged": bool(error < tol) if self._steps else True
            }
        )

    def get_steps(self) -> List[NumericalStep]:
        return self._steps
