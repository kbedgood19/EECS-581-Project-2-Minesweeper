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

"""
Description: Implements the Medium difficulty AI solver.

The Medium solver uses two basic Minesweeper rules.

Rule 1:
If all remaining hidden neighbors must be mines, flag them.

Rule 2:
If enough mines around a revealed cell are already flagged,
the remaining hidden neighbors are safe.

If neither rule works, fall back to Easy.
"""

import easy_solver #MUST IMPORT EASY SOLVER


def get_next_move(grid):
    """
    searches for a logical move before falling back to easy.
    """

    #todo:
    #loop through every revealed cell on the board

    #todo:
    #find all neighboring cells around the current revealed cell

    #todo:
    #separate those neighbors into:
    #     hidden neighbors
    #     flagged neighbors


    # ---------------------------------------------------------------
    # rule 1
    # ---------------------------------------------------------------

    #todo:
    #figure out how many mines are still needed around the cell

    #todo:
    #if the number of hidden neighbors equals the number of mines
    #still needed, return one of those cells as:
    #
    #     ("flag", x, y)


    # ---------------------------------------------------------------
    # rule 2
    # ---------------------------------------------------------------

    #todo:
    #if the number of flagged neighbors already equals the number
    #shown on the revealed cell, the remaining hidden neighbors are safe

    #todo:
    #return one safe hidden cell as:
    #
    #     ("reveal", x, y)


    #todo:
    #if neither medium rule works, fall back to easy
    #
    #     return easy_solver.get_next_move(grid)

    pass