from music21 import converter, articulations, note, chord
from pathlib import Path
from .dp import suggest_fingering 


def fingering_to_mxml(filename: str):
    path = Path(filename)
    sheet = converter.parse(path)

    right_hand = sheet.parts[0] #top staff

    score, pitches, melody_notes, free_time = [], [], [], []
    prev_start = None # time when last note started

    for item in right_hand.flatten().secondsMap:
        n = item["element"]

        if not isinstance(n,(note.Note, chord.Chord)): #only notes and chords 
            continue
        if n.tie and n.tie.type in ("stop", "continue"): #don't count ties 
            continue

        if n.isNote:
            pitch = n.pitch.midi
        else:
            pitch = max(p.midi for p in n.pitches)

        if prev_start is None: #first note edge
            free_time.append(0.0)                              
        else:
            free_time.append(item["offsetSeconds"] - prev_start) 

        pitches.append(pitch)
        melody_notes.append(n)
        prev_start = item["offsetSeconds"]

    split = []

    #attempts to account for hand pos
    for i, pitch in enumerate(pitches):
        if free_time[i] > 1:  
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

    out_path = path.with_name(path.stem + "_fingering.musicxml")
    sheet.write("musicxml", fp=out_path, makeNotation=False)



    