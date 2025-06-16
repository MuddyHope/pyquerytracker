import time
import re
import pytest
from pyquerytracker.performance_exporter import BuiltinPerformanceExporter

def test_track_decorator_outputs_execution_time(capsys):
    exporter = BuiltinPerformanceExporter()

    @exporter.track
    def dummy_function():
        time.sleep(0.1)

    dummy_function()

    # Capture the output
    captured = capsys.readouterr()
    output = captured.out.strip()

    # Assert output format (basic check)
    assert output.startswith("Function 'dummy_function' executed in ")

    # Extract the ms part and check it's within reasonable range
    match = re.search(r'executed in ([\d\.]+) ms', output)
    assert match is not None
    elapsed_ms = float(match.group(1))
    
    assert 90 <= elapsed_ms <= 200  # Allowing some tolerance

def test_track_decorator_returns_original_value():
    exporter = BuiltinPerformanceExporter()

    @exporter.track
    def add(a, b):
        return a + b

    result = add(3, 5)
    assert result == 8
