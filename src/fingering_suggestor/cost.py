
FINGER_SPANS = {
    (1, 2): (-7, -5, 1, 3, 8, 10),
    (1, 3): (-6, -4, 3, 6, 10, 12),
    (1, 4): (-4, -2, 5, 8, 11, 13),
    (1, 5): (-2, 0, 7, 10, 12, 14),
    (2, 3): (1, 1, 1, 2, 4, 6),
    (2, 4): (1, 1, 3, 4, 6, 8),
    (2, 5): (2, 2, 5, 6, 8, 10),
    (3, 4): (1, 1, 1, 2, 2, 4),
    (3, 5): (1, 1, 3, 4, 6, 8),
    (4, 5): (1, 1, 1, 2, 4, 6),
}

KEY_POSITIONS = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13]

def new_key_position(pitch: int) -> int: # midi pitch -> key position, 14 per octave
    return (pitch // 12) * 14 + KEY_POSITIONS[pitch % 12]

def is_black(pitch: int) -> bool:
    return pitch % 2 == 0 # takes the new system of key pos 

#cost for the three notes
def triple_cost(prev_prev_note, prev_prev_finger, prev_note, prev_finger, note, finger) -> float:
    first, middle, last = new_key_position(prev_prev_note), new_key_position(prev_note), new_key_position(note)
    
    middle_is_between = min(first, last) < middle < max(first, last) # notes keep going the same direction

    cost = 0.0

    # rule 12: same finger on 1st and 3rd note
    if prev_prev_finger == finger:
        if first != last and middle_is_between: # finger has to jump over the middle note, +3
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

    if span < min_comf or span > max_comf: #large gap 
        cost += 1  # rule 3: hand position change
        cost += abs(span - min_comf if span < min_comf else span - max_comf)  # rule 4: gap between 1st and 3rd note is large
        if prev_finger == 1 and middle_is_between and (span < min_prac or span > max_prac):
            cost += 1  # rule 3: thumb in the middle and big gap 

    # rule 3: 1st and 3rd note same key but different fingers (back and forth), +1
    if first == last:
        cost += 1

    return cost

def span_cost(low_finger: tuple, high_finger: tuple, span: int) -> float:
    low_f, low_pos = low_finger
    high_f, high_pos = high_finger

    low_is_black = is_black(low_pos)
    high_is_black = is_black(high_pos)

    min_prac, min_comf, min_rel, max_rel, max_comf, max_prac = FINGER_SPANS[(low_f, high_f)]

    cost = 0.0

    if low_f == 1 and span < 0: #thumb passing under / finger going over the thumb
        if low_is_black == high_is_black: #cross when same level , +1
            cost += 1
        elif low_is_black: #thumb on black, finger on white and cross
            cost += 2
    if span < min_rel or span > max_rel: # +1 penalty every unit below or above relax.
        cost += abs(span - min_rel if span < min_rel else span - max_rel) 
    if span < min_comf or span > max_comf: # +2 penalty every unit below or above comf
        cost += abs(span - min_comf if span < min_comf else span - max_comf) * 2 
    if span < min_prac or span > max_prac: # +10 every unit above or below practical.
        cost += abs(span - min_prac if span < min_prac else span - max_prac) * 10 
    if low_f == 3 and high_f == 4: # 3 and 4 back to back is weak, +1
        cost += 1.0
        if not low_is_black and high_is_black: # 3 on white, 4 on black, +1 more
            cost += 1.0
    if low_f == 1:
        if low_is_black and not high_is_black: # thumb on black, other finger on white, +1
            cost += 1
    if high_f == 5 and high_is_black:
        if not low_is_black: # pinky on black, other finger on white, +1
            cost += 1
    
    return cost 

def start_cost(note: int, finger: int) -> float: # cost for first finger
    new_note = new_key_position(note)

    if is_black(new_note) and finger == 1: # thumb on black, +0.5
        return 0.5
    if finger == 4: # weak 4th finger, +1
        return 1.0
    return 0.0

# cost from one finger to next 
def transition_cost(prev_note: int, prev_finger: int, note: int, finger: int) -> float:
    cost = 0.0 

    if prev_finger == finger and prev_note != note: # never same finger on two keys in a row. 
        return 500.0
    elif prev_finger == finger: # same key same finger, no cost 
        return 0.0
    elif prev_finger != finger and prev_note == note: # finger switch on the same key, +1
        return 1.0

    new_note, new_prev_note = new_key_position(note), new_key_position(prev_note)

    if is_black(new_note) and finger == 1: # thumb on black, +0.5
        cost += 0.5
    if finger == 4: # weak 4th finger, +1
        cost += 1.0

    # figure out which finger is the higher 
    if prev_finger > finger:
        higher_finger = (prev_finger, new_prev_note)
        lower_finger = (finger, new_note)
        span = new_prev_note - new_note
    else:
        higher_finger = (finger, new_note)
        lower_finger = (prev_finger, new_prev_note)
        span = new_note - new_prev_note 

    cost += span_cost(lower_finger, higher_finger, span) # stretch / crossing cost between the two fingers

    return cost