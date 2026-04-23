from typing import Any, Dict, List, Protocol, runtime_checkable

from .models import NumericalStep, SimulationData


@runtime_checkable
class Solver(Protocol):
    def solve(self, **kwargs: Any) -> SimulationData:
        """Execute the numerical solver and return the final simulation data."""
        ...

    def get_steps(self) -> List[NumericalStep]:
        """Return the list of intermediate steps taken by the solver."""
        ...

    def validate_input(self, **kwargs: Any) -> bool:
        """Validate the input parameters for the solver."""
        ...
