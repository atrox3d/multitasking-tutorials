from pathlib import Path
import time
import numpy as np
import scipy
from scipy.io.wavfile import write

from helpers import fs

# --- Parameters for the audio signal ---
SAMPLE_RATE = 44100  # Samples per second (CD quality)
DURATION = 5.0  # Seconds
FREQUENCY = 440.0  # Hz (A4 note)
AMPLITUDE = 0.8  # Amplitude (0.0 to 1.0)
OUTPUT_FILENAME = "sine_wave_440hz.wav"


def create_sine_wave(
    frequency: float, duration: float, sample_rate: int, amplitude: float
) -> np.ndarray:
    """Generates a sine wave signal."""
    num_samples = int(sample_rate * duration)
    time_array = np.linspace(0.0, duration, num_samples, endpoint=False)
    
    # Generate the sine wave
    wave = amplitude * np.sin(2.0 * np.pi * frequency * time_array)
    return wave


def create_sinewave_file(
    output_filename: str,
    output_dir:str = '',
    sample_rate: int = SAMPLE_RATE,
    duration: float = DURATION,
    frequency: float = FREQUENCY,
    amplitude: float = AMPLITUDE,
) -> None:
    # print(f"Generating a {duration}s sine wave at {frequency}Hz...")

    # 1. Generate the floating-point audio signal
    audio_signal = create_sine_wave(frequency, duration, sample_rate, amplitude)

    # 2. Scale for 16-bit WAV file format
    # WAV files use integers. 16-bit PCM is common, with values from -32768 to 32767.
    # We scale our float signal (from -1.0 to 1.0) to this range.
    scaled_signal = np.int16(audio_signal * 32767)

    # 3. Write to a WAV file
    # write(filename, sample_rate, data)
    output_filepath = Path(output_dir) / output_filename
    write(output_filepath, sample_rate, scaled_signal)

    # print(f"Successfully created '{output_filepath}'")
    # print("You can now play this file with any audio player.")




def etl(filepath: str) -> tuple[str, float]:
    '''
    adds noise to wave file
    '''

    # extract
    start_time = time.perf_counter()
    sample_rate, data = scipy.io.wavfile.read(filepath)

    # transform
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

    # load
    new_filename = fs.rename_filepath(filepath)
    scipy.io.wavfile.write(new_filename, sample_rate, final_data)
    end_time = time.perf_counter()
    return filepath, end_time - start_time

