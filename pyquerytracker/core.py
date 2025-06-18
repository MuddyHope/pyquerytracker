import time
import logging
import atexit
from functools import update_wrapper
from typing import Any, Callable, TypeVar, Generic, Optional

from pyquerytracker.config import get_config, ExportType
from pyquerytracker.exporter import JsonExporter
from pyquerytracker.exporter.utils import _ExporterManager

# Set up logger (unchanged)
logger = logging.getLogger("pyquerytracker")
if not logger.handlers:
    handler = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

T = TypeVar("T")


class TrackQuery(Generic[T]):
    """
    Class-based decorator to track and log the execution time of functions or methods.

    Logs include:
    - Function name
    - Class name (if method)
    - Execution time (ms)
    - Arguments
    - Errors (if any)
    - Export to JSON if configured

    Usage:
        @TrackQuery()
        def my_function():
            ...
    """

    # shared exporter and the values that built it
    _exporter: JsonExporter | None = None
    _last_export_path: Optional[str] = None
    _last_export_type: Optional[ExportType] = None

    def __init__(self) -> None:
        cfg = get_config()

        # detect “first time” OR config’s export settings changed
        need_rebuild = (
            TrackQuery._exporter is None
            or cfg.export_path != TrackQuery._last_export_path
            or cfg.export_type != TrackQuery._last_export_type
        )

        if need_rebuild:
            exporter = JsonExporter(cfg)
            _ExporterManager.set(exporter)
            atexit.register(exporter.flush)

            TrackQuery._exporter = exporter
            TrackQuery._last_export_path = cfg.export_path
            TrackQuery._last_export_type = cfg.export_type

        # instance fields
        self.config = cfg
        self._exporter = TrackQuery._exporter

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        def wrapped(*args: Any, **kwargs: Any) -> T:
            start = time.perf_counter()
            class_name: Optional[str] = None

            if args:
                first = args[0]
                if hasattr(first, "__class__"):
                    class_name = (
                        first.__name__
                        if isinstance(first, type)
                        else first.__class__.__name__
                    )

            try:
                result = func(*args, **kwargs)
                duration = (time.perf_counter() - start) * 1000
                log_data = {
                    "event": (
                        "slow_execution"
                        if duration > self.config.slow_log_threshold_ms
                        else "normal_execution"
                    ),
                    "function_name": func.__name__,
                    "class_name": class_name,
                    "duration_ms": duration,
                    "func_args": repr(args),
                    "func_kwargs": repr(kwargs),
                }

                if duration > self.config.slow_log_threshold_ms:
                    logger.log(
                        self.config.slow_log_level,
                        "Function %s.%s took %.2fms, slower than %.2fms",
                        class_name or "<module>",
                        func.__name__,
                        duration,
                        self.config.slow_log_threshold_ms,
                    )
                else:
                    logger.info(
                        "Function %s%s executed successfully in %.2fms",
                        f"{class_name}." if class_name else "",
                        func.__name__,
                        duration,
                        extra=log_data,
                    )

                self._exporter.append(log_data)
                return result

            except Exception as e:
                duration = (time.perf_counter() - start) * 1000
                log_data = {
                    "event": "error",
                    "function_name": func.__name__,
                    "class_name": class_name,
                    "duration_ms": duration,
                    "func_args": repr(args),
                    "func_kwargs": repr(kwargs),
                    "error": str(e),
                }

                logger.error(
                    "Function %s%s failed after %.2fms: %s",
                    f"{class_name}." if class_name else "",
                    func.__name__,
                    duration,
                    str(e),
                    exc_info=True,
                    extra=log_data,
                )

                self._exporter.append(log_data)
                raise

        return update_wrapper(wrapped, func)
