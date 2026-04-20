
# Simon Says Memory Game


## Project Description
This project an interactive Simon Says memeory game that tests working memory. The game displays a sequence of colored buttons that light up in randome pattern, and the player must repeat the sequence by clicking the buttons in the correct order. Each round, the sequence get faster and longer by one step, which make the game more difficult. The game tracks performance metrics including the longest sequence acheived, accuracy rate, and reaction time, saving all the data to a CSV file.

## Why Use This Program
- Memory Training: Practice and improve short-term memory in a fun, interactive way.
- Classroom / Lab Experiment: Track participant performance across multiple rounds for cognitive psychology studies.
- Entertainment: Challenge yourself or friends to see how long you can follow the color sequences.

## How it works
- The program generates a random sequence of colors
- The sequence is shown to the user
- The user types the sequence
- The program checks if it is correct
- The game continues until the user makes a mistake


## Planned Functions

### generate_sequence()
this function will generate a random sequence of colors for each round. It takes the current level as input and returns a list of color names that represents the pattern the player must memorize and repeat

### play_sequence()
This function will visually display the generated sequence to the player by lighting up each button in order with a brief delay between each one.

### check_player_input()
This function will compare the player's button clicks against the correct sequence and determine if the player successfully repeated the pattern. 


## Data Output

The program saves results in:
data/results.csv

Format:
round,correct,reaction_time

Example:
1,1,1.2  
2,1,1.5  
3,0,2.0  

