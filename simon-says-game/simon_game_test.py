"""Tests for simon_game.py using pytest."""
from simon_game import generate_sequence, check_player_input

COLORS = {"red", "blue", "green", "yellow"}

def test_generate_sequence_length():
    """Sequence length should equal the level passed in."""
    seq = generate_sequence(5)
    assert len(seq) == 5

def test_generate_sequence_valid_colors():
    """All colors in the sequence should be from the valid color set."""
    seq = generate_sequence(10)
    assert all(color in COLORS for color in seq)

def test_correct_input():
    """check_player_input should return True when sequences match."""
    seq = ["red", "blue"]
    user = ["red", "blue"]
    assert check_player_input(seq, user) is True

def test_incorrect_input():
    """check_player_input should return False when sequences differ."""
    seq = ["red", "blue"]
    user = ["blue", "red"]
    assert check_player_input(seq, user) is False
