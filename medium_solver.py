"""
Module Name: medium_solver.py
Class Name: N/A

Description: Implements the Medium difficulty AI. Applies two deductive rules based 
             on adjacent cell counts. If neither rule applies, falls back to a random click.

Inputs: The 2D grid of Cell objects.
Outputs: Returns a tuple (action, x, y) where action is "reveal" or "flag".

External sources: ChatGPT

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

    # loop through every revealed cell on the board
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            cell = grid[y][x]

            if not cell.is_revealed:
                continue

            hidden_neighbors = []
            flagged_neighbors = []

            # find all neighboring cells
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue

                    nx = x + dx
                    ny = y + dy

                    if not (0 <= ny < len(grid)):
                        continue
                    if not (0 <= nx < len(grid[ny])):
                        continue

                    neighbor = grid[ny][nx]

                    if neighbor.is_flagged:
                        flagged_neighbors.append(neighbor)
                    elif not neighbor.is_revealed:
                        hidden_neighbors.append(neighbor)

            # Rule 1: flag a hidden neighbor if it must be a mine
            mines_needed = cell.adjacent_mines - len(flagged_neighbors)

            if hidden_neighbors and len(hidden_neighbors) == mines_needed:
                neighbor = hidden_neighbors[0]
                return ("flag", neighbor.x, neighbor.y)

    # Rule 2: reveal a hidden neighbor if all mines are flagged
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            cell = grid[y][x]

            if not cell.is_revealed:
                continue

            hidden_neighbors = []
            flagged_count = 0

            # find neighboring cells
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue

                    nx = x + dx
                    ny = y + dy

                    if not (0 <= ny < len(grid)):
                        continue
                    if not (0 <= nx < len(grid[ny])):
                        continue

                    neighbor = grid[ny][nx]

                    if neighbor.is_flagged:
                        flagged_count += 1
                    elif not neighbor.is_revealed:
                        hidden_neighbors.append(neighbor)

            if flagged_count == cell.adjacent_mines and hidden_neighbors:
                neighbor = hidden_neighbors[0]
                return ("reveal", neighbor.x, neighbor.y)

    # if neither medium rule works, fall back to easy
    return easy_solver.get_next_move(grid)
