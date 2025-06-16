from pyquerytracker import TrackQuery
import pytest
import json
from pyquerytracker.config import ExportType, get_config


def test_tracking_output(capsys):
    @TrackQuery()
    def fake_db_query():
        return "done"

    assert fake_db_query() == "done"


import logging  # noqa: E402

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def test_tracking_output_with_logging(caplog):
    caplog.set_level("INFO")

    @TrackQuery()
    def fake_db_query():
        return "done"

    result = fake_db_query()
    assert result == "done"

    # Check the log records
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelname == "INFO"
    assert "Function fake_db_query executed successfully" in record.message
    assert "ms" in record.message


def test_tracking_output_with_error(caplog):
    caplog.set_level("ERROR")

    @TrackQuery()
    def failing_query():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        failing_query()

    # Check the log records
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelname == "ERROR"
    assert "Function failing_query failed" in record.message
    assert "Test error" in record.message
    assert "ms" in record.message


def test_tracking_with_class(caplog):
    class MyClass:
        @TrackQuery()
        def do_work(self, a, b):
            import time

            time.sleep(0.09)
            return a * b

    res = MyClass().do_work(2, 3)  # noqa: F841
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelname == "INFO"
    assert "MyClass" in record.message
    assert "do_work" in record.message
    assert "ms" in record.message


def test_log_export_to_json(tmp_path, monkeypatch):
    export_path = tmp_path / "log.json"

    # Monkeypatch the config to enable JSON export
    config = get_config()
    monkeypatch.setattr(config, "export_path", str(export_path))
    monkeypatch.setattr(config, "export_type", ExportType.JSON)

    @TrackQuery()
    def simple_func(x):
        return x + 1

    result = simple_func(10)
    assert result == 11

    # Ensure the log file was created
    assert export_path.exists()
    with open(export_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) >= 1
        log_entry = json.loads(lines[-1])
        assert log_entry["function_name"] == "simple_func"
        assert log_entry["event"] in ["normal_execution", "slow_execution"]
