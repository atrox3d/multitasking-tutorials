from pathlib import Path
import numpy as np
from scipy.io.wavfile import write

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
    print(f"Generating a {duration}s sine wave at {frequency}Hz...")

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

    print(f"Successfully created '{output_filepath}'")
    print("You can now play this file with any audio player.")