from pathlib import Path
import sys
import shutil
import time

import numpy as np
import scipy

# just hack the sys.path to import dame level packages
sys.path.insert(0, str(Path(__file__).resolve()))
from audio.sinewave import create_sine_wave, create_sinewave_file


ROOT_PATH = str(Path(__file__).resolve().parent.parent.parent)
DATA_PATH = str(Path(ROOT_PATH) / '.data')


def prepare_datadir(data_path:str=DATA_PATH) -> None:
    '''
    recreate data directory
    '''
    path = Path(DATA_PATH)
    if path.exists():
        print(f"Removing '{path}'...")
        shutil.rmtree(path)
    print(f"Creating '{path}'...")
    path.mkdir(exist_ok=True)
    assert path.exists()


def etl(filepath: str) -> tuple[str, float]:
    '''
    adds noise to wave file
    '''
    start_time = time.perf_counter()
    sample_rate, data = scipy.io.wavfile.read(filepath)

    # The original code had a TypeError because it tried to add a float array (the noise)
    # to an int16 array (the audio data) in-place.
    # The correct way to process audio is to convert it to a floating-point format,
    # apply transformations, and then convert it back to its original integer format.

    # 1. Normalize the int16 data to float64 in the range [-1.0, 1.0]
    if data.dtype != np.int16:
        raise TypeError("This ETL function currently only supports 16-bit WAV files.")
    max_val = np.iinfo(np.int16).max
    data_float = data.astype(np.float64) / max_val

    # 2. Add some random noise. A small epsilon is needed for float signals.
    eps = 0.01
    noisy_data = data_float + np.random.normal(scale=eps, size=len(data_float))

    # 3. Clip the signal to ensure it's within the valid [-1.0, 1.0] range
    clipped_data = np.clip(noisy_data, -1.0, 1.0)

    # 4. Convert the float signal back to int16
    final_data = (clipped_data * max_val).astype(np.int16)

    new_filename = rename_filepath(filepath)
    scipy.io.wavfile.write(new_filename, sample_rate, final_data)
    end_time = time.perf_counter()
    return filepath, end_time - start_time


def etl_demo(sounds_path:str) -> None:
    '''
    loads, adds noise, and saves wave files
    '''
    filepaths = Path(sounds_path).glob('*.wav')
    start_time = time.perf_counter()

    for filepath in filepaths:
        _, duration = etl(str(filepath))
        print(f'{filepath}: completed in {duration:.2f}')
    
    end_time = time.perf_counter()
    total_duration = end_time - start_time
    print(f'Total duration: {total_duration:.2f}')


def rename_filepath(filepath:str, name_suffix:str = '-transformed') -> str:
    '''
    add suffix to filename keeping path and extension
    '''
    return str(Path(filepath).with_stem(
        Path(filepath).stem + name_suffix
    ))


def create_input_wave_files(n:int, data_path:str=DATA_PATH) -> None:
    '''
    creates sample wave files
    '''
    for i in range(n):
        create_sinewave_file(f'sine_wave{i}.wav', data_path)


if __name__ == "__main__":
    # print(rename_filepath( str(Path(__file__).resolve())))
    prepare_datadir(DATA_PATH)
    create_input_wave_files(24, DATA_PATH)
    etl_demo(DATA_PATH)
