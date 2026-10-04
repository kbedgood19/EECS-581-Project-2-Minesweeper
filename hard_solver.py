"""
Module Name: hard_solver.py
Class Name: N/A

Description: Implements the Hard difficulty AI. Detects 1-2-1 patterns across 
             revealed cells to deduce safe and mined neighbors. Falls back to Medium 
             rules if no patterns are found.

Inputs: The 2D grid of Cell objects.
Outputs: Returns a tuple (action, x, y) where action is "reveal" or "flag".

External sources: FIXME

Authors: Group 6 - Jaydine Stiles
Creation Date: 10/4/2026

Basic Code Template/Outline: Marie Biernacki, Gemini
"""

import medium_solver # MUST IMPORT MEDIUM_SOLVER

def get_next_move(grid): # DO NOT CHANGE FUNCTION SIGNATURE OR RETURN TYPE
    """
    Analyzes the board for the 1-2-1 pattern before falling back to Medium rules.
    
    Inputs: grid (list of lists)
    Outputs: tuple (action, x, y)
    -- x is column index, y is row index
    """
    # TODO (Jaydine): Implement the Hard AI logic here.
    # Scan the board for three side-by-side revealed cells showing the "1-2-1" pattern.
    
    # RULE: If a 1-2-1 pattern is found:
    # - The two outer hidden neighbors are mines (return "flag" for one of them).
    # - The inner hidden neighbor is safe (return "reveal" for it).
    
    # FALLBACK: If the entire board is scanned and no 1-2-1 pattern is actionable,
    # pass the grid to the Medium solver (which will cascade to Easy if needed).
    return medium_solver.get_next_move(grid)


"""
FIXME DELETE LATER:
Feel free to add additional helper functions, etc as long as get_next_move(grid) returns the expected tuple

"""