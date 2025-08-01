from pathlib import Path
import sys
import time

from typer import Option, Typer

# just hack the sys.path to import dame level packages
sys.path.insert(0, str(Path(__file__).resolve()))
from helpers import audio
from helpers import fs

ROOT_PATH = str(Path(__file__).resolve().parent.parent.parent)
DATA_PATH = str(Path(ROOT_PATH) / '.data')


def etl_demo(sounds_path:str) -> None:
    '''
    loads, adds noise, and saves wave files
    '''
    filepaths = Path(sounds_path).glob('*.wav')
    start_time = time.perf_counter()

    for filepath in filepaths:
        _, duration = audio.etl(str(filepath))
        print(f'{filepath}: completed in {duration:.2f}')
    
    end_time = time.perf_counter()
    total_duration = end_time - start_time
    print(f'Total duration: {total_duration:.2f}')


def create_input_wave_files(n:int, data_path:str=DATA_PATH) -> None:
    '''
    creates sample wave files
    '''
    for i in range(n):
        audio.create_sinewave_file(f'sine_wave{i:04d}.wav', data_path)


app = Typer(
    help="A CLI to generate and process audio files.",
    add_completion=False,
    # invoke_without_command=True,  # This allows the callback to run as the default command
)

TOTAL_FILES = 400

@app.callback(invoke_without_command=True)
def main(
    # ctx: Typer,
    total_files: int = Option(TOTAL_FILES, "--files", "-n", help="Number of wave files to generate."),
    cleanup: bool = Option(True, "--cleanup", "-c", help="Cleanup data directory after processing")
):
    """
    Prepares data, creates wave files, and runs the ETL process.
    """
    # if ctx.invoked_subcommand is None:
    fs.prepare_datadir(DATA_PATH)
    create_input_wave_files(total_files, DATA_PATH)
    etl_demo(DATA_PATH)
    if cleanup:
        fs.remove_datadir(DATA_PATH)


if __name__ == "__main__":
    app()
