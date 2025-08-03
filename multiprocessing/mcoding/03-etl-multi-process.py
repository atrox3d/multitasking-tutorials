from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
from common import (
    DATA_PATH,
    TOTAL_FILES,
    time,
    Path,
    audio,
    runner,
)


def etl_demo(sounds_path:str) -> None:
    '''
    loads, adds noise, and saves wave files
    '''
    filepaths = list(Path(sounds_path).glob('*.wav'))
    start_time = time.perf_counter()

    print(f'Processing {len(filepaths)} files...')
    with Pool() as pool:
        results = pool.imap_unordered(audio.etl, filepaths)
        # this actually runs the processes
        for filename, duration in results:
            pass
            # print(f'{filename}: completed in {duration:.2f}')
    print(f'Successfully processed {len(filepaths)} files')

    
    end_time = time.perf_counter()
    total_duration = end_time - start_time
    print(f'Total duration: {total_duration:.2f}')


if __name__ == "__main__":
    # strategy pattern
    runner.run(etl_demo, TOTAL_FILES, DATA_PATH)
