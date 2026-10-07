from music21 import converter, articulations, note, chord
from pathlib import Path
from .dp import suggest_fingering 

PROJECT_ROOT = Path(__file__).parents[2]

song = "sonata.mxl"
sheet = converter.parse(PROJECT_ROOT / "test_songs" / song)


right_hand = sheet.parts[0]

score = []

pitches = []
melody_notes = []
free_time = []

prev_end = None # time when last note ended 

for item in right_hand.flatten().secondsMap:
    n = item["element"]

    if not isinstance(n,(note.Note, chord.Chord)):
        continue
    if n.tie and n.tie.type in ("stop", "continue"):
        continue
    if n.isNote:
        pitch = n.pitch.midi
    else:
        pitch = max(p.midi for p in n.pitches) #place holder, highest pitch is usually melody note. 
    
    if prev_end is None: #first note edge
        free_time.append(0.0)                              
    else:
        free_time.append(item["offsetSeconds"] - prev_end) 

    pitches.append(pitch)
    melody_notes.append(n)
    prev_end = item["offsetSeconds"]

split = []
for i, pitch in enumerate(pitches):
    if free_time[i] > 1:   # gap before this note → start a new chunk
        score.append(split)
        split = []
    split.append(pitch)
score.append(split)


fingering = []

for notes in score:
    fingering += suggest_fingering(notes)

for n, f in zip(melody_notes, fingering):
    if n.isNote:
        n.articulations.append(articulations.Fingering(f))

out_path = PROJECT_ROOT / "test_songs" / (Path(song).stem + "_fingering.musicxml")
sheet.write("musicxml", fp=out_path, makeNotation=False)



    