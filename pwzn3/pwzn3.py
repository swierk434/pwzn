import numpy as np
import time 

def my_decorator(func):
    def wrapper():
        time_tab = []
        for n in range(10):
            start = time.time()
            func()
            end = time.time()
            time_tab.append(end - start)
        print('max:', max(time_tab))
        print('min:', min(time_tab))
        print('mean:', np.mean(time_tab))
        print('std::', np.std(time_tab))
    return wrapper

@my_decorator
def time_comsuming_function():
    mean = 10
    std_dev = 1
    random_value = np.random.normal(mean, std_dev)
    time.sleep(random_value)
    print("done")

time_comsuming_function()