"""
Module Name: hard_solver.py
Class Name: EECS581 Software Engineering II

Description: Implements the Hard difficulty AI. Detects 1-2-1 patterns across 
             revealed cells to deduce safe and mined neighbors. Falls back to Medium 
             rules if no patterns are found.

Inputs: The 2D grid of Cell objects.
Outputs: Returns a tuple (action, x, y) where action is "reveal" or "flag".

External sources: ChatGPT

Authors: Group 6 - Jaydine Stiles
Creation Date: 10/4/2026

Basic Code Template/Outline: Marie Biernacki, Gemini
"""

import random
import medium_solver


# ---------------------------------------------------------------------------
# expected final solver hierarchy
# ---------------------------------------------------------------------------
#
# HARD:
#     try the 1-2-1 pattern
#         |
#         | if nothing is found
#         v
#
# MEDIUM:
#     try the two basic logical rules
#         |
#         | if nothing is found
#         v
#
# EASY:
#     choose a random valid hidden cell
#
#
# each solver should only contain the logic specific to its difficulty.
#
# easy_solver.py:
#     chooses a random valid hidden cell
#
# medium_solver.py:
#     uses the two basic logical rules
#     then calls easy_solver.py if no logical move can be made
#
# hard_solver.py:
#     uses the 1-2-1 rule
#     then calls medium_solver.py if no 1-2-1 move can be made
#
# because of this, hard_solver.py should NOT permanently duplicate the
# easy or medium solver logic.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# temporary hard ai testing values
# ---------------------------------------------------------------------------

# TEMPORARY TESTING VALUE:
#
# this controls how often the hard ai attempts to use its special 1-2-1 rule.
#
# 1.00 = always try the hard rule
# 0.75 = try the hard rule about 75% of the time
# 0.50 = try the hard rule about 50% of the time
# 0.00 = completely skip the hard rule
#
# IMPORTANT:
#
# this value is mainly here while we are building and testing the different
# solver files.
#
# the random move behavior will most likely be handled inside easy_solver.py.
# once easy_solver.py has its random move logic working correctly, this value
# probably does NOT need to control the difficulty anymore.
#
# for the final hard solver, this should either:
#
#     1. remain at 1.00
#
# OR
#
#     2. be deleted completely along with the random.random() condition
#        inside get_next_move()
#
# lowering this value right now is simply an easy way to intentionally make
# the bot weaker while testing.
HARD_RULE_CHANCE = 1.00


# TEMPORARY TESTING VALUES:
#
# these switches allow us to turn horizontal or vertical 1-2-1 detection
# on and off while debugging.
#
# true = check this direction
# false = ignore this direction
#
# for the finished hard solver, both should normally remain true.
#
# these variables could also eventually be deleted and both directions
# could simply always be checked.
CHECK_HORIZONTAL_121 = True
CHECK_VERTICAL_121 = True


def get_next_move(grid):
    """
    analyzes the board for a 1-2-1 pattern before falling back to medium rules.

    inputs:
        grid - 2D list containing Cell objects

    outputs:
        tuple (action, x, y)

        action will normally be:
            "reveal"
            "flag"

        x = column index
        y = row index
    """

    #protect against an empty or uninitialized board
    if grid is None or len(grid) == 0:
        return medium_solver.get_next_move(grid)

    # -----------------------------------------------------------------------
    # temporary testing section
    # -----------------------------------------------------------------------
    #
    # HARD_RULE_CHANCE lets us intentionally make the hard bot weaker
    # while testing.
    #
    # once easy_solver.py handles random moves correctly, this random chance
    # will probably be unnecessary.
    #
    # the final version could eventually just do:
    #
    #     move = find_121_move(grid)
    #
    # instead of checking random.random().
    #
    # if HARD_RULE_CHANCE is 1.00, this will always attempt the hard rule.
    if random.random() <= HARD_RULE_CHANCE:

        #search the board for a usable 1-2-1 pattern
        move = find_121_move(grid)

        #if the hard rule found something useful, use that move
        if move is not None:
            return move

    # -----------------------------------------------------------------------
    # medium solver handoff
    # -----------------------------------------------------------------------
    #
    # IMPORTANT FOR THE MEDIUM SOLVER:
    #
    # the two normal minesweeper logic rules should be implemented inside
    # medium_solver.py.
    #
    # RULE 1:
    #
    # if the number of hidden neighbors around a revealed cell equals the
    # number shown by that cell, those hidden neighbors should be flagged.
    #
    # RULE 2:
    #
    # if the number of flagged neighbors around a revealed cell equals the
    # number shown by that cell, the remaining hidden neighbors are safe and
    # should be revealed.
    #
    # hard_solver.py should NOT permanently contain copies of those rules.
    #
    # once medium_solver.py is completed, hard_solver.py simply sends control
    # to it whenever no usable 1-2-1 pattern is found.
    #
    # medium_solver.py should then call easy_solver.py if neither of its
    # logical rules can make a move.
    return medium_solver.get_next_move(grid)


