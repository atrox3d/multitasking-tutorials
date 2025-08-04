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
    for filepath in filepaths:
        _, duration = audio.etl(str(filepath))
        # print(f'{filepath}: completed in {duration:.2f}')
    print(f'Successfully processed {len(filepaths)} files')

    end_time = time.perf_counter()
    total_duration = end_time - start_time
    print(f'Total duration: {total_duration:.2f}')


if __name__ == "__main__":
    # strategy pattern
    runner.run(etl_demo, TOTAL_FILES, DATA_PATH)