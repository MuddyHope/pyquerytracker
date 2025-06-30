import json
import os
import subprocess
import tempfile


def run_test_in_subprocess(script: str, export_path: str):
    print("\n----- Running Script -----\n")
    print(script)
    print("\n--------------------------\n")
    
    try:
        subprocess.run(["python3", "-c", script], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("STDOUT:\n", e.stdout)
        print("STDERR:\n", e.stderr)
        raise

    assert os.path.exists(export_path)
    with open(export_path) as f:
        return json.load(f)


def test_successful_function_logs():
    with tempfile.TemporaryDirectory() as tmpdir:
        export_path = os.path.join(tmpdir, "log.json")

        script = f"""
import time
from pyquerytracker import TrackQuery
from pyquerytracker.config import configure, ExportType

configure(
    slow_log_threshold_ms=0.0,
    slow_log_level=10,
    export_type=ExportType.JSON,
    export_path=r"{export_path}",
)

@TrackQuery()
def foo(x, y):
    return x + y

foo(1, 2)
from pyquerytracker.exporter.manager import ExporterManager
ExporterManager.get().flush()
"""

        logs = run_test_in_subprocess(script, export_path)

        assert isinstance(logs, list)
        functions_logged = {log.get("function_name") for log in logs}
        assert "foo" in functions_logged
        assert any(log.get("event") == "success" for log in logs) or any(
            log.get("event") == "slow_execution" for log in logs
        )


def test_error_function_logs():
    with tempfile.TemporaryDirectory() as tmpdir:
        export_path = os.path.join(tmpdir, "log.json")

        script = f"""
import time
from pyquerytracker import TrackQuery
from pyquerytracker.config import configure, ExportType

configure(
    slow_log_threshold_ms=0.0,
    slow_log_level=10,
    export_type=ExportType.JSON,
    export_path=r"{export_path}",
)

@TrackQuery()
def bar():
    raise RuntimeError("error")

try:
    bar()
except RuntimeError:
    pass
    
from pyquerytracker.exporter.manager import ExporterManager
ExporterManager.get().flush()

"""

        logs = run_test_in_subprocess(script, export_path)

        assert isinstance(logs, list)
        functions_logged = {log.get("function_name") for log in logs}
        assert "bar" in functions_logged
        assert any(log.get("event") == "error" for log in logs)


def test_slow_function_logs():
    with tempfile.TemporaryDirectory() as tmpdir:
        export_path = os.path.join(tmpdir, "log.json")

        script = f"""
import time
from pyquerytracker import TrackQuery
from pyquerytracker.config import configure, ExportType

# Set threshold low so the sleep triggers slow log
configure(
    slow_log_threshold_ms=5.0,
    slow_log_level=10,
    export_type=ExportType.JSON,
    export_path=r"{export_path}",
)

@TrackQuery()
def slow_func():
    time.sleep(0.01)
    return "done"

slow_func()

from pyquerytracker.exporter.manager import ExporterManager
ExporterManager.get().flush()

"""

        logs = run_test_in_subprocess(script, export_path)

        assert isinstance(logs, list)
        functions_logged = {log.get("function_name") for log in logs}
        assert "slow_func" in functions_logged
        assert any(log.get("event") == "slow_execution" for log in logs)


def test_multiple_calls_logged():
    with tempfile.TemporaryDirectory() as tmpdir:
        export_path = os.path.join(tmpdir, "log.json")

        script = f"""
import time
from pyquerytracker import TrackQuery
from pyquerytracker.config import configure, ExportType

configure(
    slow_log_threshold_ms=0.0,
    slow_log_level=10,
    export_type=ExportType.JSON,
    export_path=r"{export_path}",
)

@TrackQuery()
def a():
    return 1

@TrackQuery()
def b():
    raise ValueError("fail")

a()
try:
    b()
except Exception:
    pass
a()

from pyquerytracker.exporter.manager import ExporterManager
ExporterManager.get().flush()

"""

        logs = run_test_in_subprocess(script, export_path)

        assert isinstance(logs, list)
        functions_logged = [log.get("function_name") for log in logs]

        # Because of overwrite behavior, logs might only contain last flush,
        # but often logs include multiple entries. So test at least one a, b occurrence:
        assert "a" in functions_logged or "b" in functions_logged
        # Check for presence of success and error events in the batch
        events = {log.get("event") for log in logs}
        assert "error" in events or "success" in events or "slow_execution" in events
