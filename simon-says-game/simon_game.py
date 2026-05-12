"""
Simon Says Memory Game
A terminal-based working memory experiment that generates color
sequences for the player to repeat. The color pool expands every
few levels, making the game progressively harder. Performance data
is saved to data/results.csv after each game session.
"""

import csv
import os
import random
import time
import tkinter as tk
 
# All possible colors, unlocked progressively as levels increase.
ALL_COLORS = ["red", "blue", "green", "yellow", "purple", "orange", "white"]
 
# Darker versions of each color shown when the button is "off"
# Dictionary maps color name -> dim hex code 
DIM_COLORS = {
    "red":    "#5a0000",
    "blue":   "#00005a",
    "green":  "#005a00",
    "yellow": "#5a5a00",
    "purple": "#3a005a",
    "orange": "#5a2d00",
    "white":  "#aaaaaa",
}
 
# Level thresholds at which a new color is unlocked 
COLOR_UNLOCK_LEVELS = {
    5:  "purple",
    8:  "orange",
    11: "white",
}
 
 
def get_active_colors(level: int) -> list:
    """
    Return the list of colors available at the given level.
 
    Starts with the first 4 colors. A new color is added each time
    the player reaches a threshold in COLOR_UNLOCK_LEVELS.
 
    Parameters
    ----------
    level : int
        The current game level.
 
    Returns
    -------
    list
        Colors available for sequence generation at this level.
    """
    # Start with the base 4 colors
    active = ALL_COLORS[:4].copy()
 
    # Add unlocked colors if their threshold has been reached 
    for unlock_level, color in COLOR_UNLOCK_LEVELS.items():
        if level >= unlock_level:
            active.append(color)
 
    return active
 
 
def generate_sequence(level: int, active_colors: list) -> list:
    """
    Generate a random color sequence for the current level.
 
    Parameters
    ----------
    level : int
        Determines the length of the sequence.
    active_colors : list
        The pool of colors to draw from.
 
    Returns
    -------
    list
        A list of color name strings of length `level`.
    """
    # List comprehension to build the sequence 
    return [random.choice(active_colors) for _ in range(level)]
 
 
def check_player_input(sequence: list, user_input: list) -> bool:
    """
    Check whether the player's clicks match the correct sequence.
 
    Parameters
    ----------
    sequence : list
        The correct color sequence.
    user_input : list
        The colors the player clicked in order.
 
    Returns
    -------
    bool
        True if the sequences match exactly, False otherwise.
    """
    return sequence == user_input
 
 
def display_results_summary(results: list) -> None:
    """
    Print a performance summary to the terminal after the game ends.
 
    Parameters
    ----------
    results : list
        A list of [round, correct, reaction_time] rows.
    """
    if not results:
        print("No rounds played.")
        return
 
    highest_level = len(results)
 
    # List comprehensions to filter and extract values (Ch. 2.0)
    correct_rounds = [row for row in results if row[1] == 1]
    num_correct = len(correct_rounds)
 
    reaction_times = [row[2] for row in results]
    avg_rt = sum(reaction_times) / len(reaction_times)
 
    print("\n--- Game Over! Here are your results ---")
    print(f"  Highest level reached : {highest_level}")
    print(f"  Correct rounds        : {num_correct} / {highest_level}")
    print(f"  Average reaction time : {avg_rt:.2f} seconds")
 
 
def save_data(results: list) -> None:
    """
    Save round-by-round results to data/results.csv.
 
    Parameters
    ----------
    results : list
        A list of [round, correct, reaction_time] rows to write.
    """
    # Create the data/ folder if it doesn't exist (os module, Ch. 5.0)
    os.makedirs("data", exist_ok=True)
 
    # File I/O with 'with' for automatic closing 
    with open("data/results.csv", "w", newline="") as file_handle:
        writer = csv.writer(file_handle)
        writer.writerow(["round", "correct", "reaction_time"])
        writer.writerows(results)
 
 
