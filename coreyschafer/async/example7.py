import time
import asyncio


def timestamp(message:str) -> None:
    global t1
    print(f'{time.perf_counter() - t1:.2f}s | {message}')


async def fetch_data(param, exception: bool = False):
    print((f'do something with {param}...'))
    
    await asyncio.sleep(param)
    
    print(f'done with {param}')
    
    if exception and param==2:
        raise Exception('Forced Exception')
    return f'result of {param}'


async def main():
    """
    """
    timestamp('start')                              # time 0s:
    
    # gather coroutines
    coroutines = [
        fetch_data(i, True) for i in range(1, 3)    # time 0s: create a list of coroutines
    ]
    
    timestamp('gather coroutines')
    results = await asyncio.gather(
            *coroutines,                            # run concurrently
            return_exceptions=True                  # return exceptions as results, dont stop other coroutines
    )
    timestamp(f'Coroutines results: {results}')     # time 2s
    
    ##########################################################################################################################

    # gather tasks
    timestamp('start')                              # time 0s:
    tasks = [
        asyncio.create_task(fetch_data(i, True))    # time 2s: create a list of tasks that wrap coroutines
        for i in range(1, 3)
    
    ]
    timestamp('gather tasks')
    results = await asyncio.gather(
            *tasks,                                 # run concurrently
            return_exceptions=True                  # return exceptions as results, dont stop other coroutines
    )
    timestamp(f'Tasks results: {results}')          # time 4s
    
    ##########################################################################################################################
    
    # Task Group
    timestamp('start')                              # time 4s:
    async with asyncio.TaskGroup() as tg:
        timestamp('gather results from Task Group')
        results = [
            tg.create_task(fetch_data(i, False))    # time 4s: create a list of tasks in a TaskGroup
            for i in range(1, 3)
    ]
    timestamp(
        f'Task Group results: '                     # time 6s
        f'{[result.result() for result in results]}'
    )
    
    return 'Main Coroutine Done'


t1 = time.perf_counter()

results = asyncio.run(main())
timestamp(results)

t2 = time.perf_counter()
print(f'finished in {t2-t1:.2f} seconds')           # time 3s: no performance gain
