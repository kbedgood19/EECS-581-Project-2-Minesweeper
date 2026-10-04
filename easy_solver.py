"""
Module Name: easy_solver.py
Class Name: N/A

Description: Implements the Easy difficulty AI for Minesweeper. The AI uncovers 
             cells randomly, strictly avoiding flagged or already uncovered cells.

Inputs: The 2D grid of Cell objects.
Outputs: Returns a tuple (action, x, y) where action is "reveal" and x, y are coordinates.

External sources: FIXME

Authors: Group 6 - Kaitlyn Bedgood
Creation Date: 10/4/2026

Basic Code Template/Outline: Marie Biernacki, Gemini
"""

import random # MUST IMPORT RANDOM

def get_next_move(grid): # DO NOT CHANGE FUNCTION SIGNATURE OR RETURN TYPE
    """
    Finds a random safe move on the board.
    
    Inputs: grid (list of lists)
    Outputs: tuple ("reveal", x, y)
    -- x is column index, y is row index
    """
    # TODO (Kaitlyn): Implement the Easy AI logic here.
    # 1. Loop through the grid and collect a list of all valid, hidden, unflagged cells.
    # 2. Use random.choice() to select one of those cells.
    # 3. Return the action and the cell's coordinates.
    
    # Placeholder return to prevent crashes during early testing:
    # return ("reveal", 0, 0)
    pass

"""
FIXME DELETE LATER:
Feel free to add additional helper functions, etc as long as get_next_move(grid) returns the expected tuple

"""