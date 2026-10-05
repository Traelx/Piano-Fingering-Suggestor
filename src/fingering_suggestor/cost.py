BLACK_KEYS = {1, 3, 6, 8, 10}  # pitch classes of the black keys (C# D# F# G# A#)


def is_black(pitch: int) -> bool:
    return pitch % 12 in BLACK_KEYS


def start_cost(note: int, finger: int) -> float: #cost for first finger 
    
    return 0.0

#cost from one finger to next 
def transition_cost(prev_note: int, prev_finger: int, note: int, finger: int) -> float:

    return 0.0
