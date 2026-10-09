"""
Module Name: easy_solver.py
Class Name: N/A

Description: Implements the Easy difficulty AI for Minesweeper. The AI uncovers 
             cells randomly, strictly avoiding flagged or already uncovered cells.

Inputs: The 2D grid of Cell objects.
Outputs: Returns a tuple (action, x, y) where action is "reveal" and x, y are coordinates.

External sources: ChatGPT used to help test Easy solver logic

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
    chooses a random valid hidden cell that is not flagged
    input: grid of cell objects
    expected output:
        ("reveal", x, y)

    returns none if no valid cells remain.
    """

    valid_cells = [] #list of valid cells the AI can choose from

    #two dimensional list, goes through every row and cell on board
    for row in grid: #loop through every row
        for cell in row: #loop thorugh each cell in current row
            if not cell.is_revealed and not cell.is_flagged: #check that cell is not revealed or flagged
                valid_cells.append(cell) #add cell to valid_cells as a possible move

    if len(valid_cells) == 0: #check if valid_cells is empty
        return None #returns none if there are no cells to choose from

    cell = random.choice(valid_cells) #randomly chooses one cell from available cells

    return ("reveal", cell.x, cell.y) #return the reveal action and the column and row of chosen cell