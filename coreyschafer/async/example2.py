import time
import asyncio


async def fetch_data(param):
    print((f'do something with {param}...'))
    await asyncio.sleep(param)
    print(f'done with {param}')
    return f'result of {param}'


async def main():
    """
    0s                  1s                  2s                  3s                  4s
    |                   |                   |                   |                   |   
    sleep1..............end sleep1          |                   |                   |
    |                   |                   |                   |                   |   
    |                   await coro1.........end coro1
    |                   |                   |                   |                   |
    |                   |                   await coro2.........|...................end coro2
    """
    task1 = fetch_data(1)                   # coroutine obj, runs immediately when awaited
    task2 = fetch_data(2)                   # coroutine obj, runs immediately when awaited
                                            # time 0s
                                            # ...
    print('waiting 1 second...')
    await asyncio.sleep(1)                  # nothing runs for 1 seconds
                                            # time 1s
    
    result1 = await task1                   # time 2s: task1 is run and has finished when awaited
    print('fetch 1 fully completed')
    result2 = await task2                   # time 4s: task2 is run and has finished when awaited
    print('fetch 2 fully completed')
    return [result1, result2]               # time 4s




t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()
print(f'finished in {t2-t1:.2f} seconds')   # no performance gain
