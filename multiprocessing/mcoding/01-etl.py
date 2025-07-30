from pathlib import Path
import sys

# just hack the sys.path to import root level packages
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from helpers.audio.sinewave import create_sine_wave

