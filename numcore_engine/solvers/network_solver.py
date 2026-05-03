import numpy as np
from typing import Any, Dict, List, Optional
from ..interfaces import Solver
from ..models import NumericalStep, SimulationData

class IterativeSolver(Solver):
    """Base class for iterative linear system solvers."""
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

    def _ensure_diagonal_dominance(self, A: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray, bool, List[bool]]:
        """Row-swap to maximize diagonal dominance and return SDD check results."""
        n = A.shape[0]
        
        def get_sdd_check(mat):
            check = []
            for i in range(n):
                diag = np.abs(mat[i, i])
                off_diag_sum = np.sum(np.abs(mat[i, :])) - diag
                check.append(bool(diag > off_diag_sum))
            return check

        # Try to reorder to achieve diagonal dominance
        used_rows = set()
        new_order = []
        for i in range(n):
            best_row = -1
            max_val = -1.0
            for j in range(n):
                if j not in used_rows:
                    if np.abs(A[j, i]) > max_val:
                        max_val = np.abs(A[j, i])
                        best_row = j
            
            if best_row != -1:
                new_order.append(best_row)
                used_rows.add(best_row)
            else:
                return A, b, False, get_sdd_check(A)

        A_new = A[new_order, :]
        b_new = b[new_order]
        sdd_reordered = list(new_order) != list(range(n))
        sdd_check = get_sdd_check(A_new)
        
        return A_new, b_new, sdd_reordered, sdd_check

    def get_steps(self) -> List[NumericalStep]:
        return self._steps


class GaussSeidelSolver(IterativeSolver):
    """
    Gauss-Seidel iterative method for solving linear systems Ax = b.
    Updates variables successively using the most recent values.
    """
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
        A, b, sdd_reordered, sdd_check = self._ensure_diagonal_dominance(A, b)
        
        n = A.shape[0]
        
        # Check for zero diagonal elements
        for i in range(n):
            if np.abs(A[i, i]) < 1e-12:
                raise ValueError(f"Zero diagonal element at index {i} after row swapping. Matrix might be singular.")

        x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
        self._steps = []
        
        error = float('inf')
        growing_error_count = 0
        diverged = False
        
        for k in range(max_iter):
            x_old = x.copy()
            for i in range(n):
                sum_j = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x_old[i+1:])
                x[i] = (b[i] - sum_j) / A[i, i]
            
            prev_error = error
            error = np.linalg.norm(x - x_old, ord=np.inf)
            
            # Divergence detection: 5 consecutive growing errors
            if k > 0 and error > prev_error:
                growing_error_count += 1
            else:
                growing_error_count = 0
            
            if growing_error_count >= 5:
                diverged = True
            
            self._steps.append(NumericalStep(
                step_idx=k,
                value=float(error),
                error=float(error),
                details={"x": x.tolist()}
            ))
            
            if error < tol or diverged:
                break
        
        return SimulationData(
            title=title,
            x_data=list(range(n)),
            y_data=x.tolist(),
            metadata={
                "iterations": len(self._steps),
                "final_error": float(error) if self._steps else 0.0,
                "converged": bool(error < tol and not diverged) if self._steps else True,
                "sdd_reordered": sdd_reordered,
                "sdd_check": sdd_check,
                "diverged": diverged,
                "method_type": "successive"
            }
        )


class JacobiSolver(IterativeSolver):
    """
    Jacobi iterative method for solving linear systems Ax = b.
    Updates variables simultaneously using only values from the previous iteration.
    """
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
        A, b, sdd_reordered, sdd_check = self._ensure_diagonal_dominance(A, b)

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
        growing_error_count = 0
        diverged = False

        for k in range(max_iter):
            x_new = np.zeros(n)
            for i in range(n):
                # Simultaneous update: use x (old) for ALL j
                sum_j = np.dot(A[i, :], x) - A[i, i] * x[i]
                x_new[i] = (b[i] - sum_j) / A[i, i]

            prev_error = error
            error = np.linalg.norm(x_new - x, ord=np.inf)
            
            # Divergence detection: 5 consecutive growing errors
            if k > 0 and error > prev_error:
                growing_error_count += 1
            else:
                growing_error_count = 0
            
            if growing_error_count >= 5:
                diverged = True

            self._steps.append(NumericalStep(
                step_idx=k,
                value=float(error),
                error=float(error),
                details={"x": x_new.tolist()}
            ))

            x = x_new.copy()

            if error < tol or diverged:
                break

        return SimulationData(
            title=title,
            x_data=list(range(n)),
            y_data=x.tolist(),
            metadata={
                "iterations": len(self._steps),
                "final_error": float(error) if self._steps else 0.0,
                "converged": bool(error < tol and not diverged) if self._steps else True,
                "sdd_reordered": sdd_reordered,
                "sdd_check": sdd_check,
                "diverged": diverged,
                "method_type": "simultaneous"
            }
        )


class NetworkSolver:
    """
    A high-level wrapper for linear system solvers, primarily used by the GUI.
    Defaults to using Gauss-Seidel iteration.
    """
    def __init__(self):
        self.solver = GaussSeidelSolver()

    def solve(self, **kwargs: Any) -> SimulationData:
        # Map GUI-style arguments to solver-style arguments
        if "matrix" in kwargs and "A" not in kwargs:
            kwargs["A"] = kwargs.pop("matrix")
        if "vector" in kwargs and "b" not in kwargs:
            kwargs["b"] = kwargs.pop("vector")
            
        data = self.solver.solve(**kwargs)
        
        # Ensure 'solution' is in metadata for GUI compatibility
        if "solution" not in data.metadata:
            data.metadata["solution"] = data.y_data
            
        return data
