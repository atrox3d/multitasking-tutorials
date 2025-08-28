import time
import asyncio


def timestamp(message:str) -> None:
    global t1
    print(f'{time.perf_counter() - t1:.2f}s | {message}')


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
    |       task2....sleep2......|...................end task2
    |       |        |           |                   |
    |       |        await task2.|...................|
    |                            |                   |
    |                            |                   await task1
    """
    timestamp('start')
    task1 = asyncio.create_task(fetch_data(1))      # task obj, scheduled in the loop, runs concurrently
    task2 = asyncio.create_task(fetch_data(2))      # task obj, scheduled in the loop, runs concurrently
                                                    # time: 0s
                                                    # ...
                                                    # time 1s: task1 has finished
                                                    # time 2s: task2 has finished
                                                    
    timestamp('await task2')
    result2 = await task2                           # time 2s: main is suspended until task2 is run and has finished
    timestamp('fetch 2 fully completed')    

    timestamp('await task1')
    result1 = await task1                           # time 2s: main is suspended until task1 is run and has finished, result1 was ready after 1s
    timestamp('fetch 1 fully completed')
    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
timestamp(results)

t2 = time.perf_counter()
print(f'finished in {t2-t1:.2f} seconds')           # time 2s: performance gain
