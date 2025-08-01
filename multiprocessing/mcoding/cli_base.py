from pathlib import Path
from typing import Callable

from typer import Option, Typer

# Assuming 'helpers' is a package within the same directory or a properly installed one.
from helpers import audio
from helpers import fs

ROOT_PATH = str(Path(__file__).resolve().parent.parent.parent)
DATA_PATH = str(Path(ROOT_PATH) / '.data')
TOTAL_FILES = 400


def create_input_wave_files(n: int, data_path: str = DATA_PATH) -> None:
    """
    Creates sample wave files.
    """
    for i in range(n):
        audio.create_sinewave_file(f'sine_wave{i:04d}.wav', data_path)


def run(
    etl_function: Callable[[str], None],
    cli_help: str = "A CLI to generate and process audio files."
):
    """
    Creates and runs a Typer CLI application with a shared structure.

    Args:
        etl_function: The specific ETL function to run (e.g., single-threaded or multi-threaded).
        cli_help: The help message for the CLI application.
    """
    app = Typer(help=cli_help, add_completion=False)

    @app.callback(invoke_without_command=True)
    def main(
        total_files: int = Option(TOTAL_FILES, "--files", "-n", help="Number of wave files to generate."),
        cleanup: bool = Option(True, "--cleanup/--no-cleanup", help="Cleanup data directory after processing.")
    ):
        fs.prepare_datadir(DATA_PATH)
        create_input_wave_files(total_files, DATA_PATH)
        etl_function(DATA_PATH)
        if cleanup:
            fs.remove_datadir(DATA_PATH)

    app()