import os
import time

from pyquerytracker import TrackQuery
from pyquerytracker.config import ExportType, configure

os.makedirs("logs-csv", exist_ok=True)

configure(
    slow_log_threshold_ms=50.0,
    slow_log_level=20,  # INFO
    export_type=ExportType.CSV,
    export_path="logs-csv/query_logs_2.csv",
)


@TrackQuery()
def process_data(x, y):
    time.sleep(8)
    return x + y


@TrackQuery()
def failing_task():
    time.sleep(0.03)  # not slow
    raise RuntimeError("This failed intentionally.")


# Run tasks
print("Result:", process_data(5, 7))
print("Result:", process_data(1, 2))

try:
    failing_task()
except Exception:
    pass
