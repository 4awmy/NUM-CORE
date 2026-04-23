from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class NumericalStep:
    step_idx: int
    value: float
    error: Optional[float] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SimulationData:
    title: str
    x_data: List[float]
    y_data: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)
