from threading import Thread, Lock, current_thread
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


SECONDS = 1
THREADS = 10


def worker(seconds:int) -> str:
    name = current_thread().name
    id = current_thread().ident
    print(f'worker: {name}:{id}, sleeping {seconds=}')
    time.sleep(seconds)
    return f'worker: {name}:{id}, done'


if __name__ == '__main__':
    print('main thread: starting...')
    start = time.perf_counter()

    with ThreadPoolExecutor() as executor:
        results = [executor.submit(worker, SECONDS) for _ in range(THREADS)]
        for f in as_completed(results):
            print(f.result())

    stop = time.perf_counter()
    elapsed = stop - start
    print(f'main thread: finished in {elapsed=:.2f} seconds')

