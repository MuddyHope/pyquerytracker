import os
import json
import csv
import pytest
import time

from pyquerytracker.performance_exporter import PerformanceExporter

@pytest.mark.parametrize("export_format", ['json', 'csv'])
def test_performance_exporter(tmp_path, export_format):
    # Use tests/tmp/ directory for output
    export_dir = tmp_path / "tmp"
    export_dir.mkdir(parents=True, exist_ok=True)
    export_path = export_dir / f"performance.{export_format}"

    performance_stats = {
        "cpu_usage": 55.2,
        "memory_usage": 2048,
        "timestamp": "2025-06-13T12:00:00"
    }

    exporter = PerformanceExporter(str(export_path), export_format)
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
def test_exporter_frequency(tmp_path, export_format):
    export_dir = tmp_path / "tmp"
    export_dir.mkdir(parents=True, exist_ok=True)
    export_path = export_dir / f"performance.{export_format}"

    performance_stats = {
        "cpu_usage": 60.0,
        "memory_usage": 4096,
        "timestamp": "2025-06-13T12:05:00"
    }

    exporter = PerformanceExporter(str(export_path), export_format, frequency=2)

    # First export should always succeed
    exporter.export(performance_stats)
    first_mtime = os.path.getmtime(export_path)

    # Immediately try to export again — should be skipped
    exporter.export(performance_stats)
    second_mtime = os.path.getmtime(export_path)
    assert first_mtime == second_mtime, "File was not modified because of frequency constraint."

    # Wait for frequency to expire
    time.sleep(2.1)
    exporter.export(performance_stats)
    third_mtime = os.path.getmtime(export_path)
    assert third_mtime > second_mtime, "File was modified after frequency interval."
