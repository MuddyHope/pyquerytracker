from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

# In-memory store to collect tracked query data
query_data_store: List[Dict[str, Any]] = []


def store_tracked_query(log: Dict[str, Any]):
    """Store a single tracked query log entry."""
    log["timestamp"] = datetime.now(timezone.utc)
    query_data_store.append(log)


def get_tracked_queries(minutes: int) -> List[Dict[str, Any]]:
    """Return all tracked queries within the last `minutes`."""
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    return [log for log in query_data_store if log["timestamp"] >= cutoff]
