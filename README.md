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

```python
from pyquerytracker import track_query

@track_query
def run_query():
    # Simulate SQL execution
    time.sleep(0.3)
    return "SELECT * FROM users;"

run_query()
```