from music21 import converter
from pathlib import Path
from .dp import suggest_fingering 

PROJECT_ROOT = Path(__file__).parents[2]
score = converter.parse(PROJECT_ROOT / "test_songs" / "rubia.mxl")


right_hand = score.parts[0]

score = []

for n in right_hand.recurse().notes:
    if n.isNote:
       score.append(n.pitch.midi)

print(suggest_fingering(score))


    