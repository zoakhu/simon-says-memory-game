"""
Simon Says Memory Game
A tkinter-based working memory experiment. Colored canvas pads flash
in sequence and the player clicks them to repeat the pattern. The
color pool expands at level thresholds, making the game progressively
harder. Performance data is saved to data/results.csv after each
session.
"""
 
import csv
import os
import random
import time
import tkinter as tk
 
# All possible colors, unlocked progressively as levels increase.
ALL_COLORS = ["red", "blue", "green", "yellow", "purple", "orange", "white"]
 
# Darker versions shown when a pad is "off"
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
 
# Size of each color pad in pixels
PAD_SIZE = 100
 
 
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
 
 
def display_results_summary(player_name: str, results: list) -> None:
    """
    Print a performance summary to the terminal after the game ends.
    Parameters
    ----------
    player_name : str
        The name entered by the player at the start.
    results : list
        A list of [round, correct, reaction_time] rows.
    """
    if not results:
        print("No rounds played.")
        return
 
    highest_level = len(results)
 
    # List comprehensions to filter and extract values
    correct_rounds = [row for row in results if row[1] == 1]
    num_correct = len(correct_rounds)
 
    reaction_times = [row[2] for row in results]
    avg_rt = sum(reaction_times) / len(reaction_times)
 
    print(f"\n--- Game Over! Results for {player_name} ---")
    print(f"  Highest level reached : {highest_level}")
    print(f"  Correct rounds        : {num_correct} / {highest_level}")
    print(f"  Average reaction time : {avg_rt:.2f} seconds")
 
 
def save_data(player_name: str, results: list) -> None:
    """
    Save round-by-round results to data/results.csv.
    Appends to the file if it already exists so multiple players
    accumulate in one place. Includes player name in every row.
    Parameters
    ----------
    player_name : str
        The name entered by the player at the start.
    results : list
        A list of [round, correct, reaction_time] rows to write.
    """
    # Create the data/ folder if it doesn't exist (os module)
    os.makedirs("data", exist_ok=True)
 
    file_path = "data/results.csv"
 
    # Check if file exists to decide whether to write the header
    file_exists = os.path.isfile(file_path)
 
    # Open in append mode so multiple players don't overwrite each other
    with open(file_path, "a", newline="") as file_handle:
        writer = csv.writer(file_handle)
 
        # Only write the header if this is a brand new file
        if not file_exists:
            writer.writerow(["player", "round", "correct", "reaction_time"])
 
        # Add player name to every row
        for row in results:
            writer.writerow([player_name] + row)
 
 
