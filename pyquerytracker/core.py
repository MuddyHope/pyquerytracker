import time
import logging
from functools import update_wrapper
from typing import Any, Callable, TypeVar, Generic


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

    def __init__(self) -> None:
        pass  # Placeholder for future config

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        def wrapped(*args: Any, **kwargs: Any) -> T:
            start = time.perf_counter()
            class_name = None

            # Try to detect if this is an instance or class method
            if args:
                possible_self_or_cls = args[0]
                if hasattr(possible_self_or_cls, "__class__"):
                    if isinstance(possible_self_or_cls, type):
                        # classmethod
                        class_name = possible_self_or_cls.__name__
                    else:
                        # instance method
                        class_name = possible_self_or_cls.__class__.__name__

            try:
                result = func(*args, **kwargs)
                duration = (time.perf_counter() - start) * 1000
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

        return update_wrapper(wrapped, func)
