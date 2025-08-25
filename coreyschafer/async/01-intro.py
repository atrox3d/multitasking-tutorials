import asyncio
import time


def sync_function(test_param: str) -> str:
    print('this is a synchronous function.')
    
    time.sleep(0.1)
    
    return f'sync result: {test_param}'


async def async_function(test_param: str) -> str:
    print('this is an asynchronous function.')
    
    await asyncio.sleep(0.1)
    
    return f'async result: {test_param}'


async def main():
    sync_result = sync_function('test')                 # call normal synchronous function
    print(f'{sync_result = }\n')
    
    ##########################################################################################################################
    
    loop = asyncio.get_running_loop()                   # get the async loop
    future = loop.create_future()                       # futures are low-level, awaitable, promise-like objects
    print(f'empty future: {future}')                    # futures have state (pending, canceled, ...)
    
    future.set_result('future result: test')            # futures hold future results
    future_result = await future                        # await the future to get the result
    print(f'{future_result = }\n')
    
    ##########################################################################################################################
    
    coroutine_obj = async_function('test')              # coroutines functions are defined by async def, are pausable
    print(f'coroutine object: {coroutine_obj}')         # coroutines objects are awaytables 
    
    coroutine_result = await coroutine_obj              # awaiting the coroutine object schedules and runs it
    print(f'{coroutine_result = }\n')                   # and returns the result
    
    ##########################################################################################################################
    
    task = asyncio.create_task(async_function('test'))  # a task is a wrapper to a coroutine that is scheduled
    print(f'task object: {task}')                       # to be run whenever possible
    
    task_result = await task                            # awaiting the task returns the result when possible
    print(f'{task_result = }')


if __name__ == "__main__":
    asyncio.run(main())