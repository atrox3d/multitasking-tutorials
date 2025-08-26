import time
import asyncio
from concurrent.futures import ProcessPoolExecutor


def timestamp(message:str) -> None:
    global t1
    print(f'{time.perf_counter() - t1:.2f}s | {message}')


def fetch_data(param):
    print((f'do something with {param}...'))
    
    # await asyncio.sleep(param)
    time.sleep(param)               # blocking, can't be awaited
    
    print(f'done with {param}')
    return f'result of {param}'


async def main():
    """
    0s      |         |             1s                  2s
    |       |         |             |                   |   
    process1...sleep1.|............ end process 1       |
    |       |         |             |                   |
    |       process2..|.sleep2......|...................end process2
    |       |         |             |                   |
    |       |         await task1...|
    |                               |                   |
    |                 await task2...|...................|
    """
    timestamp('start')
    loop = asyncio.get_running_loop()                               # get the async event loop
    
    with ProcessPoolExecutor() as excecutor:                        # start ctx manager
        task1 = loop.run_in_executor(excecutor, fetch_data, 1)      # wrap process in task
        task2 = loop.run_in_executor(excecutor, fetch_data, 2)      # wrap process in task
    
        timestamp('await process task1')
        result1 = await task1
        timestamp('fetch 1 fully completed')
        
        timestamp('await process task2')
        result2 = await task2
        timestamp('fetch 2 fully completed')
    return [result1, result2]


if __name__ == "__main__":
    t1 = time.perf_counter()

    results = asyncio.run(main())
    timestamp(results)

    t2 = time.perf_counter()
    print(f'finished in {t2-t1:.2f} seconds')           # time 3s: no performance gain
