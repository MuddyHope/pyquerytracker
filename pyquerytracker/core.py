import asyncio
import logging
<<<<<<< Updated upstream
import inspect
=======
import time
>>>>>>> Stashed changes
from functools import update_wrapper
from typing import Any, Callable, Generic, TypeVar

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

<<<<<<< Updated upstream
    Example usage:

    >>> @TrackQuery()
    ... def db_query():
    ...     time.sleep(0.1)
    ...     return "result"

    >>> @TrackQuery()
    ... async def async_query():
    ...     await asyncio.sleep(0.2)
    ...     return "result"
=======
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
>>>>>>> Stashed changes
    """
    def __init__(self) -> None:
        self.config = get_config()

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
<<<<<<< Updated upstream
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
=======
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
                    if duration > self.config.slow_log_threshold_ms:
                        # FIX (line-too-long): Shortened the log message text
                        log_msg = f"Slow: {class_name}.{func.__name__} took %.2fms"
                        logger.log(
                            self.config.slow_log_level,
                            log_msg,
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
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
=======
                duration = (time.perf_counter() - start) * 1000
                if duration > self.config.slow_log_threshold_ms:
                    # FIX (line-too-long): Shortened the log message text
                    log_msg = f"Slow: {class_name}.{func.__name__} took %.2fms"
                    logger.log(
                        self.config.slow_log_level,
                        log_msg,
                        duration,
                    )
>>>>>>> Stashed changes

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
