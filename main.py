"""
main.py: druhý projekt do Engeto Online Python Akademie

author: Jiří Sedláček
email: sjirka@gmail.com
"""

# ============================================================================
# ******************* IMPORT  ************************************************
# ============================================================================

import random as rd         # generate the random number
import time                 # measure the timeof the game
import json                 # export/import game stats to/from file
import os                   # manage the file
from sys import exit        # exit when error occured

# ============================================================================
# ******************* GLOBAL VARIABLES/CONSTANTS *****************************
# ============================================================================

SEP_NO = 70

# set path to file with statistics
CURR_DIR = os.path.dirname(os.path.abspath(__file__))   # path to script
FILENAME = "stats.json"                               
FILEPATH = os.path.join(CURR_DIR, FILENAME)

# ============================================================================
# ******************* CLASSES  ***********************************************
# ============================================================================


class Game:
    """Instance of class is created for every single game."""

    def __init__(self):
        self.beginning = time.time()        # start of the game
        self.counter = 0                    # counter of guesses
        self.bulls = []                     # list for bulls
        self.cows = []                      # list for cows
        self.guess = 0                      # empty guess

    def create_random_number(self) -> None:
        """Create 4-digit random number where all digits are different 
        from the others, first digit can not be 0.
        Create variable \"random_number\" as instance property."""
        self.random_number = str(rd.randint(1, 9))       # first digit
        while len(self.random_number) < 4:               # next 3 digits
            random_number_add = str(rd.randint(0, 9))
            if random_number_add in self.random_number:  # digit already present
                continue
            else:
                self.random_number += random_number_add

    def enter_guess(self) -> None:
        """Enter guessed number and provide its validation due to game
        rules.
        Create variable \"guess\" as instance property."""
        while True:
            try:
                self.guess = input("Enter your guess (or \"q\" to quit the game): ")
                if self.guess.lower() == "q":
                    print(f"{"-" * SEP_NO}")
                    break           
                elif len(self.guess) != 4:      # if guess is not 4-digit long
                    print(f"You have to enter 4-digit long number! \n{"-" * SEP_NO}")
                    raise ValueError
                elif not self.guess.isnumeric():    # if guess is not number
                    print(f"You have to enter numeric value! \n{"-" * SEP_NO}")
                    raise ValueError
                else:
                    break
            except ValueError:
                continue  
            except Exception:
                exit("Some error occured, try to run application again.")   
        self.counter += 1       # increase counter of attempts        

    def check_guess(self) -> None:
        """Check the number of bulls and cows and print their amount.
        If the guess was not the first, compare it with the last one
        and make some note."""
        guess_bulls = 0         # bulls for actual comparison
        guess_cows = 0          # cows for actual comparison
        for char in self.random_number:
            if char == self.guess[self.random_number.index(char)]:
                guess_bulls += 1
                continue
            elif char in self.guess:
                guess_cows += 1
        print(f"{guess_bulls} bull{"s" if guess_bulls != 1 else ""}, {guess_cows} cow{"s" if guess_cows != 1 else ""}")

        # compare actual bulls and cows with the ones from last comparison
        if len(self.bulls) > 0:
            if guess_bulls > self.bulls[-1] and guess_cows > self.cows[-1]:
                note = "You've more of both bulls and cows. Close to the ranch. Yeehaw!"
            elif guess_bulls > self.bulls[-1] and guess_cows == self.cows[-1]:
                note = "Same number of cows but another bull has been found. Giddy up!"
            elif guess_bulls > self.bulls[-1] and guess_cows < self.cows[-1]:
                note = "Found some new bull but lost the cow. Wasn't that bull a cow last time?"
            elif guess_bulls == self.bulls[-1] and guess_cows > self.cows[-1]:
                note = "Same number of bulls but another cow has been found. More fun for bulls."
            elif guess_bulls == self.bulls[-1] and guess_cows == self.cows[-1]:
                note = "Still the same herd. Head 'em up, move 'em out."        
            elif guess_bulls == self.bulls[-1] and guess_cows < self.cows[-1]:
                note = "Same bulls, fewer cows. More fights."
            elif guess_bulls < self.bulls[-1] and guess_cows > self.cows[-1]:
                note = "You've lost the bull but you've found the cow. Milk is better than balls."
            elif guess_bulls < self.bulls[-1] and guess_cows == self.cows[-1]: 
                note = "Fewer bulls for the same number of cows. Cows can rest." 
            elif guess_bulls < self.bulls[-1] and guess_cows < self.cows[-1]:   
                note = "You've lost both bull and cow. Hold your horses."
            print(f"{note}")      

        print(f"{"-" * SEP_NO}")

        # add actual bulls and cows to the list
        self.bulls.append(guess_bulls)
        self.cows.append(guess_cows)

    def game_finished(self) -> None:
        """Game is finished successfully - random_numebr is guessed.
        Final stats of Game instance are calculated and shown to user."""
        self.game_time = (time.time() - self.beginning)
        self.game_time_form = time.strftime("%H:%M:%S", time.gmtime(self.game_time))
        self.game_date_form = time.strftime("%Y-%m-%d", time.gmtime(self.beginning))
        print(f"\nCONGRATULATION, {act_user.nick}. YOU WON!"),
        print(f"You needed {self.counter} guess{"es" if self.counter > 1 else ""}, the game lasted {self.game_time_form}.")
        
    def game_stats_save(self) -> None:
        """Save statistics of current game to 'stats.json'."""
        self.stats = {
            "name": act_user.nick, 
            "date": self.game_date_form,
            "time": self.game_time_form,
            "guesses": self.counter, 
            }
        
        stats_json = json.dumps(self.stats) + "\n"
        with open(FILEPATH, "a") as file:
            file.write(stats_json)

        print(f"Statistics of your game were saved. \n{"-" * SEP_NO}")

