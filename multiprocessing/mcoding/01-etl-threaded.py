from pathlib import Path
import time
from multiprocessing.pool import ThreadPool

# The common CLI logic is now in cli_base
from cli_base import run
from helpers import audio


def etl_demo(sounds_path: str) -> None:
    """
    Loads, adds noise, and saves wave files using a thread pool.
    """
    filepaths = Path(sounds_path).glob('*.wav')
    start_time = time.perf_counter()

    with ThreadPool() as pool:
        # Explicitly convert Path objects to strings for consistency
        for filename, duration in pool.imap_unordered(audio.etl, map(str, filepaths)):
            print(f'{filename}: completed in {duration:.2f}')

    end_time = time.perf_counter()
    total_duration = end_time - start_time
    print(f'Total duration: {total_duration:.2f}')


if __name__ == "__main__":
    run(
        etl_function=etl_demo,
        cli_help="A CLI to generate and process audio files using threads."
    )
