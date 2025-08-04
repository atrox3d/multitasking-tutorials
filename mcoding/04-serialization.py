from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
import time
import numpy as np


def run_normal(worker, items):
    start_time = time.perf_counter()
    
    results = list(map(worker, items))
    
    end_time = time.perf_counter()
    total_duration = end_time - start_time
    print(f'run_normal Total duration: {total_duration:.2f}')
    return results


def run_multiprocess(worker, items, processes=None, chunksize=None):
    start_time = time.perf_counter()
    
    with Pool(processes=processes) as pool:
        results = pool.map(worker, items, chunksize=chunksize)
        for result in results:
            pass
    
    end_time = time.perf_counter()
    total_duration = end_time - start_time
    print(f'run_mp Total duration: {total_duration:.2f}')
    return results


def times_10(x):
    return x * 10


def return_lambda(x):
    return lambda x: x + 1


def compare_mp_to_normal(worker, items):
    print()
    run_normal(worker, items)
    run_multiprocess(worker, items)


def noop(x):
    pass



if __name__ == "__main__":
    # pitfall 1: creating processes and serializing has overhead
    compare_mp_to_normal(times_10, range(1000))

    # pitfall 2: parameters must be serializable
    try:
        compare_mp_to_normal(print, [lambda x:x+1])
    except Exception as e:
        print(e)

    # pitfall 3: return values must be serializable
    try:
        compare_mp_to_normal(return_lambda, range(10))
    except Exception as e:
        print(e)
    
    
    # pitfall 4: do not pass too much data, use a str message on how to build the data
    compare_mp_to_normal(noop, [np.random.normal(size=10_000) for _ in range(100)])
    
    
