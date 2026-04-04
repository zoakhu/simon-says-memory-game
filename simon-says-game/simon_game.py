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




