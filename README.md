# Simon Says Memory Game
 
A terminal-based Simon Says game that tests working memory. The game
generates a random sequence of colors, shows it to the player, and
asks them to repeat it. Each correct round adds one more color to the
sequence. The game ends when the player makes a mistake, and all
performance data is saved to a CSV file.
 
## Why Use This Program
- **Memory training:** Practice short-term memory in a simple,
  repeatable way.
- **Cognitive science experiment:** Collect reaction time and accuracy
  data across rounds for classroom or lab use.
- **Entertainment:** Challenge yourself or friends to beat your
  highest level.
  
## How It Works
1. The program generates a random sequence of colors.
2. The sequence is displayed one color at a time, then hidden.
3. The player types the sequence back from memory.
4. A correct answer advances the game to the next level (longer sequence).
5. A wrong answer ends the game and prints a performance summary.
6. All round data is saved to `data/results.csv`.
   
## Data Output
Results are saved in `data/results.csv` with the following format:
 
```
round,correct,reaction_time
1,1,2.34
2,1,3.01
3,0,4.52
```
 
## Requirements 
- Python 3.8 or higher
- No external packages required (uses only standard library modules:
  `random`, `time`, `csv`, `os`)
  
## How to Run
```bash
python simon_game.py
```
 
## How to Run Tests
```bash
pytest tests/
```
