from time import time

# returns extra time_taken_seconds value
def time_benchmark(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        time_taken_seconds = round(time() - start_time, 3)

        return (*result, time_taken_seconds) if isinstance(result, tuple) else (result, time_taken_seconds)
        
    return wrapper