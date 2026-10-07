# Parncutt et al 1997 small hands, converted to key positions (x 14/12, rounded)
# (3, 4) max_comf raised 2 -> 3 so E-F# (3 key positions) is comfortable for fingers 3-4
# (min_prac, min_comf, min_rel, max_rel, max_comf, max_prac), in key positions
FINGER_SPANS = {
    (1, 2): (-8, -6, 1, 4, 9, 12),
    (1, 3): (-7, -5, 4, 7, 12, 14),
    (1, 4): (-5, -2, 6, 9, 13, 15),
    (1, 5): (-2, 0, 8, 12, 14, 16),
    (2, 3): (1, 1, 1, 2, 5, 7),
    (2, 4): (1, 1, 4, 5, 7, 9),
    (2, 5): (2, 2, 6, 7, 9, 12),
    (3, 4): (1, 1, 1, 2, 3, 5),
    (3, 5): (1, 1, 4, 5, 7, 9),
    (4, 5): (1, 1, 1, 2, 5, 7),
}


# FINGER_SPANS = {
#     (1, 2): (-7, -5, 1, 3, 8, 10),
#     (1, 3): (-6, -4, 3, 6, 10, 12),
#     (1, 4): (-4, -2, 5, 8, 11, 13),
#     (1, 5): (-2, 0, 7, 10, 12, 14),
#     (2, 3): (1, 1, 1, 2, 4, 6),
#     (2, 4): (1, 1, 3, 4, 6, 8),
#     (2, 5): (2, 2, 5, 6, 8, 10),
#     (3, 4): (1, 1, 1, 2, 2, 4),
#     (3, 5): (1, 1, 3, 4, 6, 8),
#     (4, 5): (1, 1, 1, 2, 4, 6),
# }

KEY_POSITIONS = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13]

def new_key_position(pitch: int) -> int:
    return (pitch // 12) * 14 + KEY_POSITIONS[pitch % 12]  

def is_black(pitch: int) -> bool:
    return pitch % 2 == 0 # takes the new system of key pos 

#cost for the three notes appearing 
def triple_cost(prev_prev_note, prev_prev_finger, prev_note, prev_finger, note, finger) -> float:
    first, middle, last = new_key_position(prev_prev_note), new_key_position(prev_note), new_key_position(note)
    middle_is_between = min(first, last) < middle < max(first, last)

    cost = 0.0

    # rule 12
    if prev_prev_finger == finger:
        if first != last and middle_is_between:
            cost += 3
        # same finger on a different key = the hand moved
        if first != last:
            cost += 1 + abs(last - first) * 0.5
        return cost

    # distance between 1st and 3rd note
    if prev_prev_finger < finger:
        span = last - first
    else:
        span = first - last

    min_prac, min_comf, min_rel, max_rel, max_comf, max_prac = FINGER_SPANS[(min(prev_prev_finger, finger), max(prev_prev_finger, finger))]

    if span < min_comf or span > max_comf:
        cost += 1  # rule 3: hand position change
        cost += abs(span - min_comf if span < min_comf else span - max_comf)  # rule 4: size of the change
        if prev_finger == 1 and middle_is_between and (span < min_prac or span > max_prac):
            cost += 1  # rule 3: thumb in the middle and a very big change

    # rule 3
    if first == last:
        cost += 1

    return cost

def span_cost(low_finger: tuple, high_finger: tuple, span: int) -> float:
    low_f, low_pos = low_finger
    high_f, high_pos = high_finger

    min_prac, min_comf, min_rel, max_rel, max_comf, max_prac = FINGER_SPANS[(low_f, high_f)]

    cost = 0.0

    if low_f == 1 and span < 0:
        if is_black(low_pos) == is_black(high_pos):
            cost += 1
        elif is_black(low_pos):
            cost += 2
    if span < min_rel or span > max_rel:
        cost += abs(span - min_rel if span < min_rel else span - max_rel) 
    if span < min_comf or span > max_comf:
        cost += abs(span - min_comf if span < min_comf else span - max_comf) * 2 
    if span < min_prac or span > max_prac:
        cost += abs(span - min_prac if span < min_prac else span - max_prac) * 10 
    if low_f == 3 and high_f == 4:
        cost += 1.0
        if not is_black(low_pos) and is_black(high_pos):
            cost += 1.0
    if low_f == 1:
        if is_black(low_pos) and not is_black(high_pos):
            cost += 1
    if high_f == 5 and is_black(high_pos):
        if not is_black(low_pos):
            cost += 1
    
    return cost 

def start_cost(note: int, finger: int) -> float: # cost for first finger
    new_note = new_key_position(note)

    if is_black(new_note) and finger == 1:
        return 0.5
    if finger == 4:
        return 1.0
    return 0.0

# cost from one finger to next 
def transition_cost(prev_note: int, prev_finger: int, note: int, finger: int) -> float:
    cost = 0.0 

    if prev_finger == finger and prev_note != note:
        return 500.0
    elif prev_finger == finger:
        return 0.0 
    elif prev_finger != finger and prev_note == note:
        return 1.0
    
    new_note, new_prev_note = new_key_position(note), new_key_position(prev_note)

    if is_black(new_note) and finger == 1:
        cost += 0.5
    if finger == 4:
        cost += 1.0

    if prev_finger > finger:
        higher_finger = (prev_finger, new_prev_note)
        lower_finger = (finger, new_note)
        span = new_prev_note - new_note
    else:
        higher_finger = (finger, new_note)
        lower_finger = (prev_finger, new_prev_note)
        span = new_note - new_prev_note 

    cost += span_cost(lower_finger, higher_finger, span)

    return cost