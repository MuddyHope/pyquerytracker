import logging

from pyquerytracker import TrackQuery, configure


def test_configure_basic(caplog):
    configure(slow_log_threshold_ms=250)

    class MyClass:
        @TrackQuery()
        def do_work(self, a, b):
            import time

            time.sleep(0.5)
            return a * b

    res = MyClass().do_work(2, 3)  # noqa: F841
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelname == "WARNING"
    assert "MyClass" in record.message
    assert "do_work" in record.message
    assert "ms" in record.message


def test_configure_basic_with_loglevel(caplog):

    configure(slow_log_threshold_ms=100, slow_log_level=logging.ERROR)

    class MyClass:
        @TrackQuery()
        def do_slow_work(self, a, b):
            import time

            time.sleep(0.2)
            return a * b

    res = MyClass().do_slow_work(2, 3)  # noqa: F841
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelname == "ERROR"
    assert "MyClass" in record.message
    assert "do_slow_work" in record.message
    assert "ms" in record.message
