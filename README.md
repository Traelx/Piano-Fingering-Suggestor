# Fingering Suggestor

A program that suggests fingerings for piano sheet music, currently only limited to the right hand. 

The program requires a MusicXML file as an input. 


## Example


## How it works

### 1. Penalties based on hand position/movement. 

Pianists choose fingerings based on three main things:
**Expressiveness** The ability to properly express the piece using the correct fingers.
**Comfortability** How easy and comfortable the fingerings are for the hand.
**Readability and Memorization** How easy the fingerings are to memorize. 

This program currently attempts to maximize comfortability. By using Parncutt's table for finger spans, we are able to calculate the range of comfortability for the compared two fingers. 

However, a problem occurs when notes E to F or B to C are reached, as despite them having the same distance as any other white to white key, they are measured differently in semitones (What the parncutt table uses.) For example, C to D requires a movement of two semitones, while E to F only requires a movement of one. 

The solution is to add two imaginary keys exactly at those two positions in order to equally space all the white keys. With those two positions added, the octave now has 14 positions.  

Because of this change, we also must scale the Parncutt table by 14/12 in order to get the estimated spans.

Once these spans are found, they are used to calculate the costs for the two fingers for being in that range. 


### 2. Find the cheapest fingering for the whole passage

The program approaches this problem with dynamic programming. Instead of trying all 5ⁿ posible fingerings, the cheapest way to reach a note using a pair of fingers on the last two notes.

The Idea: There are 5^2 = 25 possible ways to finger two notes. 

Let's assume three notes, A, B and C. If we want a finger for C, this program asks for all the 25 possible combinations of B and C. For each of those possible 25 combinations, it then asks, what is the best finger we could've used for A to get to this combination of B and C? For example, if B and C is fingered with 2 and 3 respectively, then A should be fingered with 1 (assuming that the notes are going up) to get the least amount of cost. At the end of the program, the route with the least amount of cost is traced backwards in order to get the fingers. 


When choosing the best finger for A, the program also adds a cost for seeing the three notes A, B and C together. Because this movement (going upwards from finger 1 to 3) is comfortable, the cost is free. 

### 3. Reading the sheet music and writing the fingers in

Uses [music21](https://web.mit.edu/music21/).

- Top staff of a MusicXML file is read only, skips tied notes and rests. 
- writes the suggested fingerings back onto the score as a new MusicXML file.

## Usage

Requires [uv](https://docs.astral.sh/uv/).


```
Sheet file requires a tempo marking to fully work as intended. This is needed because the program attempts to accommodate for time a pianist has to move their fingers by checking the actual seconds that has passed between each note. 
```
git clone https://github.com/Traelx/Fingering-Suggestor.git
cd Fingering-Suggestor
uv run fingering-suggestor test_songs/sonata.mxl
```

## Project structure

```
src/fingering_suggestor/
    __init__.py       
    music_import.py   
    dp.py             
    cost.py           
```

## Limitations



## Next steps


## References

- Parncutt, R., Sloboda, J. A., Clarke, E. F., Raekallio, M., & Desain, P. (1997). An ergonomic model of keyboard fingering for melodic fragments. *Music Perception*, 14(4), 341–382.
- Jacobs, J. P. (2001). Refinements to the ergonomic model for keyboard fingering of Parncutt, Sloboda, Clarke, Raekallio, and Desain. *Music Perception*, 18(4), 505–511.
