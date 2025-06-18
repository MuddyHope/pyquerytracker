import time
import logging
import pytest
from pyquerytracker import TrackQuery


def test_tracking_output():
    @TrackQuery()
    def fake_db_query():
        return "done"

    assert fake_db_query() == "done"


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

    result = failing_query()
    assert result is None

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
            time.sleep(0.09)
            return a * b

    MyClass().do_work(2, 3)
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelname == "INFO"
    assert "MyClass" in record.message
    assert "do_work" in record.message
    assert "ms" in record.message
