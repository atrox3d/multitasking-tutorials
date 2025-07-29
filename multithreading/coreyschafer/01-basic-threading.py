from threading import Thread, Lock, current_thread
import time


SECONDS = 1
THREADS = 10


def worker(seconds:int) -> None:
    name = current_thread().name
    id = current_thread().ident
    print(f'worker: {name}:{id}, sleeping {seconds=}')
    time.sleep(seconds)
    print(f'worker: {name}:{id}, done')


if __name__ == '__main__':
    print('main thread: starting...')
    start = time.perf_counter()

    threads = []
    for _ in range(THREADS):
        t = Thread(target=worker, args=(SECONDS,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    stop = time.perf_counter()
    elapsed = stop - start
    print(f'main thread: finished in {elapsed=:.2f} seconds')

