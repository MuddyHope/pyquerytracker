import logging
from pyquerytracker import TrackQuery
from pyquerytracker.config import configure, ExportType

# ✅ Step 1: Configure tracking
configure(
    slow_log_threshold_ms=50,             # Set threshold for slow queries
    slow_log_level=logging.WARNING,       # Logging level for slow queries
    export_type=ExportType.JSON,          # Export to JSON
    export_path="logs/queries_2.json"       # File to export logs
)

# ✅ Step 2: Decorate functions
@TrackQuery()
def fast_function(x, y):
    return x + y

@TrackQuery()
def slow_function(x):
    import time
    time.sleep(0.049)  # 100ms
    return x * 2

@TrackQuery()
def faulty_function():
    raise ValueError("Simulated failure")

# ✅ Step 3: Run functions and observe logs
if __name__ == "__main__":
    print("Fast:", fast_function(3, 4))
    print("Fast:", fast_function(4, 12))
    print("Fast:", fast_function(4, 00))
    print("Fast:", fast_function(556, 12))

    print("Slow:", slow_function(10))

    try:
        faulty_function()
    except Exception:
        pass

    print("Done.")
