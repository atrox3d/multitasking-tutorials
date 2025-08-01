from pathlib import Path
import time

# The common CLI logic is now in cli_base
from cli_base import run
from helpers import audio


def etl_demo(sounds_path: str) -> None:
    """
    Loads, adds noise, and saves wave files sequentially.
    """
    filepaths = Path(sounds_path).glob('*.wav')
    start_time = time.perf_counter()

    for filepath in filepaths:
        _, duration = audio.etl(str(filepath))
        print(f'{filepath.name}: completed in {duration:.2f}')

    end_time = time.perf_counter()
    total_duration = end_time - start_time
    print(f'Total duration: {total_duration:.2f}')


if __name__ == "__main__":
    run(
        etl_function=etl_demo,
        cli_help="A CLI to generate and process audio files sequentially."
    )
