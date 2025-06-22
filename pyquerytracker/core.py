import asyncio
import time
from functools import update_wrapper
from typing import Any, Callable, Generic, TypeVar

from pyquerytracker.config import get_config
from pyquerytracker.exporter.base import NullExporter
from pyquerytracker.exporter.manager import ExporterManager
from pyquerytracker.utils.logger import QueryLogger

logger = QueryLogger.get_logger()

T = TypeVar("T")


class TrackQuery(Generic[T]):
    """
    Class-based decorator to track and log the execution time of functions or methods.

    Works with both synchronous and asynchronous functions.

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

        @TrackQuery()
        async def my_async_function():
            ...
    """

    def __init__(self) -> None:
        self.config = get_config()
        if self.config.export_type and self.config.export_path:
            exporter = ExporterManager.create_exporter(self.config)
            ExporterManager.set(exporter)
            self.exporter = exporter
        else:
            self.exporter = NullExporter()

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        if asyncio.iscoroutinefunction(func):

            async def async_wrapped(*args: Any, **kwargs: Any) -> T:
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
                    result = await func(*args, **kwargs)
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
                            f"{class_name}.{func.__name__} -> "
                            f"Slow execution: took {duration:.2f}ms",
                        )
                    else:
                        logger.info(
                            "Function %s%s executed successfully in %.2fms",
                            f"{class_name}." if class_name else "",
                            func.__name__,
                            duration,
                            extra=log_data,
                        )
                    self.exporter.append(log_data)
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
                    self.exporter.append(log_data)
                    return None

            return update_wrapper(async_wrapped, func)

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
                        f"{class_name}.{func.__name__} -> "
                        f"Slow execution: took {duration:.2f}ms",
                    )
                else:
                    logger.info(
                        "Function %s%s executed successfully in %.2fms",
                        f"{class_name}." if class_name else "",
                        func.__name__,
                        duration,
                        extra=log_data,
                    )
                self.exporter.append(log_data)
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
                self.exporter.append(log_data)
                return None

        return update_wrapper(wrapped, func)
