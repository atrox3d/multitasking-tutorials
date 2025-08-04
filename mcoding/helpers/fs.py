from pathlib import Path
import shutil


def remove_datadir(data_path:str) -> None:
    '''
    remove data directory
    '''
    path = Path(data_path)
    if path.exists():
        print(f"Removing '{path}'...")
        shutil.rmtree(path)
        print(f"Successfully removed '{path}'")


def prepare_datadir(data_path:str) -> None:
    '''
    recreate data directory
    '''
    path = Path(data_path)
    remove_datadir(data_path)
    print(f"Creating '{path}'...")
    path.mkdir(exist_ok=True)
    assert path.exists()


def rename_filepath(filepath:str, name_suffix:str = '-transformed') -> str:
    '''
    add suffix to filename keeping path and extension
    '''
    return str(Path(filepath).with_stem(
        Path(filepath).stem + name_suffix
    ))
