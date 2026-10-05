from collections.abc import Callable

from .cost import start_cost, transition_cost

FINGERS = (1, 2, 3, 4, 5)

def suggest_fingering(notes: list[int], cost_fn = transition_cost) -> list[int]:
    if not notes:
        return []

    best_path = [{f: start_cost(notes[0],f) for f in FINGERS}] # start edgecase 
    parent = [{}]

    for i in range(1, len(notes)):
        prev_note, current_note = notes[i-1], notes[i]
        row = {} #best path
        par = {} #parent
        for f in FINGERS:
            best_previous_finger, best_total_cost = None, float("inf")
            for previous_finger in FINGERS:
                total_cost = best_path[i-1][previous_finger] + cost_fn(prev_note, previous_finger, current_note, f)
                if total_cost < best_total_cost:
                    best_previous_finger, best_total_cost = previous_finger, total_cost
                row[f] = best_total_cost
                par[f] = best_previous_finger
        best_path.append(row)
        parent.append(par)
            
    f = None
    lowest_path = float("inf")

    for finger in FINGERS:
        if best_path[-1][finger] < lowest_path:
            lowest_path = best_path[-1][finger]
            f = finger
        
    fingering = [f]
    for i in range(len(notes) - 1, 0, -1): #go back to get all the fingers
        f = parent[i][f]
        fingering.append(f)
    fingering.reverse() #put in correct order. 
    return fingering