def run_game() -> None:
    """
    Build and run the tkinter Simon Says GUI.
 
    Creates a window with colored buttons. The game flashes the
    sequence, then waits for the player to click the buttons in
    order. Uses tkinter from Ch. 11 of course notes.
    """
    # ── Game state variables ──────────────────────────────────────
    level = 1
    results = []
    sequence = []
    player_clicks = []
    start_time = 0.0
    accepting_input = False  # guard: ignore clicks during playback
 
    # ── Build the window ─────────────────────────────────────────
    window = tk.Tk()
    window.title("Simon Says")
    window.configure(bg="black")
 
    # Status label shown at the top (Ch. 11.3)
    status_label = tk.Label(
        window,
        text="Press Start to play!",
        font="Helvetica 18 bold",
        bg="black",
        fg="white",
    )
    status_label.pack(pady=10)
 
    # Frame to hold the color buttons (Ch. 11.1)
    button_frame = tk.Frame(window, bg="black")
    button_frame.pack(pady=10)
 
    # Dictionary to store button widgets keyed by color name 
    buttons = {}
 
    def flash_button(color: str) -> None:
        """
        Briefly light up a button to show it as part of the sequence.
 
        Parameters
        ----------
        color : str
            The color name of the button to flash.
        """
        # Set button to its bright color
        buttons[color].configure(bg=color)
        # Schedule it to go dim again after 500 ms (Ch. 11.4 .after())
        window.after(500, lambda: buttons[color].configure(bg=DIM_COLORS[color]))
 
    def on_button_click(color: str) -> None:
        """
        Handle a player clicking a color button.
 
        Records the click, flashes the button, and checks whether
        the player has completed their response for this round.
 
        Parameters
        ----------
        color : str
            The color name of the button that was clicked.
        """
        nonlocal accepting_input, start_time
 
        # Ignore clicks during sequence playback
        if not accepting_input:
            return
 
        flash_button(color)
        player_clicks.append(color)
 
        # Check after every click if the answer is already wrong
        click_index = len(player_clicks) - 1
        if player_clicks[click_index] != sequence[click_index]:
            # Wrong click — end the round immediately
            accepting_input = False
            reaction_time = round(time.time() - start_time, 2)
            results.append([level, 0, reaction_time])
            status_label.configure(
                text=f"Wrong! Sequence was: {' '.join(sequence)}"
            )
            # Show summary then close after 3 seconds
            window.after(3000, end_game)
            return
 
        # If the player has clicked the full sequence correctly
        if len(player_clicks) == len(sequence):
            accepting_input = False
            reaction_time = round(time.time() - start_time, 2)
            results.append([level, 1, reaction_time])
            status_label.configure(text="Correct! Get ready...")
            # Wait 1 second then start the next round
            window.after(1000, next_round)
 
    def build_buttons(active_colors: list) -> None:
        """
        Create or recreate color buttons for the current active set.
 
        Destroys old buttons and builds new ones so the layout always
        matches the current active color pool.
 
        Parameters
        ----------
        active_colors : list
            The colors to show buttons for this level.
        """
        # Remove any existing buttons (Ch. 11.3)
        for widget in button_frame.winfo_children():
            widget.destroy()
        buttons.clear()
 
        # Build one button per active color using a loop (Ch. 2.0)
        for i, color in enumerate(active_colors):
            btn = tk.Button(
                button_frame,
                bg=DIM_COLORS[color],
                width=6,
                height=3,
                command=lambda c=color: on_button_click(c),
            )
            # Arrange in rows of 4 using grid (Ch. 11.2)
            btn.grid(row=i // 4, column=i % 4, padx=8, pady=8)
            buttons[color] = btn
 
    def play_sequence_gui(seq: list, index: int = 0) -> None:
        """
        Flash each color in the sequence one at a time using .after().
 
        Recursively schedules the next flash until the sequence is
        done, then enables player input.
 
        Parameters
        ----------
        seq : list
            The full color sequence to play.
        index : int
            The current position in the sequence being flashed.
        """
        nonlocal accepting_input, start_time
 
        if index < len(seq):
            flash_button(seq[index])
            # Schedule the next flash 900 ms later (Ch. 11.4)
            window.after(900, lambda: play_sequence_gui(seq, index + 1))
        else:
            # Sequence finished — enable player clicks
            accepting_input = True
            start_time = time.time()
            status_label.configure(text="Your turn! Click the sequence.")
 
    def next_round() -> None:
        """
        Advance to the next level and start a new round.
 
        Updates the button layout if a new color was just unlocked,
        generates a new sequence, and plays it for the player.
        """
        nonlocal level, sequence
        level += 1
        start_new_round()
 
    def start_new_round() -> None:
        """
        Set up and begin a fresh round at the current level.
 
        Clears previous clicks, rebuilds buttons if needed, announces
        any newly unlocked color, and plays the new sequence.
        """
        nonlocal sequence
        player_clicks.clear()
 
        active_colors = get_active_colors(level)
        build_buttons(active_colors)
 
        # Announce a new color if this level unlocks one (Ch. 1.7)
        if level in COLOR_UNLOCK_LEVELS:
            new_color = COLOR_UNLOCK_LEVELS[level]
            status_label.configure(
                text=f"Level {level}: '{new_color}' added! Watch..."
            )
        else:
            status_label.configure(
                text=f"Level {level} — Watch the sequence..."
            )
 
        sequence = generate_sequence(level, active_colors)
 
        # Short delay before flashing so the label is readable
        window.after(1200, lambda: play_sequence_gui(sequence))
 
    def end_game() -> None:
        """Print results summary, save data, and close the window."""
        display_results_summary(results)
        save_data(results)
        print("\nData saved to data/results.csv")
        window.destroy()
 
    def start_game() -> None:
        """
        Begin the game from level 1 when the Start button is pressed.
 
        Hides the Start button and kicks off the first round.
        """
        start_btn.pack_forget()
        start_new_round()
 
    # ── Start button and quit button ─────────────────────────────
    start_btn = tk.Button(
        window,
        text="Start Game",
        font="Helvetica 14 bold",
        command=start_game,
    )
    start_btn.pack(pady=5)
 
    quit_btn = tk.Button(
        window,
        text="Quit",
        font="Helvetica 12",
        command=end_game,
    )
    quit_btn.pack(pady=5)
 
    # Build the initial button layout before the game starts
    build_buttons(get_active_colors(level))
 
    # Start the tkinter event loop 
    window.mainloop()
 
 
def main() -> None:
    """Entry point: start the Simon Says GUI."""
    run_game()
 
 
if __name__ == "__main__":
    main()
 
