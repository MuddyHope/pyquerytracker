import time
import logging
import inspect
from functools import update_wrapper
from typing import Any, Callable, TypeVar, Generic
from pyquerytracker.config import get_config

logger = logging.getLogger("pyquerytracker")
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.propagate = True

T = TypeVar("T")


class TrackQuery(Generic[T]):
    """
    A decorator to track execution time of synchronous and asynchronous functions.

    Example usage:

    >>> @TrackQuery()
    ... def db_query():
    ...     time.sleep(0.1)
    ...     return "result"

    >>> @TrackQuery()
    ... async def async_query():
    ...     await asyncio.sleep(0.2)
    ...     return "result"
    """
    def __init__(self) -> None:
        self.config = get_config()

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        if inspect.iscoroutinefunction(func):
            async def async_wrapped(*args: Any, **kwargs: Any) -> T:
                return await self._execute(func, args, kwargs, is_async=True)
            return update_wrapper(async_wrapped, func)
        else:
            def sync_wrapped(*args: Any, **kwargs: Any) -> T:
                return self._execute_sync(func, args, kwargs)
            return update_wrapper(sync_wrapped, func)

    def _execute_sync(self, func: Callable[..., T], args: Any, kwargs: Any) -> T:
        import asyncio
        return asyncio.run(self._execute(func, args, kwargs, is_async=False))

    async def _execute(self, func, args, kwargs, is_async=False):
        start = time.perf_counter()
        class_name = None

        if args:
            obj = args[0]
            if hasattr(obj, "__class__"):
                class_name = obj.__class__.__name__ if not isinstance(obj, type) else obj.__name__

        try:
            if is_async:
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            duration = (time.perf_counter() - start) * 1000
            if duration > self.config.slow_log_threshold_ms:
                logger.log(
                    self.config.slow_log_level,
                    f"{class_name + '.' if class_name else ''}{func.__name__} -> Slow execution: took %.2fms",
                    duration,
                )
            else:
                logger.log(
                    self.config.slow_log_level,
                    "Function %s%s executed successfully in %.2fms",
                    f"{class_name + '.' if class_name else ''}",
                    func.__name__,
                    duration,
                    extra={
                        "function_name": func.__name__,
                        "class_name": class_name,
                        "duration_ms": duration,
                        "func_args": args,
                        "func_kwargs": kwargs,
                    },
                )

            return result

        except Exception as e:
            duration = (time.perf_counter() - start) * 1000
            logger.error(
                "Function %s%s failed after %.2fms: %s",
                f"{class_name + '.' if class_name else ''}",
                func.__name__,
                duration,
                str(e),
                exc_info=True,
                extra={
                    "function_name": func.__name__,
                    "class_name": class_name,
                    "duration_ms": duration,
                    "func_args": args,
                    "func_kwargs": kwargs,
                    "error": str(e),
                },
            )
            raise
