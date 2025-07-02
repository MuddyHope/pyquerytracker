from fastapi.testclient import TestClient

from pyquerytracker.app import app as fastapi_app
from pyquerytracker.core import TrackQuery

client = TestClient(fastapi_app)


# Simulate query activity
@TrackQuery()
def sample_query():
    return "ok"


@TrackQuery()
def slow_query():
    import time
    time.sleep(0.1)  # Simulate slow query
    return "slow"


def test_metrics_endpoint():
    """Test the /metrics endpoint returns correct aggregated data."""
    # Trigger some sample queries
    for _ in range(3):
        sample_query()
    
    # Trigger a slow query
    slow_query()

    # Call the metrics endpoint
    response = client.get("/metrics")
    assert response.status_code == 200

    json = response.json()
    
    # Check required fields
    assert "total_queries" in json
    assert "average_execution_time_ms" in json
    assert "slowest_query" in json
    
    # Check data types
    assert isinstance(json["total_queries"], int)
    assert isinstance(json["average_execution_time_ms"], (int, float))
    assert json["total_queries"] >= 4  # At least our test queries
    
    # Check slowest query structure
    if json["slowest_query"]:
        assert "function_name" in json["slowest_query"]
        assert "execution_time_ms" in json["slowest_query"]
        assert "timestamp" in json["slowest_query"]
        assert "event" in json["slowest_query"]
    
    # Optional: Print results for debug
    print("📊 Metrics API response:", json) 