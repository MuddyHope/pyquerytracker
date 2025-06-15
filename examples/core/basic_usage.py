from pyquerytracker import TrackQuery, configure

configure(slow_log_threshold_ms=1000, slow_log_level=20)


@TrackQuery()
def simple_query():
    """A simple function that simulates a database query."""
    import time

    time.sleep(0.5)  # Simulate some work
    return "Query completed successfully"


if __name__ == "__main__":
    result = simple_query()
    print(f"Result: {result}")
