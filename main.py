"""
Module Name: main.py
Class Name: N/A (Main Execution Script)

Description: The central entry point for the Minesweeper application. Handles the 
             initial game setup (prompting for mine count via a dialog box), 
             initializes the game logic and user interface, and defines the core 
             event handlers to bridge the UI and backend game state.

Inputs: User input for mine count via dialog box, and user mouse click events.
Outputs: Initializes the GUI window and outputs game status (win/loss) to the console.

External sources: Inherited codebase from Project 1.

Authors: Original code by Group 26. 
         Comments added by Group 6: Marie Biernacki.
         Timer/High Score feature by Group 6: Ximena Bustos.

Creation Date: 9/29/2026 (Inherited)
Modified Date(s): 10/4/2026 (Group 6 Comments)
                  10/7/2026 (Group 6 Timer/High Score Feature)
"""


from tkinter import Tk, simpledialog

import game_state
import minesweeper
import timer        # XIMENA
import setup_menu   # MARIE 
from interface import MinesweeperUI

# --- Global Configurations ---
DEFAULT_MINES = 10

def get_mine_count():
    """
    Spawns a temporary Tkinter dialog window asking the player how many mines 
    they want in the game (between 10 and 20).
    
    Inputs: None (Wait for user GUI input).
    Outputs: Returns (int) - The chosen mine count, or DEFAULT_MINES if canceled.
    
    Authors: Original by Group 26. Comments by Group 6.
    """
    # Create a hidden root window strictly for hosting the dialog box
    root = Tk()
    root.withdraw()

    # Prompt the user for an integer within the restricted bounds
    count = simpledialog.askinteger(
        "Mine Count",
        "How many mines? (10-20)",
        minvalue=10,
        maxvalue=20,
        initialvalue=DEFAULT_MINES
    )

    # Destroy the hidden root window once the dialog is closed
    root.destroy()

    # Fallback to the default if the user hits "Cancel" or closes the window
    return count if count is not None else DEFAULT_MINES


