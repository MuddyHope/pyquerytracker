import time
from functools import wraps

def track_query(func):
    """
    Decorator that measures and logs the execution time of the decorated function.

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
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        # TODO: Log or save metadata
        print(f"Function {func.__name__} took {duration:.4f}s")
        return result
    return wrapper