def find_121_move(grid):
    """
    scans the entire board for horizontal and vertical 1-2-1 patterns.

    inputs:
        grid - 2D list containing Cell objects

    outputs:
        tuple (action, x, y) if an action can be made

        none if no usable 1-2-1 pattern is found
    """

    #get the current board dimensions instead of assuming a specific board size
    height = len(grid)
    width = len(grid[0])

    # -----------------------------------------------------------------------
    # horizontal 1-2-1 search
    # -----------------------------------------------------------------------
    #
    # example:
    #
    #     ? ? ?
    #     1 2 1
    #
    # or:
    #
    #     1 2 1
    #     ? ? ?
    #
    # the question marks represent hidden cells that may be affected by
    # the 1-2-1 rule.
    # -----------------------------------------------------------------------

    if CHECK_HORIZONTAL_121:

        #loop through every row
        for y in range(height):

            #subtract 2 because a 1-2-1 pattern requires three cells
            for x in range(width - 2):

                #store the three neighboring cells
                left_cell = grid[y][x]
                middle_cell = grid[y][x + 1]
                right_cell = grid[y][x + 2]

                #check whether all three cells are revealed and display 1-2-1
                if (
                    is_revealed_number(left_cell, 1)
                    and is_revealed_number(middle_cell, 2)
                    and is_revealed_number(right_cell, 1)
                ):

                    #a 1-2-1 pattern was found, so inspect the cells around it
                    move = check_horizontal_121(grid, x, y)

                    #if this pattern gives us a valid move, immediately use it
                    if move is not None:
                        return move

    # -----------------------------------------------------------------------
    # vertical 1-2-1 search
    # -----------------------------------------------------------------------
    #
    # example:
    #
    #     ? 1
    #     ? 2
    #     ? 1
    #
    # or:
    #
    #     1 ?
    #     2 ?
    #     1 ?
    #
    # this is the same idea as the horizontal pattern, just rotated.
    # -----------------------------------------------------------------------

    if CHECK_VERTICAL_121:

        #subtract 2 because the pattern requires three cells vertically
        for y in range(height - 2):

            #check every column
            for x in range(width):

                #store the three vertically neighboring cells
                top_cell = grid[y][x]
                middle_cell = grid[y + 1][x]
                bottom_cell = grid[y + 2][x]

                #check whether all three cells are revealed and display 1-2-1
                if (
                    is_revealed_number(top_cell, 1)
                    and is_revealed_number(middle_cell, 2)
                    and is_revealed_number(bottom_cell, 1)
                ):

                    #a vertical 1-2-1 pattern was found
                    move = check_vertical_121(grid, x, y)

                    #if the pattern gives us a valid move, use it
                    if move is not None:
                        return move

    #no usable 1-2-1 pattern was found anywhere on the board
    return None


def is_revealed_number(cell, number):
    """
    checks whether a cell is revealed and displays a specific number.

    inputs:
        cell - Cell object
        number - number we expect the cell to display

    outputs:
        true if the cell is revealed and matches the requested number
        false otherwise
    """

    #IMPORTANT:
    #
    #do not check cell.is_mine here.
    #
    #the ai should only make decisions using information that would normally
    #be visible to a player.
    #
    #looking directly at whether a hidden cell is a mine would basically
    #allow the bot to cheat.
    return cell.is_revealed and cell.adjacent_mines == number