def main():
    """
    The main setup function that links the frontend (UI) and backend (logic) together, 
    establishes event handler callbacks, and starts the game loop.
    
    Inputs: None.
    Outputs: None. Begins application execution.
   
    Authors: Original by Group 26. Comments by Group 6.
    """

    #  ------------------ MARIE ------------------
    config = setup_menu.get_game_config()
    mine_count = config["mines"]
    game_mode = config["mode"]
    ai_difficulty = config["difficulty"]
    # --------------------------------------------
    
    # 1. Initialize the backend logic using the user's requested mine count
    minesweeper.reset() # (Lauren): Reset the game state before starting a new game.
    
    minesweeper.configure(mine_count, game_mode, ai_difficulty) # MARIE - pass all three variables to setup the game
    game_state.reset_game_status()

    def refresh_status_bar():
        """
        Calculates and pushes the current mine and flag counts to the UI.
        """
        # Update the left side of the status bar (static total mine count)
        ui.update_mine_count(minesweeper.NUM_MINES)

        # Calculate flags placed by subtracting remaining mines from total mines
        flags_placed = minesweeper.NUM_MINES - minesweeper.mines_remaining

        # Update the right side of the status bar (flags placed / total mines)
        ui.update_score(flags_placed, minesweeper.NUM_MINES)

    def handle_left_click(row, col):
        """
        Callback triggered when a user left-clicks a tile in the GUI.
        """
        # Ignore clicks if the game is already won or lost
        if game_state.get_game_status() != game_state.PLAYING:
            return

        # ------------------ MARIE ------------------
        # Ignore flags on empty board or already revealed cells
        if minesweeper.grid is not None and minesweeper.grid[row][col].is_revealed:
            return
        # --------------------------------------------

        # ------------------ XIMENA ------------------
        # Starts the timer when the player makes their first move
        # minesweeper.first_click is True until the first left click
        if minesweeper.first_click:
            timer.start_timer()
            ui.update_timer()
        # --------------------------------------------

        # Process the click in the backend and get the updated game status
        status = minesweeper.onLeftClick(col, row)
        
        # Re-render the visual grid and update the status bar numbers
        ui.render(minesweeper.grid)
        refresh_status_bar()

        # Check if this click ended the game
        report_status(status)

        # ------------------ MARIE ------------------
        # Automatically Trigger the AI on Left Click
        # If the game is still going, let the AI take its turn after a 500ms delay
        if status == game_state.PLAYING:
            if minesweeper.GAME_MODE == "Interactive":
                ui.root.after(500, handle_ai_turn)
        # --------------------------------------------


    def handle_right_click(row, col):
        """
        Callback triggered when a user right-clicks a tile in the GUI (flagging).
        """
        # Ignore clicks if the game is already won or lost
        if game_state.get_game_status() != game_state.PLAYING:
            return

        # ------------------ MARIE ------------------
        # Ignore flags on empty board or already revealed cells
        if minesweeper.grid is None or minesweeper.grid[row][col].is_revealed:
            return
        # -------------------------------------------

        # Process the flag toggle in the backend
        status = minesweeper.onRightClick(col, row)

        # Synchronize visuals
        ui.render(minesweeper.grid)
        refresh_status_bar()
        report_status(status)

        # ------------------ MARIE ------------------
        # Automatically Trigger the AI on Right Click
        if status == game_state.PLAYING and minesweeper.GAME_MODE == "Interactive":
            ui.root.after(500, handle_ai_turn)
        # --------------------------------------


    #  ------------------ MARIE ------------------
    def handle_ai_turn():
        """
        Executes the AI move automatically and updates the UI.
        """
        if game_state.get_game_status() != game_state.PLAYING:
            return

        # Start timer for Auto mode before the first move
        if minesweeper.first_click:
            timer.start_timer()
            ui.update_timer()

        # Execute the move and sync the frontend
        status = minesweeper.execute_ai_move()
        ui.render(minesweeper.grid)
        refresh_status_bar()
        report_status(status)

        # If in Auto mode, create an infinite loop of AI turns until the game ends
        if minesweeper.GAME_MODE == "Auto" and status == game_state.PLAYING:
            ui.root.after(500, handle_ai_turn)
    # --------------------------------------------

    
    def report_status(status):
        """
        Checks the game status and prints a console message upon victory or loss.
        """
        if status == game_state.VICTORY:
            # ------------------ XIMENA ------------------
            # Stops the timer so the final game time is saved
            # Gets the final game duration in seconds
            timer.stop_timer()
            game_time = timer.get_time()
            # --------------------------------------------
            print("You win!")
            # ------------------ XIMENA ------------------
            # Checks if the completed time is a new high score
            # Updates the high score displayed in the GUI
            print(f"Game time: {game_time} seconds")        # Prints final game duration
            if timer.save_high_score(game_time):
                print("New High Score!")
            else:
                high_score = timer.get_high_score()
                print(f"High score: {high_score} seconds")
            ui.update_high_score()
            # --------------------------------------------
        elif status == game_state.LOSS:
            # ------------------ XIMENA ------------------
            # Stops the timer when the player loses
            # Gets the final game duration in seconds
            timer.stop_timer()
            game_time = timer.get_time()
            # --------------------------------------------
            print("You lose!")
            # ------------------ XIMENA ------------------
            print(f"Game time: {game_time} seconds")        # Prints final game duration
            # --------------------------------------------

    # 2. Instantiate the UI, passing in our local click handlers as callbacks
    ui = MinesweeperUI(handle_left_click, handle_right_click)

    # 3. Perform an initial sync of the text in the status bar
    refresh_status_bar()

    #  ------------------ MARIE ------------------
    # added for auto mode, to start the game by itself
    if game_mode == "Auto":
        # Wait 1000ms (1 second) for the window to visually load, then go
        ui.root.after(1000, handle_ai_turn)
    # --------------------------------------------

    # 4. Start the Tkinter main event loop (this blocks until the window is closed)
    ui.run()

# Execute main() only when run as a script
if __name__ == "__main__":
    main()
