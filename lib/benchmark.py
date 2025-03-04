from time import time

def time_benchmark(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        func(*args, **kwargs)
        end_time = time()

        total_time_ms = (end_time - start_time) * 1000
        print(f"Total time took {(total_time_ms):.3f} ms")
        
    return wrapper