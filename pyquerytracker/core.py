import time
import logging
import json
import os
from functools import update_wrapper
from typing import Any, Callable, TypeVar, Generic
from pyquerytracker.config import get_config, ExportType

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

    def export_log(self, log_data: dict):
        """
        Export log data to a JSON file if configured.
        
        Parameters:
            log_data (dict): The data to log and export.
        """
        if self.config.export_path and self.config.export_type == ExportType.JSON:
            os.makedirs(os.path.dirname(self.config.export_path), exist_ok=True)
            with open(self.config.export_path, "a", encoding="utf-8") as f:
                json.dump(log_data, f)
                f.write("\n")

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        def wrapped(*args: Any, **kwargs: Any) -> T:
            start = time.perf_counter()
            class_name = None

            # Detect if it's an instance or class method
            if args:
                possible_self_or_cls = args[0]
                if hasattr(possible_self_or_cls, "__class__"):
                    if isinstance(possible_self_or_cls, type):
                        class_name = possible_self_or_cls.__name__  # classmethod
                    else:
                        class_name = (
                            possible_self_or_cls.__class__.__name__
                        )  # instance method

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
                        f"{class_name}.{func.__name__} -> Slow execution: took %.2fms",
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

                self.export_log(log_data)
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
                self.export_log(log_data)
                raise

        return update_wrapper(wrapped, func)
