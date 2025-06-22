import logging

from pyquerytracker import TrackQuery

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@TrackQuery()
def complex_query(user_id: int, query_type: str, limit: int = 10):
    """A function that simulates a complex database query with arguments."""
    import time

    time.sleep(0.2)  # Simulate some work
    return f"Retrieved {limit} {query_type} records for user {user_id}"


if __name__ == "__main__":
    # Test with positional arguments
    result1 = complex_query(123, "posts")
    print(f"Result 1: {result1}")

    # Test with keyword arguments
    result2 = complex_query(user_id=456, query_type="comments", limit=5)
    print(f"Result 2: {result2}")
