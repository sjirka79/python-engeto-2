"""
main.py: druhý projekt do Engeto Online Python Akademie, version 2

author: Jiří Sedláček
email: sjirka@gmail.com
"""

# version 1 - fully functional, additional functions, mainly stats, based on classes, not approved by evaluator
# version 2 - tiny script, WITHOUT classes - on request of evaluator, removed everything except basic function

import random as rd         # generate the random number
from sys import exit        # exit when error occured

SEP = "-" * 50                  # separator

counter = 0                     # counter of guesses
reports = [
        "Hi there!", 
        """I've generated a random 4 digit number for you.
Let's play a bulls and cows game.""",
        "Enter a number: ",
        """Correct, you've guessed the right number 
in""",
        "That's amazing!",
        """You must enter 4-digit number without a zero in 
the first position where each digit is different."""
        ]

def create_random_number() -> str:
    """Create 4-digit random number where all digits are different 
    from the others, first digit can not be 0."""
    while True:
        random_number = "".join(map(str, rd.sample(range(10), k=4)))    # generate 4-digit random number with distinct digits
        if random_number[0] != "0":                                     # if first digit is "0", generate new random number
            break
    return random_number

def enter_guess() -> str:
    """Enter guessed number and provide its validation due to game rules (4 different digits, zeno not the first)."""
    while True:
        try:
            guess = input()
            if len(set(guess)) != 4 or not guess.isnumeric() or guess[0] == "0":      # check the input for the rules
                print(f"{reports[5]} \n{SEP}")
                raise ValueError
            else:
                break
        except ValueError:
            continue  
        except Exception:
            exit("Some error occured, try to run application again.")   
    return guess       

def check_guess(rnd_number: str, guess: str) -> int:
    """Check the number of bulls and cows"""
    bulls = len([znak for znak in guess if znak == rnd_number[guess.index(znak)]])      # bulls - both char and its position are correct
    cows = len(set(rnd_number) & set(guess)) - bulls                                    # cows - correct chars in wrong place
    return bulls, cows

def plural(pocet: int, last_char: str) -> str:
    """Function of checking 0 or plural BS and cows, guesses respectively"""
    if pocet != 1:
        if last_char == "s":
            plur = "es"
        else:
            plur = "s"
    else:
        plur = ""
    return plur

if __name__ == "__main__":

    # header of the "game"
    print(f"{reports[0]}\n{SEP}")               
    random_number = create_random_number()
    print(f"{reports[1]}\n{SEP}\n{reports[2]}\n{SEP}")

    # body of the code
    while True:
        guess = enter_guess()
        counter += 1                            # counter of guesses
        if guess == random_number:              # if guess is equal to random_number
            break
        bulls, cows = check_guess(random_number,guess)      # calculate the number of bulls and cows
        print(f"{bulls} bull{plural(bulls, "l")}, {cows} cow{plural(cows, "w")}\n{SEP}")

    # conclusion of the "game"
    print(f"{reports[3]} {counter} guess{plural(counter, "s")}\n{SEP}\n{reports[4]}")