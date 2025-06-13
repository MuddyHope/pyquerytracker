import logging
from pyquerytracker.core import track_query

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@track_query
def failing_query():
    """A function that simulates a failed database query."""
    import time

    time.sleep(0.3)  # Simulate some work
    raise ValueError("Database connection failed")


if __name__ == "__main__":
    try:
        failing_query()
    except ValueError as e:
        print(f"Caught expected error: {e}")
