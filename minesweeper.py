"""
Minesweeper Game Logic for EECS581
"""

import random
import game_state

GRID_WIDTH = 10
GRID_HEIGHT = 10

NUM_MINES = 10
mines_remaining = NUM_MINES
first_click = True
grid = None


class Cell:
    """
    Represents a single cell in the Minesweeper grid.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def reveal(self):
        self.is_revealed = True


def configure(num_mines):
    global NUM_MINES, mines_remaining
    NUM_MINES = num_mines
    mines_remaining = num_mines


def onLeftClick(x, y):
    """
    Handle the left click event on the Minesweeper grid.

    Parameters:
    x (int): The x-coordinate of the clicked cell.
    y (int): The y-coordinate of the clicked cell.
    """
    global first_click

    if first_click:
        init_grid(x, y)
        first_click = False

    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        cell = grid[y][x]

        if cell.is_flagged:
            return game_state.get_game_status()  # flagged cells can't be revealed

        if not cell.is_revealed:
            cell.reveal()
            if cell.is_mine:
                game_over()
            elif cell.adjacent_mines == 0:
                reveal_adjacent_cells(x, y)
            if not cell.is_mine:
                game_state.check_victory(grid)

    return game_state.get_game_status()


def onRightClick(x, y):
    """
    Handle the right click event on the Minesweeper grid (toggles a flag).

    Parameters:
    x (int): The x-coordinate (column) of the clicked cell.
    y (int): The y-coordinate (row) of the clicked cell.
    """
    global mines_remaining

    if grid is None:
        # Nothing has been placed yet; there's nothing to flag before the
        # first left click.
        return game_state.get_game_status()

    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        cell = grid[y][x]
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged
            if cell.is_flagged:
                mines_remaining -= 1
            else:
                mines_remaining += 1

    return game_state.get_game_status()


def init_grid(firstclick_x, firstclick_y):
    """
    Initialize the Minesweeper grid with cells.

    Parameters:
    firstclick_x (int): The x-coordinate of the first clicked cell.
    firstclick_y (int): The y-coordinate of the first clicked cell.
    """
    global grid
    grid = [[Cell(x, y) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
    place_mines(firstclick_x, firstclick_y)
    calculate_adjacent_mines()


def place_mines(firstclick_x, firstclick_y):
    """
    Randomly place mines in the grid.

    Parameters:
    firstclick_x (int): The x-coordinate of the first clicked cell.
    firstclick_y (int): The y-coordinate of the first clicked cell.
    """
    mines_placed = 0
    while mines_placed < NUM_MINES:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)

        # Original condition here was `not A or not B`, which is true for
        # almost any cell and barely constrained placement. This requires
        # both: the cell isn't already a mine, AND it isn't the first-clicked
        # cell.
        if not grid[y][x].is_mine and (x, y) != (firstclick_x, firstclick_y):
            grid[y][x].is_mine = True
            mines_placed += 1


def calculate_adjacent_mines():
    """
    Calculate the number of adjacent mines for each cell in the grid.
    """
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if not grid[y][x].is_mine:
                count = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                            if grid[ny][nx].is_mine:
                                count += 1
                grid[y][x].adjacent_mines = count


def reveal_adjacent_cells(x, y):
    """
    Reveal adjacent cells recursively if they are not mines and have no
    adjacent mines.
    """
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                neighbor_cell = grid[ny][nx]
                # (Lauren): Changes made because it did not check whether neighbor_cell was already flagged
                # BUG: The recursive reveal can currently reach that flagged cell and reveal it internally because it doesn't check is_flagged
                if (not neighbor_cell.is_revealed and not neighbor_cell.is_mine and not neighbor_cell.is_flagged):
                    neighbor_cell.reveal()

                    if neighbor_cell.adjacent_mines == 0:
                        reveal_adjacent_cells(nx, ny)


def game_over():
    """
    Handle the game over scenario when a mine is clicked.
    """
    game_state.set_game_over()
    print("Game Over! You clicked on a mine.")
    for row in grid:
        for cell in row:
            if cell.is_mine:
                cell.reveal()


def reset():
    """
    Reset all module-level state for a new game (call before starting over).
    """
    global grid, first_click, mines_remaining
    grid = None
    first_click = True
    mines_remaining = NUM_MINES
    game_state.reset_game_status()
