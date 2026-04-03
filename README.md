# BCOG-200-Final-Project

# Simon Says Memory Game


## Project Description
This project an interactive Simon Says memeory game that tests working memory and sequential processing abilities. The game displays a sequence of colored buttons that light up in randome pattern, and the player must repeat the sequence by clicking the buttons in the correct order. Each round, the sequence get longer by one step, which make the cognitive challege more difficult. The game tracks performance metrics including the longest sequence acheived, accuracy rate, and recation time, saving all the data to a CSV file.



## Planned Functions

### generate_sequence()
this function will generate a random sequence of colors for each round. It takes the current level as input and returns a list of color names that represents the pattern the player must memorize and repeat

### play_sequence()
This function will visually display the generated sequence to the player by lighting up each button in order with a brief delay between each one.

### check_player_input()
This function will compare the player's button clicks against the correct sequence and determine if the player successfully repeated the pattern. 