def run_game() -> None:
    """
    Build and run the tkinter Simon Says GUI.
    Uses a canvas to draw colored pads so colors render correctly
    on Mac. Flashes each pad in sequence then waits for the player
    to click them in order. Uses tkinter from Ch. 11 of course notes.
    """
    # ── Game state ────────────────────────────────────────────────
    level = 1
    results = []
    sequence = []
    player_clicks = []
    start_time = 0.0
    accepting_input = False
    player_name = ""
 
    # ── Window setup ─────────────────────────────────────────────
    window = tk.Tk()
    window.title("Simon Says")
    window.configure(bg="black")
    window.resizable(False, False)
 
    # ── Name entry screen ─────────────────────────────────────────
    name_frame = tk.Frame(window, bg="black")
    name_frame.pack(pady=40, padx=40)
 
    tk.Label(
        name_frame,
        text="Simon Says",
        font="Helvetica 28 bold",
        bg="black",
        fg="white",
    ).pack(pady=(0, 4))
 
    tk.Label(
        name_frame,
        text="A working memory game",
        font="Helvetica 13",
        bg="black",
        fg="#aaaaaa",
    ).pack(pady=(0, 24))
 
    tk.Label(
        name_frame,
        text="Enter your name to begin:",
        font="Helvetica 14",
        bg="black",
        fg="white",
    ).pack()
 
    # Entry widget for the player's name
    name_entry = tk.Entry(
        name_frame,
        font="Helvetica 14",
        width=20,
        justify=tk.CENTER,
    )
    name_entry.pack(pady=8)
    name_entry.focus()
 
    # Error label shown if player submits an empty name
    name_error_label = tk.Label(
        name_frame,
        text="",
        font="Helvetica 11",
        bg="black",
        fg="#ff4444",
    )
    name_error_label.pack()
 
    def submit_name() -> None:
        """
        Validate the name entry and transition to the game screen.
        Shows an error if the field is empty, otherwise stores the
        name and builds the game UI.
        """
        nonlocal player_name
 
        # .strip() removes accidental leading/trailing spaces
        entered = name_entry.get().strip()
 
        if not entered:
            name_error_label.configure(text="Please enter a name first.")
            return
 
        player_name = entered
        name_frame.destroy()
        build_game_ui()
 
    # Allow pressing Enter to submit the name
    name_entry.bind("<Return>", lambda event: submit_name())
 
    tk.Button(
        name_frame,
        text="Start",
        font="Helvetica 13 bold",
        command=submit_name,
    ).pack(pady=8)
 
    # ── Game UI (built after name is submitted) ───────────────────
    def build_game_ui() -> None:
        """Build all game widgets after the player submits their name."""
        nonlocal sequence, accepting_input, start_time
 
        # Greeting with the player's name
        tk.Label(
            window,
            text=f"Welcome, {player_name}!",
            font="Helvetica 15 bold",
            bg="black",
            fg="#aaffaa",
        ).pack(pady=(10, 0))
 
        # Status label at the top
        status_label = tk.Label(
            window,
            text="Press Start to play!",
            font="Helvetica 18 bold",
            bg="black",
            fg="white",
            wraplength=420,
        )
        status_label.pack(pady=12)
 
        # Canvas for drawing the color pads
        canvas = tk.Canvas(window, bg="black", highlightthickness=0)
        canvas.pack(pady=10)
 
        # Results label shown at game over — empty until needed
        results_label = tk.Label(
            window,
            text="",
            font="Helvetica 13",
            bg="black",
            fg="white",
            justify=tk.LEFT,
        )
        results_label.pack(pady=4)
 
        pad_ids = {}
 
        def build_pads(active_colors: list) -> None:
            """
            Draw one colored rectangle per active color onto the canvas.
            Arranges pads in rows of 4. Clears old pads first so the
            layout always matches the current color pool.
            Parameters
            ----------
            active_colors : list
                Colors to draw pads for at this level.
            """
            canvas.delete("all")
            pad_ids.clear()
 
            cols = 4
            pad_gap = 10
            num_colors = len(active_colors)
            num_rows = (num_colors + cols - 1) // cols  # ceiling division
 
            # Resize the canvas to fit the pads
            canvas_w = cols * PAD_SIZE + (cols + 1) * pad_gap
            canvas_h = num_rows * PAD_SIZE + (num_rows + 1) * pad_gap
            canvas.configure(width=canvas_w, height=canvas_h)
 
            # Draw each pad as a filled rectangle — all start dim
            # to prevent any flicker between rounds, from peer reviewer2
            for i, color in enumerate(active_colors):
                row = i // cols
                col = i % cols
                x1 = pad_gap + col * (PAD_SIZE + pad_gap)
                y1 = pad_gap + row * (PAD_SIZE + pad_gap)
                x2 = x1 + PAD_SIZE
                y2 = y1 + PAD_SIZE
 
                # Draw dim rectangle and store its id
                rect_id = canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=DIM_COLORS[color],
                    outline="white",
                    width=2,
                    tags=color,   # tag lets us find it by color name
                )
                pad_ids[color] = rect_id
 
            # Force full redraw before any flashing begins
            window.update()
            canvas.bind("<Button-1>", on_canvas_click)
 
        def flash_pad(color: str) -> None:
            """
            Briefly light up a pad to its bright color then dim it.

            """
            # Set to bright color and force redraw
            canvas.itemconfig(pad_ids[color], fill=color)
            window.update()
            window.after(
                600,
                lambda: canvas.itemconfig(
                    pad_ids[color], fill=DIM_COLORS[color]
                )
            )
 
        def on_canvas_click(event: tk.Event) -> None:
            """
            Detect which pad the player clicked based on canvas coordinates.
            """
            nonlocal accepting_input, start_time
 
            if not accepting_input:
                return
 
            # Find which rectangle was clicked using canvas.find_overlapping
            clicked = canvas.find_overlapping(
                event.x, event.y, event.x, event.y
            )
            if not clicked:
                return
 
            # Match the clicked rectangle id to a color name
            clicked_color = None
            for color, rect_id in pad_ids.items():
                if rect_id in clicked:
                    clicked_color = color
                    break
 
            if clicked_color is None:
                return
 
            flash_pad(clicked_color)
            player_clicks.append(clicked_color)
 
            # Check immediately if the latest click is wrong
            click_index = len(player_clicks) - 1
            if player_clicks[click_index] != sequence[click_index]:
                accepting_input = False
                reaction_time = round(time.time() - start_time, 2)
                results.append([level, 0, reaction_time])
                status_label.configure(
                    text=f"Wrong! The sequence was: {' '.join(sequence)}"
                )
                # Show results in window instead of closing immediately
                window.after(1500, show_results_screen)
                return
 
            # Check if the full sequence was completed correctly
            if len(player_clicks) == len(sequence):
                accepting_input = False
                reaction_time = round(time.time() - start_time, 2)
                results.append([level, 1, reaction_time])
                status_label.configure(text = "Correct! Get ready...")
                window.after(1000, next_round)
 
        def play_sequence_gui(seq: list, index: int = 0) -> None:
            """
            Flash each pad in the sequence one at a time using .after().
            Schedules the next flash recursively until done, then enables
            player input.
            """
            nonlocal accepting_input, start_time
 
            if index < len(seq):
                flash_pad(seq[index])
                # Schedule next flash 900 ms later
                window.after(900, lambda: play_sequence_gui(seq, index + 1))
            else:
                # Done — enable player input
                accepting_input = True
                start_time = time.time()
                status_label.configure(text="Your turn! Click the sequence.")
 
        def start_new_round() -> None:
            """
            Set up and begin a fresh round at the current level.
            Clears previous clicks, rebuilds pads, announces any newly
            unlocked color, and plays the new sequence.
            """
            nonlocal sequence
            player_clicks.clear()
 
            active_colors = get_active_colors(level)
            build_pads(active_colors)
 
            # Announce a new color if this level unlocks one
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
            window.after(1200, lambda: play_sequence_gui(sequence))
 
        def next_round() -> None:
            """Advance level by one and start a new round."""
            nonlocal level
            level += 1
            start_new_round()
 
        def show_results_screen() -> None:
            """
            Display the game-over summary inside the window.
            Shows player name, highest level, correct rounds, and
            average reaction time so the player can read results
            before closing. Also saves data to CSV.
            """
            if not results:
                return
 
            highest_level = len(results)
            correct_rounds = [row for row in results if row[1] == 1]
            num_correct = len(correct_rounds)
            reaction_times = [row[2] for row in results]
            avg_rt = sum(reaction_times) / len(reaction_times)
 
            # Build summary string shown in the window
            summary = (
                f"Player: {player_name}\n"
                f"Highest level reached:  {highest_level}\n"
                f"Correct rounds:         {num_correct} / {highest_level}\n"
                f"Avg reaction time:      {avg_rt:.2f} seconds\n\n"
                f"Data saved to data/results.csv"
            )
            results_label.configure(text=summary)
 
            display_results_summary(player_name, results)
            save_data(player_name, results)
 
            # Change Quit to Close so player knows to dismiss manually, from peer reviewer3
            quit_btn.configure(text="Close")
 
        def end_game() -> None:
            """Print summary, save data, and close the window."""
            if results:
                save_data(player_name, results)
            display_results_summary(player_name, results)
            print("\nData saved to data/results.csv")
            window.destroy()
 
        def start_game() -> None:
            """Hide the Start button and begin round 1."""
            start_btn.pack_forget()
            start_new_round()
 
        # ── Buttons ───────────────────────────────────────────────────
        btn_frame = tk.Frame(window, bg="black")
        btn_frame.pack(pady=8)
 
        start_btn = tk.Button(
            btn_frame,
            text="Start Game",
            font="Helvetica 14 bold",
            command=start_game,
        )
        start_btn.pack(side=tk.LEFT, padx=8)
 
        quit_btn = tk.Button(
            btn_frame,
            text="Quit",
            font="Helvetica 12",
            command=end_game,
        )
        quit_btn.pack(side=tk.LEFT, padx=8)
 
        # Draw initial pads before the game starts
        build_pads(get_active_colors(level))
 
    # Start the tkinter event loop
    window.mainloop()
 
 
def main() -> None:
    """Entry point: start the Simon Says GUI."""
    run_game()
 
 
if __name__ == "__main__":
    main()
