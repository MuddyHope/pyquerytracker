import os
import json
import csv
import pytest
import time

from pyquerytracker.performance_exporter import PerformanceExporter

# Define persistent output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

@pytest.mark.parametrize("export_format", ['json', 'csv'])
def test_performance_exporter_persistent(export_format):
    export_path = os.path.join(OUTPUT_DIR, f"performance.{export_format}")

    performance_stats = {
        "cpu_usage": 55.2,
        "memory_usage": 2048,
        "timestamp": "2025-06-13T12:00:00"
    }

    exporter = PerformanceExporter(export_path, export_format)
    exporter.export(performance_stats)

    assert os.path.exists(export_path)

    if export_format == 'json':
        with open(export_path, 'r') as f:
            data = json.load(f)
            assert data == performance_stats
    elif export_format == 'csv':
        with open(export_path, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert rows[0] == ['Metric', 'Value']
            exported_data = {row[0]: row[1] for row in rows[1:]}
            exported_data = {
                k: float(v) if k in ['cpu_usage', 'memory_usage'] else v
                for k, v in exported_data.items()
            }
            assert exported_data["cpu_usage"] == performance_stats["cpu_usage"]
            assert exported_data["memory_usage"] == performance_stats["memory_usage"]
            assert exported_data["timestamp"] == performance_stats["timestamp"]

@pytest.mark.parametrize("export_format", ['json', 'csv'])
def test_exporter_frequency_persistent(export_format):
    export_path = os.path.join(OUTPUT_DIR, f"performance_freq.{export_format}")

    performance_stats = {
        "cpu_usage": 60.0,
        "memory_usage": 4096,
        "timestamp": "2025-06-13T12:05:00"
    }

    exporter = PerformanceExporter(export_path, export_format, frequency=2)

    # First export should succeed
    exporter.export(performance_stats)
    first_mtime = os.path.getmtime(export_path)

    # Immediate second export — should be skipped
    exporter.export(performance_stats)
    second_mtime = os.path.getmtime(export_path)
    assert first_mtime == second_mtime, "File should not have been modified due to frequency limit."

    # Wait for frequency period to pass
    time.sleep(2.1)
    exporter.export(performance_stats)
    third_mtime = os.path.getmtime(export_path)
    assert third_mtime > second_mtime, "File should be modified after frequency period."
