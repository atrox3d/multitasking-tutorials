from pathlib import Path
import sys
import time
from typing import Callable

from typer import Option, Typer

# just hack the sys.path to import dame level packages
sys.path.insert(0, str(Path(__file__).resolve()))
from helpers import audio
from helpers import fs

ROOT_PATH = str(Path(__file__).resolve().parent.parent.parent)
DATA_PATH = str(Path(ROOT_PATH) / '.data')


def create_input_wave_files(n:int, data_path:str=DATA_PATH) -> None:
    '''
    creates sample wave files
    '''
    print(f'Creating {n} wave files...')
    for i in range(n):
        audio.create_sinewave_file(f'sine_wave{i:04d}.wav', data_path)
    print(f'Successfully created {n} wave files')


TOTAL_FILES = 400


def run(
    etl: Callable,
    help="A CLI to generate and process audio files.",
):
    app = Typer(
        add_completion=False,
        help=help,
        # invoke_without_command=True,  # This allows the callback to run as the default command
    )


    @app.callback(invoke_without_command=True)
    def main(
        # ctx: Typer,
        total_files: int = Option(TOTAL_FILES, "--files", "-n", help="Number of wave files to generate."),
        cleanup: bool = Option(True, "--cleanup/--no-cleanup", "-c", help="Cleanup data directory after processing")
    ):
        """
        Prepares data, creates wave files, and runs the ETL process.
        """
        # if ctx.invoked_subcommand is None:
        fs.prepare_datadir(DATA_PATH)
        create_input_wave_files(total_files, DATA_PATH)
        
        etl(DATA_PATH)
        
        if cleanup:
            fs.remove_datadir(DATA_PATH)


        app()
