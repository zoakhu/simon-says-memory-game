"""
Tests for simon_game.py using pytest.

"""

from simon_game import (
    generate_sequence,
    check_player_input,
    get_active_colors,
)

# Base 4 colors always available from level 1
BASE_COLORS = {"red", "blue", "green", "yellow"}


def test_generate_sequence_length():
    """Sequence length should equal the level passed in."""
    active = get_active_colors(1)
    seq = generate_sequence(5, active)
    assert len(seq) == 5


def test_generate_sequence_valid_colors():
    """Every color in the sequence should be from the active color set."""
    active = get_active_colors(1)
    seq = generate_sequence(10, active)
    # membership operator 'in' (Ch. 1.6)
    assert all(color in active for color in seq)


def test_generate_sequence_level_one():
    """A level-1 sequence should contain exactly one color."""
    active = get_active_colors(1)
    seq = generate_sequence(1, active)
    assert len(seq) == 1


def test_check_player_input_correct():
    """check_player_input should return True when sequences match."""
    seq = ["red", "blue"]
    user = ["red", "blue"]
    assert check_player_input(seq, user) is True


def test_check_player_input_wrong_order():
    """check_player_input should return False when order differs."""
    seq = ["red", "blue"]
    user = ["blue", "red"]
    assert check_player_input(seq, user) is False


def test_check_player_input_wrong_color():
    """check_player_input should return False when a color is wrong."""
    seq = ["red", "blue", "green"]
    user = ["red", "blue", "yellow"]
    assert check_player_input(seq, user) is False


def test_check_player_input_empty():
    """check_player_input should return False when user input is empty."""
    seq = ["red"]
    user = []
    assert check_player_input(seq, user) is False


def test_get_active_colors_base():
    """Levels 1-4 should only have the base 4 colors."""
    for level in range(1, 5):
        active = get_active_colors(level)
        assert set(active) == BASE_COLORS


def test_get_active_colors_purple_unlocked():
    """'purple' should be added at level 5 and remain after."""
    for level in [5, 6, 7]:
        active = get_active_colors(level)
        assert "purple" in active
        assert len(active) == 5


def test_get_active_colors_orange_unlocked():
    """'orange' should be added at level 8 and remain after."""
    active = get_active_colors(8)
    assert "orange" in active
    assert len(active) == 6


def test_get_active_colors_white_unlocked():
    """'white' should be added at level 11, giving 7 total colors."""
    active = get_active_colors(11)
    assert "white" in active
    assert len(active) == 7
