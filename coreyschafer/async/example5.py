import time
import asyncio


def timestamp(message:str) -> None:
    print(f'{time.perf_counter():.0f} | {message}')


async def fetch_data(param):
    print((f'do something with {param}...'))
    
    # await asyncio.sleep(param)
    time.sleep(param)               # blocking, can't be awaited
    
    print(f'done with {param}')
    return f'result of {param}'


async def main():
    """
    0s      |                    1s         |         2s             3s
    |       |                    |          |         |              |
    task1...time.sleep1..BLOCK...end task1  |         |              |
    |       |                    |          |         |              |
    |       |                    task2......time.sleep2...BLOCK......end task2
    |       |                    |          |         |              |
    |       |                    |          |         |              await task1
    |       |                    |          |         |              |
    |       |                    |          |         |              await task2
    """
    timestamp('start')
    task1 = asyncio.create_task(fetch_data(1))      # task obj, scheduled in the loop, cannot run concurrently because of time.sleep
    task2 = asyncio.create_task(fetch_data(2))      # task obj, scheduled in the loop, cannot run concurrently because of time.sleep
                                                    # 
                                                    # time 0s: task 1 blocks for 1s
                                                    # time 1s: task1 has finished
                                                    # time 1s: task2 starts, blocks for 2 seconds
                                                    
                                                    # time 3s: task2 has finished
    timestamp('await task1')
    result1 = await task1                           # time 3s: main is suspended until task1 is run and has finished
    timestamp('fetch 1 fully completed')
    
    timestamp('await task2')
    result2 = await task2                           # time 3s: main is suspended until task2 is run and has finished
    timestamp('fetch 1 fully completed')
    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
timestamp(results)

t2 = time.perf_counter()
print(f'finished in {t2-t1:.2f} seconds')           # time 3s: no performance gain
