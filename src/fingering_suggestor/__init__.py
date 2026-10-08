from .dp import suggest_fingering
from .music_import import fingering_to_mxml
import sys

def main() -> None:
    if (len(sys.argv) < 2):
        print("Please choose mxl file. Usage: fingering-suggestor <SONGNAME.mxl> ")
        return
    fingering_to_mxml(sys.argv[1])
