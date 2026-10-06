from .cost import start_cost, transition_cost, triple_cost

FINGERS = (1, 2, 3, 4, 5)

def suggest_fingering(notes: list[int]) -> list[int]:

   
    if len(notes) == 0:
        return []
    #song w 1 note
    if len(notes) == 1:
        best_f = None
        lowest = float("inf")
        for f in FINGERS:
            if start_cost(notes[0], f) < lowest:
                lowest = start_cost(notes[0], f)
                best_f = f
        return [best_f]

    #finger combinations 
    first = {}
    for a in FINGERS:
        for b in FINGERS:
            first[(a, b)] = start_cost(notes[0], a) + transition_cost(notes[0], a, notes[1], b)

    #holds best possible path taken to note 
    best_path = [None, first]
    parent = [None, {}]

    
    for i in range(2, len(notes)):
        row = {}
        par = {}
        for b in FINGERS:              # note i - 1 finger 
            for c in FINGERS:          # note i finger 
                best_a, best_total = None, float("inf")
                for a in FINGERS:      # note i - 2 finger 
                    total = (best_path[i-1][(a, b)] #best possible path up to a,b 
                             + transition_cost(notes[i-1], b, notes[i], c) 
                             + triple_cost(notes[i-2], a, notes[i-1], b, notes[i], c)) # only penalize for difficult fingerings.
                    if total < best_total:
                        best_a, best_total = a, total #best path for a for b,c
                row[(b, c)] = best_total
                par[(b, c)] = best_a
        best_path.append(row)
        parent.append(par)

    
    best_pair = None
    lowest = float("inf")
    #finds the last two notes with lowest penalty 
    for pair in best_path[-1]:
        if best_path[-1][pair] < lowest:
            lowest = best_path[-1][pair]
            best_pair = pair

    #set fingers 
    b, c = best_pair

    #prep fingering to return 
    fingering = [c,b]

    #go backwards 
    for i in range(len(notes) -1 , 1,-1):
        a = parent[i][(b,c)]
        fingering.append(a)

        #move fingers up 1. 
        b,c = a,b
    fingering.reverse()
    return fingering