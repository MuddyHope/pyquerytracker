import time
import functools

class BuiltinPerformanceExporter:
    def __init__(self, output_func=print):
        self.output_func = output_func

    def track(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            elapsed_ms = (end - start) * 1000
            self.output_func(f"Function '{func.__name__}' executed in {elapsed_ms:.2f} ms")
            return result
        return wrapper
