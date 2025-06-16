![GitHub Release](https://img.shields.io/github/v/release/MuddyHope/pyquerytracker)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/MuddyHope/pyquerytracker)

![PyPI - Downloads](https://img.shields.io/pypi/dm/pyquerytracker)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/MuddyHope/pyquerytracker/.github%2Fworkflows%2Fpublish.yml)
![GitHub forks](https://img.shields.io/github/forks/MuddyHope/pyquerytracker)

![PyPI - License](https://img.shields.io/pypi/l/pyquerytracker)

# 🐍 pyquerytracker

**pyquerytracker** is a lightweight Python utility to **track and analyze database query performance** using simple decorators. It enables developers to gain visibility into SQL execution time, log metadata, and export insights in JSON format — with optional FastAPI integration and scheduled reporting.

---

## 🚀 Features

- ✅ Easy-to-use decorator to track function execution (e.g., SQL queries)
- ✅ Capture runtime, function name, args, return values, and more
- ✅ Export logs to JSON or CSV
- ✅ Summary statistics and data analysis
- ✅ Memory-efficient data collection
- ✅ Configurable export options

## TODO Features
- ✅ FastAPI integration to expose tracked metrics via REST API
- ✅ Schedule periodic exports using `APScheduler`
- ✅ Plug-and-play with any Python database client (SQLAlchemy, psycopg2, etc.)
- ✅ Advanced filtering and querying capabilities

---

## 📦 Installation

```bash
pip install pyquerytracker
```

## Usage
### Basic Usage
```python
import time
from pyquerytracker import TrackQuery

@TrackQuery()
def run_query():
    time.sleep(0.3)  # Simulate SQL execution
    return "SELECT * FROM users;"

run_query()
```
### Output
```bash
2025-06-14 14:23:00,123 - pyquerytracker - INFO - Function run_query executed successfully in 305.12ms
```

### With Configure
```
import logging
from pyquerytracker.config import configure

configure(
    slow_log_threshold_ms=200,     # Log queries slower than 200ms
    slow_log_level=logging.DEBUG   # Use DEBUG level for slow logs
)
```

### Output
```bash
2025-06-14 14:24:45,456 - pyquerytracker - WARNING - Slow execution: run_query took 501.87ms
```

### Export to CSV/JSON
```python
import time
from pyquerytracker import TrackQuery, export_data, ExportType, get_summary

@TrackQuery()
def database_query():
    time.sleep(0.1)  # Simulate query execution
    return "SELECT * FROM users;"

# Execute some tracked functions
for i in range(5):
    database_query()

# Export to CSV
export_data(ExportType.CSV, "query_export.csv", include_summary=True)

# Export to JSON
export_data(ExportType.JSON, "query_export.json", include_summary=True)

# Get summary statistics
stats = get_summary()
print(f"Total queries: {stats['total_queries']}")
print(f"Average duration: {stats['average_duration_ms']:.2f}ms")
```

### CSV Export Output Example
```csv
timestamp,function_name,class_name,duration_ms,status,error_message,args_count,kwargs_count
2025-06-14T14:23:00.123456,database_query,,102.34,success,,0,0
2025-06-14T14:23:01.234567,database_query,,98.76,success,,0,0
2025-06-14T14:23:02.345678,database_query,,105.43,success,,0,0

SUMMARY STATISTICS
total_queries,5
successful_queries,5
failed_queries,0
average_duration_ms,101.23
min_duration_ms,98.76
max_duration_ms,105.43
```

### API Reference

#### Export Functions
- [`export_data(export_type, filepath, include_summary=True, clear_after_export=False)`](pyquerytracker/config.py) - Export tracked data to file
- [`get_summary()`](pyquerytracker/config.py) - Get summary statistics
- [`clear_data()`](pyquerytracker/config.py) - Clear all tracked data

#### Export Types
- [`ExportType.CSV`](pyquerytracker/config.py) - Export as CSV format
- [`ExportType.JSON`](pyquerytracker/config.py) - Export as JSON format



