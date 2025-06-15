# 🐍 pyquerytracker

**pyquerytracker** is a lightweight Python utility to **track and analyze database query performance** using simple decorators. It enables developers to gain visibility into SQL execution time, log metadata, and export insights in JSON format — with optional FastAPI integration and scheduled reporting.

---

## 🚀 Features

- ✅ Easy-to-use decorator to track function execution (e.g., SQL queries)
- ✅ Capture runtime, function name, args, return values, and more

## TODO Features
- ✅ Export logs to JSON or CSV
- ✅ FastAPI integration to expose tracked metrics via REST API
- ✅ Schedule periodic exports using `APScheduler`
- ✅ Plug-and-play with any Python database client (SQLAlchemy, psycopg2, etc.)
- ✅ Modular and extensible design

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



