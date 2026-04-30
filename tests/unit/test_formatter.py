import os
import csv
import pytest
from numcore_cli.formatter import NumericalFormatter
from numcore_engine.models import NumericalStep

def test_export_steps_to_csv(tmp_path):
    # Setup test data
    steps = [
        NumericalStep(step_idx=0, value=1.0, error=0.1, details={"x_n": 0.5, "f(x)": 2.0}),
        NumericalStep(step_idx=1, value=1.1, error=0.01, details={"x_n": 1.0, "f(x)": 0.5}),
    ]
    
    filename = tmp_path / "test_results.csv"
    
    # Execute
    returned_filename = NumericalFormatter.export_steps_to_csv(steps, "Newton", str(filename))
    
    # Verify
    assert returned_filename == str(filename)
    assert os.path.exists(filename)
    
    with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        
        assert len(rows) == 2
        
        assert rows[0]["step_idx"] == "0"
        assert rows[0]["value"] == "1.0"
        assert rows[0]["error"] == "0.1"
        assert rows[0]["x_n"] == "0.5"
        assert rows[0]["f(x)"] == "2.0"
        
        assert rows[1]["step_idx"] == "1"
        assert rows[1]["value"] == "1.1"
        assert rows[1]["error"] == "0.01"
        assert rows[1]["x_n"] == "1.0"
        assert rows[1]["f(x)"] == "0.5"

def test_export_steps_to_csv_default_filename(tmp_path):
    # Change directory to tmp_path to avoid cluttering root
    os.chdir(tmp_path)
    
    steps = [
        NumericalStep(step_idx=0, value=1.0, error=None, details={"a": 1}),
    ]
    
    # Execute
    returned_filename = NumericalFormatter.export_steps_to_csv(steps, "Test Method")
    
    # Verify
    assert "results_test_method_" in returned_filename
    assert returned_filename.endswith(".csv")
    assert os.path.exists(returned_filename)

def test_export_steps_to_csv_with_lists(tmp_path):
    # Test handling of list values in details (common in linear systems)
    steps = [
        NumericalStep(step_idx=0, value=0.0, error=0.1, details={"x": [1.0, 2.0, 3.0]}),
    ]
    
    filename = tmp_path / "test_lists.csv"
    
    # Execute
    NumericalFormatter.export_steps_to_csv(steps, "Gauss-Seidel", str(filename))
    
    # Verify
    with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        assert rows[0]["x"] == "[1.0, 2.0, 3.0]"
