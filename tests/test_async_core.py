import asyncio
import logging

import pytest

from pyquerytracker import TrackQuery, configure

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio


async def test_async_tracking_output(caplog):
    caplog.set_level("INFO")

    @TrackQuery()
    async def fake_async_db_query():
        await asyncio.sleep(0.01)
        return "done"

    result = await fake_async_db_query()
    assert result == "done"

    # Check the log records
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelname == "INFO"
    assert "Function fake_async_db_query executed successfully" in record.message
    assert "ms" in record.message


async def test_async_tracking_output_with_error(caplog):
    configure(slow_log_threshold_ms=10, slow_log_level=40)
    caplog.set_level("ERROR")

    @TrackQuery()
    async def failing_async_query():
        await asyncio.sleep(0.01)
        raise ValueError("Async Test error")

    result = await failing_async_query()
    assert result is None

    # Check the log records
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelname == "ERROR"
    assert "Function failing_async_query failed" in record.message
    assert "Async Test error" in record.message
    assert "ms" in record.message


async def test_async_tracking_with_class(caplog):
    configure(slow_log_threshold_ms=1000, slow_log_level=logging.INFO)
    caplog.set_level("INFO")

    class MyAsyncClass:
        @TrackQuery()
        async def do_work(self, a, b):
            await asyncio.sleep(0.01)
            return a + b

    result = await MyAsyncClass().do_work(5, 10)
    assert result == 15
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelname == "INFO"
    assert "MyAsyncClass" in record.message
    assert "do_work" in record.message
    assert "ms" in record.message


async def test_async_configure_slow_log(caplog):
    configure(slow_log_threshold_ms=10, slow_log_level=40)
    caplog.set_level("ERROR", logger="pyquerytracker")

    @TrackQuery()
    async def do_slow_async_work():
        await asyncio.sleep(0.1)
        return "slow"

    try:
        result = await do_slow_async_work()
        assert result == "slow"
        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.levelname == "ERROR"  # Configured to ERROR for slow logs
        assert "do_slow_async_work" in record.message
        assert "Slow execution" in record.message
        assert "ms" in record.message

    finally:
        # Reset config to avoid affecting other tests
        configure(slow_log_threshold_ms=100.0, slow_log_level=logging.WARNING)
