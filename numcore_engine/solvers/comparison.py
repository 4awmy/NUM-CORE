import time
from typing import Any, Dict, List, Optional
from ..models import ComparisonResult, NumericalData, SimulationData
from ..interfaces import Solver

class ComparisonRunner:
    """
    Runs multiple solvers for a given problem and compares their performance.
    """

    def __init__(self, solvers: Dict[str, Solver]) -> None:
        self.solvers = solvers

    def run_comparison(self, **kwargs: Any) -> ComparisonResult:
        """
        Execute all compatible solvers and compare their results.
        """
        results: List[NumericalData] = []
        
        for name, solver in self.solvers.items():
            if solver.validate_input(**kwargs):
                start_time = time.perf_counter()
                try:
                    data = solver.solve(**kwargs)
                    end_time = time.perf_counter()
                    
                    # Create a new SimulationData with computation time
                    # We use SimulationData because it's the most common return type
                    comp_data = SimulationData(
                        title=name,
                        metadata=data.metadata,
                        computation_time_ms=(end_time - start_time) * 1000,
                        x_data=data.x_data,
                        y_data=data.y_data
                    )
                    results.append(comp_data)
                except Exception:
                    # Skip solvers that fail for this specific input
                    continue
        
        if not results:
            raise ValueError("No compatible solvers found for the given input.")

        # Determine best method
        # Criteria: 
        # 1. Not diverged
        # 2. Fewest iterations (if applicable)
        # 3. Fastest computation time
        
        valid_results = [r for r in results if not r.metadata.get("diverged", False)]
        
        if not valid_results:
            # If all diverged, pick the one that lasted longest or just the first one
            best_method_data = results[0]
        else:
            # Sort by iterations first, then by time
            best_method_data = min(
                valid_results, 
                key=lambda x: (x.metadata.get("iterations", 999), x.computation_time_ms)
            )
        
        recommendation = self._generate_recommendation(results, best_method_data.title)
        
        return ComparisonResult(
            best_method=best_method_data.title,
            results=results,
            recommendation=recommendation
        )

    def _generate_recommendation(self, results: List[NumericalData], best_name: str) -> str:
        """Generates a logical recommendation based on comparison results."""
        best_data = next(r for r in results if r.title == best_name)
        
        if best_data.metadata.get("diverged", False):
            return "All tested methods diverged for this problem. Try different initial guesses or parameters."
            
        iterations = best_data.metadata.get("iterations")
        if iterations:
            return f"Recommended: {best_name}. It converged in {iterations} iterations, which was the most efficient among tested methods."
        else:
            return f"Recommended: {best_name}. It provided the fastest stable solution."
