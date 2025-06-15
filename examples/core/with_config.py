from pyquerytracker import TrackQuery
from pyquerytracker.config import configure
import time
import logging

configure(slow_log_threshold_ms=500, slow_log_level=logging.ERROR)


@TrackQuery()
def fast_query():
    """A function that executes quickly."""
    return "Fast query completed"


@TrackQuery()
def slow_query():
    """A function that takes some time to execute."""
    time.sleep(0.5)  # Simulate some work
    return "Slow query completed"


if __name__ == "__main__":
    # Test with positional arguments
    result1 = fast_query()
    print(f"Result 1: {result1}")

    # Test with keyword arguments
    result2 = slow_query()
    print(f"Result 2: {result2}")
