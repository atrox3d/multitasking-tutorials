import time


def fetch_data(param):
    print((f'do something with {param}...'))
    time.sleep(param)
    print(f'done with {param}')
    return f'result of {param}'


def main():
    """
    0s                  1s                  2s                  3s
    |                   |                   |                   |
    fetch_data(1).......end fetch_data(1)   |                   |
    |                   |                   |                   |
    |                   fetch_data(2).......|...................end fetch_data(1)
    """
    result1 = fetch_data(1)             # time 1s: task1 has finished
    print('fetch 1 fully completed')
    result2 = fetch_data(2)             # time 3s: task2 has finished
    print('fetch 2 fully completed')
    return [result1, result2]


t1 = time.perf_counter()

results = main()
print(results)

t2 = time.perf_counter()
print(f'finished in {t2-t1:.2f} seconds')
