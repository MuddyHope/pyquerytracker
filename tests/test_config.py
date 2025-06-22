import logging
import time
from pyquerytracker.core import TrackQuery, logger


def configure(slow_log_threshold_ms=100, slow_log_level=logging.INFO):
    logger.setLevel(slow_log_level)


def test_configure_basic(caplog):
    configure(slow_log_threshold_ms=250)

    class MyClass:
        @TrackQuery()
        def do_work(self, a, b):
            time.sleep(0.5)
            return a * b

    MyClass().do_work(2, 3)
    assert len(caplog.records) == 1


def test_configure_basic_with_loglevel(caplog):
    caplog.set_level("ERROR", logger="pyquerytracker")

    configure(slow_log_threshold_ms=100, slow_log_level=logging.ERROR)

    class MyClass:
        def do_slow_work(self, a, b):
            import time
            time.sleep(0.2)
            return a * b

    # Apply TrackQuery to the unbound method
    MyClass.do_slow_work = TrackQuery()(MyClass.do_slow_work)

    result = MyClass().do_slow_work(2, 3)
    assert result == 6
