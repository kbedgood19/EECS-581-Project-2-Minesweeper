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

"""
Description: Implements the Easy difficulty AI solver.

The Easy solver should randomly choose a valid hidden cell.
It should avoid cells that are already revealed or flagged.
"""

import random #MUST IMPORT RANDOM


def get_next_move(grid):
    """
    chooses a random valid hidden cell.

    expected output:
        ("reveal", x, y)

    returns none if no valid cells remain.
    """

    #todo:
    #create a list to store possible cells the ai can choose from

    #todo:
    #loop through every cell in the grid

    #todo:
    #only include cells that are:
    #     not revealed
    #     not flagged

    #todo:
    #if there are no valid cells left, return none

    #todo:
    #use random.choice() to select one valid cell

    #todo:
    #return the selected cell in this format:
    #
    #     ("reveal", x, y)

    pass