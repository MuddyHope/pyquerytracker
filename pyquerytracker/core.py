import time
import logging
import atexit
from functools import update_wrapper
from typing import Any, Callable, TypeVar, Generic

from pyquerytracker.config import get_config
from pyquerytracker.exporter import JsonExporter

# Set up logger
logger = logging.getLogger("pyquerytracker")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

T = TypeVar("T")

# Singleton exporter instance (no global keyword)
_exporter_instance: JsonExporter | None = None


def flush_exported_logs() -> None:
    """Manually flushes the JSON exporter buffer to disk, if initialized."""
    if _exporter_instance is not None:
        _exporter_instance.flush()


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

    def __init__(self) -> None:
        self.config = get_config()
        exporter = JsonExporter(self.config)
        global _exporter_instance  # okay now: short-lived and safe
        _exporter_instance = exporter
        self._exporter = exporter
        atexit.register(self._exporter.flush)

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        def wrapped(*args: Any, **kwargs: Any) -> T:
            start = time.perf_counter()
            class_name = None

            if args:
                possible_self_or_cls = args[0]
                if hasattr(possible_self_or_cls, "__class__"):
                    if isinstance(possible_self_or_cls, type):
                        class_name = possible_self_or_cls.__name__
                    else:
                        class_name = possible_self_or_cls.__class__.__name__

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
                        "%s.%s → Slow execution: took %.2fms",
                        class_name or "<module>",
                        func.__name__,
                        duration,
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
