from pyquerytracker.core import TrackQuery
import time


@TrackQuery()
def fast_query():
    """A function that executes quickly."""
    return "Fast query completed"


@TrackQuery()
def slow_query():
    """A function that takes some time to execute."""
    time.sleep(0.5)  # Simulate some work
    return "Slow query completed"


@TrackQuery()
def failing_query():
    """A function that raises an error."""
    time.sleep(0.2)  # Simulate some work
    raise ValueError("Query failed!")


if __name__ == "__main__":
    print("\nTesting fast query:")
    result1 = fast_query()
    print(f"Result: {result1}")

    print("\nTesting slow query:")
    result2 = slow_query()
    print(f"Result: {result2}")

    print("\nTesting failing query:")
    try:
        failing_query()
    except ValueError as e:
        print(f"Caught expected error: {e}")
