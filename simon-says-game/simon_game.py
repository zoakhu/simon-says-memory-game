import random
import time
import csv

COLORS = ["red", "blue", "green", "yellow"]

def generate_sequence(level):
    sequence = []
    for i in range(level):
        sequence.append(random.choice(COLORS))
    return sequence

def play_sequence(sequence):
    print("\nWatch the sequence:")
    for color in sequence:
        print(color)
        time.sleep(0.8)
    print("\n" * 20)

def get_user_input(length):
    user = input("enter the sequence (seperate by space): ")
    return user.lower().split()

def check_player_input(sequence, user_input):
    if sequence == user_input:
        return True
    else:
        return False 

def save_data(data):
    with open("data/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["round", "correct", "reaction_time"])
        writer.writerows(data)

def run_game():
    level = 1
    results = []

    while True:
        print(f"\nLevel {level}")

        sequence = generate_sequence(level)
        play_sequence(sequence)

        start = time.time()
        user_input = get_user_input(level)
        end = time.time()

        correct = check_player_input(sequence, user_input)
        rt = end - start

        if correct:
            print("correct!")
            results.append([level, 1, rt])
            level += 1
        else:
            print("wrong! game over.")
            results.append([level, 0, rt])
            break

    save_data(results)
    print("Data saved to data/results.csv")

if __name__ == "__main__":
    run_game()


