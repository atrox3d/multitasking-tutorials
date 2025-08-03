from pathlib import Path
import sys
import time

# just hack the sys.path to import dame level packages
sys.path.insert(0, str(Path(__file__).resolve()))
from helpers import audio
from helpers import runner

ROOT_PATH = str(Path(__file__).resolve().parent.parent.parent)
DATA_PATH = str(Path(ROOT_PATH) / '.data')
TOTAL_FILES = 400
