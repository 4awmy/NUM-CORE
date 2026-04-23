import pytest
from numcore_engine.models import NumericalStep, SimulationData
from numcore_engine.parser import SymbolicParser


def test_numerical_step_creation():
    step = NumericalStep(step_idx=1, value=5.0, error=0.1, details={"method": "test"})
    assert step.step_idx == 1
    assert step.value == 5.0
    assert step.error == 0.1
    assert step.details["method"] == "test"


def test_simulation_data_creation():
    data = SimulationData(title="Test Simulation", x_data=[0.0, 1.0], y_data=[0.0, 1.0])
    assert data.title == "Test Simulation"
    assert data.x_data == [0.0, 1.0]
    assert data.y_data == [0.0, 1.0]


def test_symbolic_parser_single_variable():
    parser = SymbolicParser()
    func = parser.parse_expression("x**2 + 5")
    assert func(2) == 9.0
    assert func(0) == 5.0


def test_symbolic_parser_multiple_variables():
    parser = SymbolicParser()
    func = parser.parse_expression("x + y", variables=["x", "y"])
    assert func(2, 3) == 5.0


def test_symbolic_parser_derivative():
    parser = SymbolicParser()
    derivative = parser.get_derivative("x**2 + 5", variable="x")
    # sympy might return '2*x' or '2.0*x' depending on version/context
    assert "2*x" in derivative.replace(" ", "")


def test_symbolic_parser_higher_order_derivative():
    parser = SymbolicParser()
    derivative = parser.get_derivative("x**3", variable="x", order=2)
    assert "6*x" in derivative.replace(" ", "")
