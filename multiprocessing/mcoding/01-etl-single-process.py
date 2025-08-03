from pathlib import Path
import sys
import time

# just hack the sys.path to import dame level packages
sys.path.insert(0, str(Path(__file__).resolve()))
from helpers import audio
from helpers import runner

ROOT_PATH = str(Path(__file__).resolve().parent.parent.parent)
DATA_PATH = str(Path(ROOT_PATH) / '.data')
TOTAL_FILES = 400


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