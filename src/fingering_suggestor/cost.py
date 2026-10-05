BLACK_KEYS = {1, 3, 6, 8, 10}  # pitch classes of the black keys (C# D# F# G# A#)

#Parncutt et al 1997 Small hands
# (min_prac, min_comf, min_rel, max_rel, max_comf, max_prac), in semitones
FINGER_SPANS = {
    (1,2): (-7, -5, 1, 3, 8, 10),
    (1,3): (-6, -4, 3, 6, 10, 12),
    (1,4): (-4, -2, 5, 8, 11, 13),
    (1,5): (-2, 0, 7, 10, 12, 14),
    (2,3): (1, 1, 1, 2, 4, 6),
    (2,4): (1, 1, 3, 4, 6, 8),
    (2,5): (2, 2, 5, 6, 8, 10),
    (3,4): (1, 1, 1, 2, 2, 4),
    (3,5): (1, 1, 3, 4, 6, 8),
    (4,5): (1, 1, 1, 2, 4, 6),
    
}

KEY_POSITIONS = [1,2,3,4,5,7,8,9,10,11,12,13]

def is_black(pitch: int) -> bool:
    return pitch % 12 in BLACK_KEYS

def new_key_position(pitch: int) -> int:
    return (pitch//12) * 14 + KEY_POSITIONS[pitch%12]  

def span_cost(low_finger: int, high_finger: int, span: int) -> float:

    min_prac,min_comf,min_rel,max_rel,max_comf,max_prac = FINGER_SPANS[(low_finger,high_finger)]

    cost = 0.0

    if span < min_rel or span > max_rel:
        cost += abs(span - min_rel if span < min_rel else span - max_rel) 
    if span < min_comf or span > max_comf:
        cost += abs(span - min_comf if span < min_comf else span - max_comf) * 2 

    return cost 
    



def start_cost(note: int, finger: int) -> float: #cost for first finger 

    return 0.0

#cost from one finger to next 
def transition_cost(prev_note: int, prev_finger: int, note: int, finger: int) -> float:
    if prev_finger == finger:
        return 500.0
    
    new_note, new_prev_note = new_key_position(note), new_key_position(prev_note)
    
    if prev_finger > finger:
        higher_finger = prev_finger
        lower_finger = finger
        span = new_prev_note - new_note
    else:
        higher_finger = finger
        lower_finger = prev_finger
        span = new_note - new_prev_note 

    return span_cost(lower_finger,higher_finger,span)


