from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class NumericalStep:
    step_idx: int
    value: float
    error: Optional[float] = None
    details: Dict[str, Any] = field(default_factory=dict)
    check_name: Optional[str] = None
    check_passed: Optional[bool] = None


@dataclass(frozen=True)
class NumericalData:
    title: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    computation_time_ms: float = 0.0


@dataclass(frozen=True)
class SimulationData(NumericalData):
    x_data: List[float] = field(default_factory=list)
    y_data: List[float] = field(default_factory=list)


@dataclass(frozen=True)
class ComparisonResult:
    best_method: str
    results: List[NumericalData]
    recommendation: str