def check_horizontal_121(grid, start_x, y):
    """
    checks the hidden cells surrounding a horizontal 1-2-1 pattern.

    the detected pattern begins at:

        grid[y][start_x]

    example pattern:

        ? ? ?
        1 2 1

    or:

        1 2 1
        ? ? ?

    the two outer hidden cells are mines and the middle hidden cell is safe,
    but only when no other unresolved neighbors can affect the 1-2-1 values.

    possible outputs:

        ("flag", x, y)
        ("reveal", x, y)
        none
    """

    height = len(grid)
    width = len(grid[0])

    #store the positions of the three revealed number cells
    number_positions = [
        (start_x, y),
        (start_x + 1, y),
        (start_x + 2, y),
    ]

    #check the row above the pattern first, then the row below it
    possible_rows = []

    if y - 1 >= 0:
        possible_rows.append(y - 1)

    if y + 1 < height:
        possible_rows.append(y + 1)

    for target_y in possible_rows:
        #these are the three covered cells directly beside the 1-2-1 pattern
        candidate_positions = [
            (start_x, target_y),
            (start_x + 1, target_y),
            (start_x + 2, target_y),
        ]
        candidate_set = set(candidate_positions)

        #make sure no other hidden or flagged neighbors can change the pattern
        pattern_is_clear = True

        for number_x, number_y in number_positions:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    neighbor_x = number_x + dx
                    neighbor_y = number_y + dy

                    #skip coordinates that fall outside the board
                    if not (0 <= neighbor_x < width and 0 <= neighbor_y < height):
                        continue

                    #skip the three cells that the 1-2-1 rule is analyzing
                    if (neighbor_x, neighbor_y) in candidate_set:
                        continue

                    neighbor = grid[neighbor_y][neighbor_x]

                    #an unresolved cell outside the three candidates means the
                    #1-2-1 pattern alone is not enough to prove a move
                    if neighbor.is_flagged or not neighbor.is_revealed:
                        pattern_is_clear = False
                        break

                if not pattern_is_clear:
                    break

            if not pattern_is_clear:
                break

        if not pattern_is_clear:
            continue

        left_cell = grid[target_y][start_x]
        middle_cell = grid[target_y][start_x + 1]
        right_cell = grid[target_y][start_x + 2]

        #the outer cells must still be covered because the 1-2-1 rule says
        #they are mines; a revealed outer cell means this side is not usable
        if left_cell.is_revealed or right_cell.is_revealed:
            continue

        #the middle cell is known to be safe, so a flag on it makes this
        #pattern unusable until that incorrect flag is removed
        if middle_cell.is_flagged:
            continue

        #flag the left mine first if it has not already been flagged
        if not left_cell.is_flagged:
            return ("flag", left_cell.x, left_cell.y)

        #once the left mine is flagged, flag the right mine
        if not right_cell.is_flagged:
            return ("flag", right_cell.x, right_cell.y)

        #after both outer mines are flagged, the middle cell is safe to reveal
        if not middle_cell.is_revealed:
            return ("reveal", middle_cell.x, middle_cell.y)

    #no horizontal 1-2-1 move is currently available
    return None


def check_vertical_121(grid, x, start_y):
    """
    checks the hidden cells surrounding a vertical 1-2-1 pattern.

    the detected pattern begins at:

        grid[start_y][x]

    example pattern:

        ? 1
        ? 2
        ? 1

    or:

        1 ?
        2 ?
        1 ?

    the two outer hidden cells are mines and the middle hidden cell is safe,
    but only when no other unresolved neighbors can affect the 1-2-1 values.

    possible outputs:

        ("flag", x, y)
        ("reveal", x, y)
        none
    """

    height = len(grid)
    width = len(grid[0])

    #store the positions of the three revealed number cells
    number_positions = [
        (x, start_y),
        (x, start_y + 1),
        (x, start_y + 2),
    ]

    #check the column left of the pattern first, then the column to the right
    possible_columns = []

    if x - 1 >= 0:
        possible_columns.append(x - 1)

    if x + 1 < width:
        possible_columns.append(x + 1)

    for target_x in possible_columns:
        #these are the three covered cells directly beside the 1-2-1 pattern
        candidate_positions = [
            (target_x, start_y),
            (target_x, start_y + 1),
            (target_x, start_y + 2),
        ]
        candidate_set = set(candidate_positions)

        #make sure no other hidden or flagged neighbors can change the pattern
        pattern_is_clear = True

        for number_x, number_y in number_positions:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    neighbor_x = number_x + dx
                    neighbor_y = number_y + dy

                    #skip coordinates that fall outside the board
                    if not (0 <= neighbor_x < width and 0 <= neighbor_y < height):
                        continue

                    #skip the three cells that the 1-2-1 rule is analyzing
                    if (neighbor_x, neighbor_y) in candidate_set:
                        continue

                    neighbor = grid[neighbor_y][neighbor_x]

                    #an unresolved cell outside the three candidates means the
                    #1-2-1 pattern alone is not enough to prove a move
                    if neighbor.is_flagged or not neighbor.is_revealed:
                        pattern_is_clear = False
                        break

                if not pattern_is_clear:
                    break

            if not pattern_is_clear:
                break

        if not pattern_is_clear:
            continue

        top_cell = grid[start_y][target_x]
        middle_cell = grid[start_y + 1][target_x]
        bottom_cell = grid[start_y + 2][target_x]

        #the outer cells must still be covered because the 1-2-1 rule says
        #they are mines; a revealed outer cell means this side is not usable
        if top_cell.is_revealed or bottom_cell.is_revealed:
            continue

        #the middle cell is known to be safe, so a flag on it makes this
        #pattern unusable until that incorrect flag is removed
        if middle_cell.is_flagged:
            continue

        #flag the top mine first if it has not already been flagged
        if not top_cell.is_flagged:
            return ("flag", top_cell.x, top_cell.y)

        #once the top mine is flagged, flag the bottom mine
        if not bottom_cell.is_flagged:
            return ("flag", bottom_cell.x, bottom_cell.y)

        #after both outer mines are flagged, the middle cell is safe to reveal
        if not middle_cell.is_revealed:
            return ("reveal", middle_cell.x, middle_cell.y)

    #no vertical 1-2-1 move is currently available
    return None
