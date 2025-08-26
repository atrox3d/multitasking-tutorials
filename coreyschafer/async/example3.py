import time
import asyncio


async def fetch_data(param):
    print((f'do something with {param}...'))
    await asyncio.sleep(param)
    print(f'done with {param}')
    return f'result of {param}'


async def main():
    """
    0s      |        |           1s                  2s
    |       |        |           |                   |   
    task1...sleep1...|...........end task1           |
    |       |        |           |                   |
    |       |        |           await task1
    |       |        |           |                   |
    |       task2....sleep2......|...................end task2
    |                            |                   |
    |                            |                   await task2
    """
    task1 = asyncio.create_task(fetch_data(1))      # task obj, scheduled in the loop, runs concurrently
    task2 = asyncio.create_task(fetch_data(2))      # task obj, scheduled in the loop, runs concurrently
                                                    # time: 0s
                                                    # ...
                                                    # time 1s: task1 has finished
                                                    # time 1s: task2 still running
                                                    
    result1 = await task1                           # time 1s: main is suspended until task1 is run and has finished
    print('fetch 1 fully completed')
    
                                                    # time 2s: task2 has finished
    result2 = await task2                           # time 2s: main is suspended until task2 is run and has finished
    print('fetch 2 fully completed')
    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()
print(f'finished in {t2-t1:.2f} seconds')           # time 2s: performance gain
