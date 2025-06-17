from pathlib import Path
import json
from pyquerytracker.config import configure, ExportType
from pyquerytracker.core import flush_exported_logs
from pyquerytracker import TrackQuery
import logging


def test_log_export_to_json(tmp_path):
    log_file = tmp_path / "out.json"
    # configure for JSON export
    configure(export_type=ExportType.JSON, export_path=str(log_file))

    logging.debug("Exporting to JSON log file: %s", log_file)

    @TrackQuery()
    def simple(x):
        return x + 1

    # Sanity check:  Is the exporter initialized?
    # print("Exporting Enabled:", TrackQuery._exporter is not None)
    assert simple(10) == 11
    assert flush_exported_logs() is None  # No return value expected
    # print("Log location:", log_file)
    # print("Log file exists:", log_file.exists())
    assert log_file.exists()

    with log_file.open() as f:
        entries = json.load(f)
        assert len(entries) >= 1
        entry = entries[-1]
        assert entry["function_name"] == "simple"
        assert entry["event"] in ("normal_execution", "slow_execution")
