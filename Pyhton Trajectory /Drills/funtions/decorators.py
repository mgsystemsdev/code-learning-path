



import time

def timer(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print(f"Time taken: {end - start} seconds")
    return wrapper

@timer
def slow_function():
    for _ in range(1_000_000):
        pass

slow_function()
