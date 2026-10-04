"""
Module Name: medium_solver.py
Class Name: N/A

Description: Implements the Medium difficulty AI. Applies two deductive rules based 
             on adjacent cell counts. If neither rule applies, falls back to a random click.

Inputs: The 2D grid of Cell objects.
Outputs: Returns a tuple (action, x, y) where action is "reveal" or "flag".

External sources: FIXME

Authors: Group 6 - Greeshma Kunduri
Creation Date: 10/4/2026

Basic Code Template/Outline: Marie Biernacki, Gemini
"""

import easy_solver # MUST IMPORT EASY_SOLVER

def get_next_move(grid): # DO NOT CHANGE FUNCTION SIGNATURE OR RETURN TYPE
    """
    Analyzes the board for logical moves using Medium rules.
    
    Inputs: grid (list of lists)
    Outputs: tuple (action, x, y)
    -- x is column index, y is row index
    """
    # TODO (Greeshma): Implement the Medium AI logic here.
    # Loop through all revealed cells and count their hidden and flagged neighbors.
    
    # RULE 1: If hidden neighbors == cell.adjacent_mines -> flag a hidden neighbor.
    # (If there are multiple, just return one "flag" action. The loop will catch the rest next turn).
    
    # RULE 2: If flagged neighbors == cell.adjacent_mines -> reveal a safe hidden neighbor.
    
    # FALLBACK: If the entire board is scanned and neither rule applies, use the Easy AI.
    return easy_solver.get_next_move(grid)

"""
FIXME DELETE LATER:
Feel free to add additional helper functions, etc as long as get_next_move(grid) returns the expected tuple

"""