import pytest
from fastapi.testclient import TestClient
from pyquerytracker.api import app
from pyquerytracker.core import TrackQuery

client = TestClient(app)

# Simulate query activity
@TrackQuery()
def sample_query():
    return "ok"

def test_query_stats_endpoint():
    # Trigger a few logs
    for _ in range(3):
        sample_query()

    # Call the stats endpoint
    response = client.get("/api/query-stats?minutes=5")
    assert response.status_code == 200

    json = response.json()
    assert "labels" in json
    assert "durations" in json
    assert isinstance(json["labels"], list)
    assert isinstance(json["durations"], list)

    # Optional: Print results for debug
    print("📊 Dashboard API response:", json)
