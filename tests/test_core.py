import pytest
from pyquerytracker.core import TrackQuery
import time
import asyncio


def test_tracking_output():
    @TrackQuery()
    def fake_db_query():
        return "done"
    assert fake_db_query() == "done"


def test_tracking_output_with_logging(caplog):
    caplog.set_level("INFO", logger="pyquerytracker")

    @TrackQuery()
    def fake_db_query():
        return "done"

    result = fake_db_query()
    assert result == "done"
    assert len(caplog.records) == 1
    assert "executed successfully" in caplog.records[0].message


def test_tracking_output_with_error(caplog):
    caplog.set_level("ERROR")

    @TrackQuery()
    def failing_query():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        failing_query()

    assert len(caplog.records) == 1
    assert "failed" in caplog.records[0].message


def test_tracking_with_class(caplog):
    caplog.set_level("INFO", logger="pyquerytracker")

    class MyClass:
        @TrackQuery()
        def do_work(self, a, b):
            time.sleep(0.1)
            return a * b

    MyClass().do_work(2, 3)
    assert len(caplog.records) == 1


@pytest.mark.asyncio
async def test_async_tracking(caplog):
    caplog.set_level("INFO", logger="pyquerytracker")

    @TrackQuery()
    async def async_query():
        await asyncio.sleep(0.2)
        return "async result"

    result = await async_query()
    assert result == "async result"
    assert len(caplog.records) == 1
