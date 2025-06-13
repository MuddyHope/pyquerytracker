import time
import logging
from functools import wraps
from typing import Any, Callable, TypeVar, cast

# Configure the logger for this module
logger = logging.getLogger(__name__)

# Set up a default handler if none exists
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

T = TypeVar("T")


def track_query(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator that measures and logs the execution time of the decorated function.
    Logs include function name, execution time, and any arguments passed.

    Args:
        func (callable): The function whose execution time is to be tracked.

    Returns:
        callable: The wrapped function that, when called, logs the duration
                  of its execution and returns the original function's result.

    Example:
        @track_query
        def my_function():
            pass
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            duration = (time.perf_counter() - start) * 1000

            logger.info(
                "Function %s executed successfully in %.2fms",
                func.__name__,
                duration,
                extra={
                    "function_name": func.__name__,
                    "duration_ms": duration,
                    "func_args": args,
                    "func_kwargs": kwargs,
                },
            )
            return result
        except Exception as e:
            duration = (time.perf_counter() - start) * 1000

            logger.error(
                "Function %s failed after %.2fms: %s",
                func.__name__,
                duration,
                str(e),
                exc_info=True,
                extra={
                    "function_name": func.__name__,
                    "duration_ms": duration,
                    "func_args": args,
                    "func_kwargs": kwargs,
                    "error": str(e),
                },
            )
            raise

    return cast(Callable[..., T], wrapper)
