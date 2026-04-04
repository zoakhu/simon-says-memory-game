from simon_game import generate_sequence, check_player_input

def test_generate_sequence():
    seq = generate_sequence(5)
    assert len(seq) == 5

def test_correct_input():
    seq = ["red", "blue"]
    user = ["red", "blue"]
    assert check_player_input(seq, user) == True

def test_incorrect_input():
    seq = ["red", "blue"]
    user = ["blue", "red"]
    assert check_player_input(seq, user) == False

# run tests manually
if __name__ == "__main__":
    test_generate_sequence()
    test_correct_input()
    test_incorrect_input()
    print("All tests passed!")