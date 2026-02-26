from functools import wraps
import time

def timing(func):
    """Measure how long a function takes to execute"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⏱️  {func.__name__}() took {end_time - start_time:.4f} seconds")
        return result
    return wrapper
