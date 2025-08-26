import time
import asyncio


def fetch_data(param):
    print((f'do something with {param}...'))
    
    # await asyncio.sleep(param)
    time.sleep(param)               # blocking, can't be awaited
    
    print(f'done with {param}')
    return f'result of {param}'


async def main():
    """
    0s      |        |             1s                  2s
    |       |        |             |                   |   
    thread1...sleep1.|............ end thread1           |
    |       |        |             |                   |
    |       thread2....sleep2......|...................end thread2
    |       |        |             |                   |
    |       |        await task1...|
    |                              |                   |
    |                await task2...|...................|
    """
    task1 = asyncio.create_task(                    # task obj, scheduled in the loop
        asyncio.to_thread(                          # ** wraps blocking coro in thread to free event loop **
            fetch_data, 1                           # coro obj, blocking, scheduled in the loop, runs concurrently
        )
    )
    task2 = asyncio.create_task(                    # task obj, scheduled in the loop
        asyncio.to_thread(                          # ** wraps blocking coro in thread to free event loop **
            fetch_data, 2                           # coro obj, blocking, scheduled in the loop, runs concurrently
        )
    )
                                                    # 
    result1 = await task1                           # time 0s: main is suspended until task1 is run and has finished
                                                    # time 0s: task 1 blocks for 1s
                                                    # time 0s: task2 blocks for 2s
                                                    # time 1s: task1 has finished
    print('fetch 1 fully completed')
                                                    
    result2 = await task2                           # time 1s: main is suspended until task2 is run and has finished
                                                    # time 2s: task2 has finished
    print('fetch 2 fully completed')
    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()
print(f'finished in {t2-t1:.2f} seconds')           # time 3s: no performance gain
