from pathlib import Path
import json
from pyquerytracker.config import configure, ExportType
from pyquerytracker import TrackQuery


def test_log_export_to_json(tmp_path):
    log_file = tmp_path / "out.jsonl"
    # configure for JSON export
    configure(export_type=ExportType.JSON, export_path=str(log_file))

    @TrackQuery()
    def simple(x):
        return x + 1

    assert simple(10) == 11
    assert log_file.exists()

    with log_file.open() as f:
        lines = f.readlines()
        assert len(lines) >= 1
        entry = json.loads(lines[-1])
        assert entry["function_name"] == "simple"
        assert entry["event"] in ("normal_execution", "slow_execution")
