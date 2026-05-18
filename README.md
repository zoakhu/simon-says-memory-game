# Simon Says Memory Game

An interactive Simon Says game that tests working memory. Colored pads
flash in a sequence and the player clicks them to repeat the pattern.
Each correct round adds one more color to the sequence. New colors are
unlocked at higher levels, making the game progressively harder.
Performance data is saved to a CSV file after each session.

## Why Use This Program

- **Memory training:** Practice short-term memory in a fun, interactive way.
- **Cognitive science experiment:** Collect reaction time and accuracy
  data across rounds for classroom or lab use.
- **Entertainment:** Challenge yourself or friends to beat your highest level.

## How It Works

1. Enter your name on the start screen.
2. Colored pads flash in a sequence — memorize the order.
3. Click the pads in the same order to repeat the sequence.
4. A correct answer advances the game to the next level (longer sequence).
5. A wrong answer ends the game and displays a performance summary.
6. New colors unlock at levels 5, 8, and 11 to increase difficulty.
7. All round data is saved to `data/results.csv`.

## Data Output

Results are saved in `data/results.csv` with the following format:

```
player,round,correct,reaction_time
Zohra, 1, 1, .47
Zohra, 2, 1, 1.27
Zohra, 3, 0, 1.77

```

## Requirements

- Python 3.8 or higher
- No external packages required (uses only standard library modules:
  `random`, `time`, `csv`, `os`, `tkinter`)

## How to Run

```bash
python3 simon_game.py
```

## How to Run Tests

```bash
pytest tests/
```

