"""
Module Name: game_state.py
Class Name: N/A (Module-level functions)

Description: Manages the global game state and victory logic for Minesweeper. 
             Tracks whether the user is actively playing, has won, or has lost, 
             and provides a method to check the grid for win conditions.

Inputs: The 2D grid of Cell objects (passed to check_victory).
Outputs: Boolean victory status and current game status strings.

External sources: Inherited codebase from Project 1.

Authors: Original code by Group 26. 
         Comments added by Group 6: Marie Biernacki.

Creation Date: 9/29/2026 (Inherited)

Modified Date(s): 10/4/2026 (Group 6 Comments)

"""

# --- Constants representing the three possible game states ---
PLAYING = "Playing"
VICTORY = "Victory"
LOSS = "Game Over: Loss"

# Global tracker for current status
game_status = PLAYING


def check_victory(grid):
    """
    Check whether all non-mine cells have been successfully revealed.
    
    Inputs: grid (list of lists): The 2D array of Cell objects.
    Outputs: Returns (bool) - True if won, False if still playing. Updates global game_status.
    
    Authors: Group 26 (Original), Group 6 (Comments)
    """
    global game_status

    # Iterate through every cell in the grid
    for row in grid:
        for cell in row:

            # If we find a cell that does NOT have a mine, but is NOT YET revealed,
            # the game is not over. Return early to continue playing.
            if not cell.is_mine and not cell.is_revealed:
                return False

    # If the nested loops finish without returning, all safe cells have been revealed.
    # The user has won the game.
    game_status = VICTORY
    return True


def set_game_over():
    """
    Triggered when a user clicks a mine. Sets the game state to loss.
    
    Inputs: None.
    Outputs: None. Updates global game_status.
    
    Authors: Group 26 (Original), Group 6 (Comments)
    """
    global game_status
    game_status = LOSS


def reset_game_status():
    """
    Resets the game state tracker back to active play for a new game session.
    
    Inputs: None.
    Outputs: None. Updates global game_status.
    
    Authors: Group 26 (Original), Group 6 (Comments)
    """
    global game_status
    game_status = PLAYING


def get_game_status():
    """
    Retrieves the current game status.
    
    Inputs: None.
    Outputs: Returns (str) - The current game status (Playing, Victory, or Loss).
    
    Authors: Group 26 (Original), Group 6 (Comments)
    """
    return game_status
