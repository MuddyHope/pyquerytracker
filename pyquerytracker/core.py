import asyncio
import time
from functools import update_wrapper
from typing import Any, Callable, Generic, Optional, TypeVar

from pyquerytracker.config import get_config
from pyquerytracker.db.writer import DBWriter
from pyquerytracker.exporter.base import NullExporter
from pyquerytracker.exporter.manager import ExporterManager
from pyquerytracker.tracker import store_tracked_query
from pyquerytracker.utils.logger import QueryLogger

logger = QueryLogger.get_logger()

T = TypeVar("T")


class TrackQuery(Generic[T]):
    def __init__(self) -> None:
        self.config = get_config()
        if self.config.export_type and self.config.export_path:
            exporter = ExporterManager.create_exporter(self.config)
            ExporterManager.set(exporter)
            self.exporter = exporter
        else:
            self.exporter = NullExporter()

    def _extract_class_name(self, args: Any) -> Optional[str]:
        if args:
            obj = args[0]
            if hasattr(obj, "__class__"):
                return obj.__name__ if isinstance(obj, type) else obj.__class__.__name__
        return None

    # pylint: disable=too-many-positional-arguments
    def _build_log_data(self, func, class_name, duration, args, kwargs, error=None):
        data = {
            "event": (
                "error"
                if error
                else (
                    "slow_execution"
                    if duration > self.config.slow_log_threshold_ms
                    else "normal_execution"
                )
            ),
            "function_name": func.__name__,
            "class_name": class_name,
            "duration_ms": duration,
            "func_args": repr(args),
            "func_kwargs": repr(kwargs),
        }
        if error:
            data["error"] = str(error)
        return data

    def _handle_export(self, log_data):
        self.exporter.append(log_data)
        if self.config.persist_to_db:
            DBWriter.save(log_data)
        store_tracked_query(log_data)

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        if asyncio.iscoroutinefunction(func):

            async def async_wrapped(*args: Any, **kwargs: Any) -> T:
                start = time.perf_counter()
                class_name = self._extract_class_name(args)

                try:
                    result = await func(*args, **kwargs)
                    duration = (time.perf_counter() - start) * 1000
                    log_data = self._build_log_data(
                        func, class_name, duration, args, kwargs
                    )

                    if duration > self.config.slow_log_threshold_ms:
                        logger.log(
                            self.config.slow_log_level,
                            "%s%s -> Slow execution: took %.2fms",
                            f"{class_name}." if class_name else "",
                            func.__name__,
                            duration,
                            extra=log_data,
                        )
                    else:
                        logger.info(
                            "Function %s%s executed successfully in %.2fms",
                            f"{class_name}." if class_name else "",
                            func.__name__,
                            duration,
                            extra=log_data,
                        )

                    self._handle_export(log_data)
                    return result

                except Exception as e:
                    duration = (time.perf_counter() - start) * 1000
                    log_data = self._build_log_data(
                        func, class_name, duration, args, kwargs, error=e
                    )
                    logger.error(
                        "Function %s%s failed after %.2fms: %s",
                        f"{class_name}." if class_name else "",
                        func.__name__,
                        duration,
                        str(e),
                        exc_info=True,
                        extra=log_data,
                    )
                    self._handle_export(log_data)
                    return None

            return update_wrapper(async_wrapped, func)

        def wrapped(*args: Any, **kwargs: Any) -> T:
            start = time.perf_counter()
            class_name = self._extract_class_name(args)

            try:
                result = func(*args, **kwargs)
                duration = (time.perf_counter() - start) * 1000
                log_data = self._build_log_data(
                    func, class_name, duration, args, kwargs
                )

                if duration > self.config.slow_log_threshold_ms:
                    logger.log(
                        self.config.slow_log_level,
                        "%s%s -> Slow execution: took %.2fms",
                        f"{class_name}." if class_name else "",
                        func.__name__,
                        duration,
                        extra=log_data,
                    )
                else:
                    logger.info(
                        "Function %s%s executed successfully in %.2fms",
                        f"{class_name}." if class_name else "",
                        func.__name__,
                        duration,
                        extra=log_data,
                    )

                self._handle_export(log_data)
                return result

            except Exception as e:
                duration = (time.perf_counter() - start) * 1000
                log_data = self._build_log_data(
                    func, class_name, duration, args, kwargs, error=e
                )
                logger.error(
                    "Function %s%s failed after %.2fms: %s",
                    f"{class_name}." if class_name else "",
                    func.__name__,
                    duration,
                    str(e),
                    exc_info=True,
                    extra=log_data,
                )
                self._handle_export(log_data)
                return None

        return update_wrapper(wrapped, func)
