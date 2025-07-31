from pathlib import Path
import sys
import time

import numpy as np
import scipy

# just hack the sys.path to import root level packages

ROOT_PATH = str(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0, ROOT_PATH)
from helpers.audio.sinewave import create_sine_wave, create_sinewave_file

DATA_PATH = str(Path(ROOT_PATH) / '.data')
assert Path(DATA_PATH).exists()


def etl(filename: str) -> tuple[str, float]:
    start_time = time.perf_counter()
    sample_rate, data = scipy.io.wavfile.read(filename)
    
    eps = .1
    data += np.random.normal(scale=eps, size=len(data))
    data = np.clip(data, -1.0, 1.0)
    
    new_filename = rename_filepath(filename)
    scipy.io.wavfile.write(new_filename, sample_rate, final_data)
    end_time = time.perf_counter()
    return filename, end_time - start_time


def etl_demo(sounds_path:str) -> None:
    filepaths = Path(sounds_path).glob('*.wav')
    start_time = time.perf_counter()
    for filepath in filepaths:
        _, duration = etl(str(filepath))
        print(f'{filepath}: completed in {duration:.2f}')
    end_time = time.perf_counter()
    total_duration = end_time - start_time
    print(f'Total duration: {total_duration:.2f}')


def rename_filepath(filepath:str, name_suffix:str = '-transformed') -> str:
    return str(Path(filepath).with_stem(
        Path(filepath).stem + name_suffix
    ))


def create_input_wave_files(n:int) -> None:
    for i in range(n):
        create_sinewave_file(f'sine_wave{i}.wav', DATA_PATH)


if __name__ == "__main__":
    print(rename_filepath( str(Path(__file__).resolve())))
    create_input_wave_files(24)
    etl_demo(DATA_PATH)