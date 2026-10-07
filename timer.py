"""
Module Name: timer.py
Class Name: N/A

Description: Tracks the duration of a game and stores the player's best completion time.
             The timer starts when the player makes their first move and stops when the 
             game ends. The lower completion times are considered better high scores.

Inputs: Game start and end times, and the player's completed game time.
Outputs: Elapsed game time and saved high score information.

External sources: https://www.w3schools.com/python/module_os.asp, https://www.geeksforgeeks.org/python/os-module-python-examples/, 
                  https://www.geeksforgeeks.org/python/python-time-module/, ChatGPT 

Authors: Group 6 - Ximena Bustos
Creation Date: 10/7/2026

"""

import time     # Imports time module so we can record the current time
import os       # Imports os module so we check whether high score file exists

HIGH_SCORE_FILE = "high_score.txt"      # The file where the player's best time will be stored

start_time = None       # Stores time when current game starts. At None because game has not started yet
end_time = None         # Stores time when current game ends. At None because game has not started yet

# Starts timer when the player makes their first move.
def start_timer():
    global start_time       # The global variables will be changed
    global end_time

    # Records the time at the beginning of the game
    # Resets end_time because it's a new game
    # Allows the timer to run again if a previous game has ended
    start_time = time.time()
    end_time = None

# Stops the timer when game ends
def stop_timer():
    global end_time     # The global variable will be changed

    # Only stop the timer if the game was actually started
    # Records current time as the end of the game
    if start_time is not None:
        end_time = time.time()

# Returns the number of seconds that have passed since the game started
def get_time():
    # If the timer not started, there is no elapsed game time
    # Returns 0 seconds.
    if start_time is None:
        return 0
    
    # If the game has ended, the saved time will be used
    # Returns the subtracted start time from the end time
    if end_time is not None:
        return int(end_time - start_time)
    
    # This continuously shows the current game duration
    return int(time.time() - start_time)

# Reads and returns the saved high score
def get_high_score():
    # Checks if the high score file exists
    # No file, no high score yet
    if not os.path.exists(HIGH_SCORE_FILE):
        return None
    
    # Opens the high score file in read mode
    # Reads the value from the file and converts string
    # to integer so it can be compared with other times
    with open(HIGH_SCORE_FILE, "r") as file:
        return int(file.read())
    
# Sves the player's game time if it's a new high score
def save_high_score(game_time):
    # Gets the player's previous high score
    high_score = get_high_score()

    # A new high score happens if then there is no previoud high score 
    # or the current game finished faster than the old high score
    if high_score is None or game_time < high_score:
        with open(HIGH_SCORE_FILE, "w") as file:        # Opens the high score file in write mode
            file.write(str(game_time))          # Converts the game time to a string and saves it to the file

        return True         # Returns True to tell main.py that a new high score was saved
    
    return False            # Returns False if the current time was not better than the existing high score