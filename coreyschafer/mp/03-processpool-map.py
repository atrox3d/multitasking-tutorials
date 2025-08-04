from multiprocessing import Process, current_process
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import os


SECONDS = 10
CPUS = os.cpu_count()


def worker(seconds:int) -> None:
    name = current_process().name
    id = current_process().pid
    print(f'worker: {name}:{id}, sleeping {seconds=}')
    time.sleep(seconds)
    return f'worker: {name}:{id}, done'


if __name__ == '__main__':
    print(f'main process: {CPUS = } starting...')
    start = time.perf_counter()

    with ProcessPoolExecutor() as executor:
        secs = [SECONDS for _ in range(CPUS)]
        results = executor.map(worker, secs)
        for result in results:
            print(result)

    stop = time.perf_counter()
    elapsed = stop - start
    print(f'main process: finished in {elapsed=:.2f} seconds')

