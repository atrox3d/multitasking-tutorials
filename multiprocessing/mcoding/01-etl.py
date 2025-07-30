from pathlib import Path
import sys
import time

import numpy as np
import scipy

# just hack the sys.path to import root level packages
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from helpers.audio.sinewave import create_sine_wave

def etl(filename:str) -> tuple[str|float]:
    start_time = time.perf_counter()
    sample_rate, data = scipy.io.wavfile.read(filename)
    
    eps = .1
    data += np.random.normal(scale=eps, size=len(data))
    data = np.clip(data, -1.0, 1.0)
    
    new_filename = rename_filepath(filename)
    scipy.io.wavfile.write(new_filename, sample_rate, data)
    end_time = time.perf_counter()
    return filename, end_time - start_time


def rename_filepath(filepath:str, name_suffix:str = '-transformed') -> str:
    return Path(filepath).with_stem(
        Path(filepath).stem + name_suffix
    )


if __name__ == "__main__":
    print(rename_filepath(
        str(Path(__file__).resolve())
    ))