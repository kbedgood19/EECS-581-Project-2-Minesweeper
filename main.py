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

Creation Date: 9/29/2026 (Inherited)
Modified Date(s): 10/4/2026 (Group 6 Comments)
"""


from tkinter import Tk, simpledialog

import game_state
import minesweeper
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
    minesweeper.reset() # (Lauren): Reset the game state before starting a new game.
    """
    The main setup function that links the frontend (UI) and backend (logic) together, 
    establishes event handler callbacks, and starts the game loop.
    
    Inputs: None.
    Outputs: None. Begins application execution.
   
    Authors: Original by Group 26. Comments by Group 6.
    """

    # 1. Initialize the backend logic using the user's requested mine count
    minesweeper.configure(get_mine_count())
    game_state.reset_game_status()

    def refresh_status_bar():
        """
        Calculates and pushes the current mine and flag counts to the UI.
        """
        # Update the left side of the status bar (mines remaining)
        ui.update_mine_count(minesweeper.mines_remaining)

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

        # Process the click in the backend and get the updated game status
        status = minesweeper.onLeftClick(col, row)
        
        # Re-render the visual grid and update the status bar numbers
        ui.render(minesweeper.grid)
        refresh_status_bar()

        # Check if this click ended the game
        report_status(status)

    def handle_right_click(row, col):
        """
        Callback triggered when a user right-clicks a tile in the GUI (flagging).
        """
        # Ignore clicks if the game is already won or lost
        if game_state.get_game_status() != game_state.PLAYING:
            return

        # Process the flag toggle in the backend
        status = minesweeper.onRightClick(col, row)

        # Synchronize visuals
        ui.render(minesweeper.grid)
        refresh_status_bar()
        report_status(status)

    def report_status(status):
        """
        Checks the game status and prints a console message upon victory or loss.
        """
        if status == game_state.VICTORY:
            print("You win!")
        elif status == game_state.LOSS:
            print("You lose!")

    # 2. Instantiate the UI, passing in our local click handlers as callbacks
    ui = MinesweeperUI(handle_left_click, handle_right_click)

    # 3. Perform an initial sync of the text in the status bar
    refresh_status_bar()

    # 4. Start the Tkinter main event loop (this blocks until the window is closed)
    ui.run()

# Execute main() only when run as a script
if __name__ == "__main__":
    main()
