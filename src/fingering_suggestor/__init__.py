from .dp import suggest_fingering
from . import music_import
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def note_name(pitch: int) -> str:
    return f"{NOTE_NAMES[pitch % 12]}{pitch // 12 - 1}"


def main() -> None:
    notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C major scale
    fingering = suggest_fingering(notes)
    print(" ".join(f"{note_name(n)}:{f}" for n, f in zip(notes, fingering)))
