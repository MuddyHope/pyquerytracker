
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

## 🔧 Configuration

```python
import logging
from pyquerytracker.config import configure

configure(
    slow_log_threshold_ms=200,     # Log queries slower than 200ms
    slow_log_level=logging.DEBUG   # Use DEBUG level for slow logs
)
```

---

## ⚙️ Usage

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

**Output:**
```
2025-06-14 14:23:00,123 - pyquerytracker - INFO - Function run_query executed successfully in 305.12ms
```

---

### 🧩 Async Support

Use the same decorator with `async` functions or class methods:

```python
import asyncio
from pyquerytracker import TrackQuery

@TrackQuery()
async def fetch_data():
    await asyncio.sleep(0.2)
    return "fetched"

class MyService:
    @TrackQuery()
    async def do_work(self, x, y):
        await asyncio.sleep(0.1)
        return x + y

asyncio.run(fetch_data())
```

---

### 🌐 Run the FastAPI Server

To view tracked query logs via REST, WebSocket, or a Web-based dashboard, start the built-in FastAPI server:

```bash
uvicorn pyquerytracker.api:app --reload
```

- ⚠️ If your project or file structure is different, replace `pyquerytracker.api` with your own module path, like `<your_project_name>.<your_server(file)_name>`.

- Open docs at [http://localhost:8000/docs](http://localhost:8000/docs)
- **Query Dashboard UI:** [http://localhost:8000/dashboard](http://localhost:8000/dashboard)
- REST endpoint: `GET /queries`
- WebSocket stream: `ws://localhost:8000/ws`

Then run your tracked functions in another terminal or script:

```python
@TrackQuery()
def insert_query():
    time.sleep(0.4)
    return "INSERT INTO users ..."
```

You’ll see logs live on the server via API/WebSocket.

---

## 📤 Export Logs

Enable exporting to CSV or JSON by setting config:

```python
from pyquerytracker.config import configure

configure(
    export_type="json",
    export_path="./query_logs.json"
)
```

---

Let us know how you’re using `pyquerytracker` and feel free to contribute!


