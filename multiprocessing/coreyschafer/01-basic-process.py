from multiprocessing import Process, current_process
import time
import os


SECONDS = 5
CPUS = os.cpu_count()


def worker(seconds:int) -> None:
    name = current_process().name
    id = current_process().pid
    print(f'worker: {name}:{id}, sleeping {seconds=}')
    time.sleep(seconds)
    print(f'worker: {name}:{id}, done')


if __name__ == '__main__':
    print(f'main process: {CPUS = } starting...')
    start = time.perf_counter()

    processes = []
    for _ in range(CPUS):
        p = Process(target=worker, args=(SECONDS,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    stop = time.perf_counter()
    elapsed = stop - start
    print(f'main process: finished in {elapsed=:.2f} seconds')

