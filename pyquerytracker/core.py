import time
import logging
import inspect
# import asyncio
from functools import update_wrapper
from typing import Any, Callable, TypeVar, Generic
from pyquerytracker.config import get_config

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

    Now supports both synchronous and asynchronous functions.

    Logs include:
    - Function name
    - Class name (if method)
    - Execution time (ms)
    - Arguments
    - Errors (if any)
    """

    def __init__(self) -> None:
        self.config = get_config()

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        # Support for async functions
        if inspect.iscoroutinefunction(func):
            async def async_wrapped(*args: Any, **kwargs: Any) -> T:
                return await self._execute(func, args, kwargs, is_async=True)
            return update_wrapper(async_wrapped, func)
        else:
            def sync_wrapped(*args: Any, **kwargs: Any) -> T:
                return self._execute(func, args, kwargs, is_async=False)
            return update_wrapper(sync_wrapped, func)

    async def _execute(self, func, args, kwargs, is_async=False):
        start = time.perf_counter()
        class_name = None

        # Detect class name if method
        if args:
            obj = args[0]
            if hasattr(obj, "__class__"):
                class_name = obj.__class__.__name__ if not isinstance(obj, type) else obj.__name__

        try:
            # Await async functions, call sync ones directly
            if is_async:
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            duration = (time.perf_counter() - start) * 1000
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
                f"{class_name}." if class_name else "",
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