class User:
    """User methods and properties."""

    def user_login(self) -> None:
        self.nick = input("Please enter your name or nick: ") 
        if self.nick == "":
            self.nick = "Anonym"
        print(f"Howdy, nice to meet you, {self.nick}. We hope you'll enjoy the game.\n{"*" * SEP_NO}")    

class Stats:
    """Methods and properties for stats calculation and their display"""
    
    def stats_load() -> list:
        """Read statistics from file stats.json.
        Return it as file with dictionaries."""   
        stats_list = [] 

        if os.path.exists(FILEPATH):    # check, if the stats file exists
            # open file and load the stats
            with open(FILEPATH, "r") as file:
                for line in file:
                    stats_list.append(json.loads(line.strip()))
        else:
            print("Stats file does not exist, no game was probably played yet.")
            print(f"{"-" * SEP_NO}")

        return stats_list
    
    def stats_print(title: str, stats_par: list) -> bool:
        """Print statistics from file stats.json."""
        sort_by, name_filter = stats_par
       
        # load stats
        stats_raw = Stats.stats_load()

        if stats_raw:   # stats file was found and data loaded

            # filter stats if required (name_filter == True)
            # stats_filtered = filter(lambda x: x[act_user.nick], stats_raw) if name_filter else stats_raw
            stats_filtered = filter(lambda x: x["name"]==act_user.nick, stats_raw) if name_filter else stats_raw

            # sort stats in order to var sort_by
            stats_ordered = sorted(stats_filtered, key=lambda x: x[sort_by])

            # max. name lenght due to format
            max_name = max((max(len(item["name"]) for item in stats_ordered)), 4)
            
            # print header of table
            sep_no_stat = 34 + max_name
            print(f"{("**** " + title + " ****").center(sep_no_stat)}")
            print("NAME".ljust(max_name), "|", "DATE".center(10), "|", "TIME".center(8), "|", "GUESSES")
            print("-" * sep_no_stat)

            for game in stats_ordered:
                print(game["name"].ljust(max_name), "|",
                    game["date"], "|",
                    game["time"], "|",
                    str(game["guesses"]).rjust(7))
            print("-" * SEP_NO)    

        return False

    def today_stat(title: str, *_) -> bool:
        """Show the stats from actual session stored in game_list."""

        if game_list:       # game_list is not empty, some game was played       

            # print header of table
            print(f"{("**** " + title + " ****").center(25)}")
            print("GAME", "|", "TIME".center(8), "|", "GUESSES")
            print("-" * 25)

            # print single raws of table
            for game in game_list:
                print((str(game_list.index(game) + 1)).rjust(4), "|",
                    game.game_time_form, "|",
                    (str(game.counter)).rjust(7))
                
        else:
            print("No game was already played in this session.")

        print("-" * SEP_NO)    
        return False
    
    def Stats_exit(*_) -> bool:
        """Exit Stats."""
        return True
  
