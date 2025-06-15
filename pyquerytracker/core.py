import time
import logging
import json
from functools import update_wrapper
from typing import Any, Callable, TypeVar, Generic, Optional


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

    Usage:
        @TrackQuery()
        def my_function():
            ...
    """

    def __init__(self, json_log_path: Optional[str] = None) -> None:
        self.json_log_path = json_log_path

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        def wrapped(*args: Any, **kwargs: Any) -> T:
            start = time.perf_counter()
            class_name = None

            if args:
                possible_self_or_cls = args[0]
                if hasattr(possible_self_or_cls, "__class__"):
                    class_name = (
                        possible_self_or_cls.__name__
                        if isinstance(possible_self_or_cls, type)
                        else possible_self_or_cls.__class__.__name__
                    )

            log_data = {
                "function_name": func.__name__,
                "class_name": class_name,
                "func_args": repr(args),
                "func_kwargs": repr(kwargs),
                "duration_ms": None,
                "error": None,
            }

            try:
                result = func(*args, **kwargs)
                duration = (time.perf_counter() - start) * 1000
                log_data["duration_ms"] = duration

                logger.info(
                    "Function %s%s executed successfully in %.2fms",
                    f"{class_name}." if class_name else "",
                    func.__name__,
                    duration,
                    extra=log_data,
                )

                if self.json_log_path:
                    self._append_to_json_log(log_data)

                return result
            except Exception as e:
                duration = (time.perf_counter() - start) * 1000
                log_data["duration_ms"] = duration
                log_data["error"] = str(e)

                logger.error(
                    "Function %s%s failed after %.2fms: %s",
                    f"{class_name}." if class_name else "",
                    func.__name__,
                    duration,
                    str(e),
                    exc_info=True,
                    extra=log_data,
                )

                if self.json_log_path:
                    self._append_to_json_log(log_data)

                raise

        return update_wrapper(wrapped, func)

    def _append_to_json_log(self, log_data: dict):
        try:
            with open(self.json_log_path, "a", encoding="utf-8") as f:
                json.dump(log_data, f)
                f.write("\n")
        except Exception as e:
            logger.warning("Failed to write JSON log: %s", str(e))