class AppCore:
    """Appplication methods and properties."""

    def __init__(self, title, MENU):
        self.menu_title = title
        self.menu_dict = MENU

    TITLE = r"""
    
WELCOME IN OUR BRAND NEW GAME
 ____        _ _        ___      ____                  
| __ ) _   _| | |___   ( _ )    / ___|_____      _____ 
|  _ \| | | | | / __|  / _ \/\ | |   / _ \ \ /\ / / __|
| |_) | |_| | | \__ \ | (_>  < | |__| (_) \ V  V /\__ \
|____/ \__,_|_|_|___/  \___/\/  \____\___/ \_/\_/ |___/

Cattle Inc.  (c)2025
"""

    RULES = """The computer will generate a 4-digit long random number. This number
does not start with 0 (zero) and every digit is different.   
Your goal is to guess this number in as few steps as possible.

Your guess is evaluated as follows:
    BULL - correct digit in the correct place
    COW - correct digit in the wrong place.

Good luck."""

    def run_game(*_) -> bool:
        """Run the game"""

        # every single game is stored as global instance of class "Game"
        global act_game
        act_game = Game()               # new instance of class Game

        global game_list                # all games are stored in list
        game_list.append(act_game)      # add instance to game_list, global

        act_game.create_random_number()     # generate new random_number

        while True:                     # guessing the random number
            act_game.enter_guess()
            if act_game.guess.lower() == "q":   # user wants to quit game
                game_list.pop()                 # remove last (unfinished) game
                break
            elif act_game.guess == act_game.random_number:  # user has won
                act_game.game_finished() 
                act_game.game_stats_save() 
                break
            else:                               # normal game progress 
                act_game.check_guess()   
        return False

    def rules(*_) -> bool:
        """Display the rules"""
        print(f"{AppCore.RULES} \n{"*" * SEP_NO}")
        return False

    def AppCore_exit(*_) -> bool:
        """Exit the AppCore"""
        print(f"Thank you for the play, {act_user.nick}.\nWe hope you have enjoyed it.")
        print(f"{"*" * SEP_NO}")
        return True

    def show_menu(menu_title: str, menu_dict: dict) -> None:
        """Show the menu items."""
        print(f"{menu_title}")
        item = 1
        for key in menu_dict.keys():
            print(f"{" " * 4}{item} - {key}")
            item += 1
        print(f"{"-" * SEP_NO}")

    def menu_choice(self, *_):
        """Enter a choice from the menu.""" 
        self.app_exit = False
        while not self.app_exit:
            try:
                AppCore.show_menu(self.menu_title, self.menu_dict)
                self.choice = input(f"Enter your choice (1-{len(self.menu_dict)}): ")
                print(f"{"-" * SEP_NO}")
                if not self.choice.isnumeric():
                    # check the choice to be numerical
                    print(f"You have to enter a number! \n{"-" * SEP_NO}")
                    raise ValueError
                elif int(self.choice) not in range(1, len(self.menu_dict)+1):
                    # check the choice to be in given range
                    print(f"You have to enter a number in range from 1 to {len(self.menu_dict)}! \n{"-" * SEP_NO}")
                    raise ValueError
                else:
                    # run the appropriate function from menu_dict
                    self.act_fce = list(self.menu_dict.values())[int(self.choice)-1]
                    self.app_exit = self.act_fce[0](self.act_fce[1], self.act_fce[2])
            except ValueError:
                continue  
            except Exception:
                exit("Some error occured, try to run application again.")    

# ============================================================================
# ******************* APP BLOCK  *********************************************
# ============================================================================  

if __name__ == "__main__":

    # title screen, create User instance, user login
    print(f"{AppCore.TITLE}\n{"*" * SEP_NO}")
    act_user = User()
    act_user.user_login()

    # instances of class Game are stored in list "game_list"
    game_list = []
    
    # create instance for stats menu
    MENU_STATS = {
        "Today's stat": [Stats.today_stat, "TODAY'S STATS", ""],
        "My stats (guesses ordered)": [Stats.stats_print, "MY STATS (BY GUESSES)", ["guesses", True]],
        "My stats (time ordered)": [Stats.stats_print, "MY STATS (BY TIME)", ["time", True]],
        "My stats (date ordered)": [Stats.stats_print, "MY STATS (BY DATE)", ["date", True]],
        "Total stats (guesses ordered)": [Stats.stats_print, "TOTAL STATS (BY GUESSES)", ["guesses", False]],
        "Total stats (time ordered)": [Stats.stats_print, "TOTAL STATS (BY TIME)", ["time", False]],
        "Total stats (name ordered)": [Stats.stats_print, "TOTAL STATS (BY NAME)", ["name", False]],
        "Total stats (date ordered)": [Stats.stats_print, "TOTAL STATS (BY DATE)", ["date", False]],
        "Back to MAIN MENU": [Stats.Stats_exit, "", ""]        
        }
    stats_menu = AppCore("STATISTICS", MENU_STATS)
    
    # create instance for main menu
    MENU_MAIN = {
        "New game": [AppCore.run_game, "", ""],            
        "Statistics": [stats_menu.menu_choice, "", ""],
        "Rules": [AppCore.rules, "", ""],
        "Exit": [AppCore.AppCore_exit, "", ""]
        }
    appcore_menu = AppCore("MAIN MENU:", MENU_MAIN)
    
    # run the instance for the main menu
    appcore_menu.menu_choice()


    
