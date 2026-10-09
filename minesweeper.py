"""
Prologue Comments: added by Group 6 members for clarity

Module Name: minesweeper.py
Class Name: Cell -- module also acts as the BoardManager

Description: Manages the 10x10 Minesweeper grid logic. Creates and stores 
             Cell objects, handles user click events, manages random mine placement 
             (ensuring the first click is always safe), calculates adjacent mines, 
             and handles the recursive logic for revealing empty cells.

Inputs: Row and column coordinates from user interactions, number of mines.
Outputs: Updates to the grid state, updates to remaining mine counts, and 
         returns game status strings ("Playing", "Victory", "Game Over: Loss").

External sources: Inherited codebase from Group 26

Authors: Original code by Group 26 . 
         Comments added by Group 6: Marie Biernacki.

Creation Date: 9/29/2026 (Inherited)

Modified Date(s): 10/4/2026 (Group 6 Comments)


"""


import random
import game_state

# MARIE - added for AI integration
import easy_solver
import medium_solver
import hard_solver

# --- Global Configurations --- 
GRID_WIDTH = 10
GRID_HEIGHT = 10

# --- Gloabl State Variables ---
NUM_MINES = 10
GAME_MODE = "Solo"          # MARIE - Added for setup_menu config
AI_DIFFICULTY = "Easy"      # MARIE - Added for setup_menu config
mines_remaining = NUM_MINES
first_click = True
grid = None


class Cell:
    """
    Represents a single cell in the Minesweeper grid.
    
    Attributes:
    x (int): The x-coordinate (column).
    y (int): The y-coordinate (row).
    is_mine (bool): True if the cell contains a mine, False otherwise.
    is_revealed (bool): True if the user has uncovered this cell.
    is_flagged (bool): True if the user has flagged this cell.
    adjacent_mines (int): The number of mines in the 8 surrounding neighbor cells.

    Authors: Group 26 (Original), Group 6 (Comments)

    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def reveal(self):
        """ Set's cell's state to revealed. """
        self.is_revealed = True

#  ------------------ MARIE ------------------
# modified to incorporate game mode and difficulty level
def configure(num_mines, mode="Solo", difficulty="Easy"):
    """
    Configures the game's initial mine count.
    
    Inputs:
        num_mines (int) - The total number of mines for the session.
        mode (str) - The selected game mode (Solo, Interactive, Auto).
        difficulty (str) - The AI difficulty (Easy, Medium, Hard).
    Outputs: None. Updates global variables.

    Authors: Group 26 (Original), Group 6 (Comments)
             Group 6 - Marie Biernacki
    
    """
    
    global NUM_MINES, mines_remaining, GAME_MODE, AI_DIFFICULTY
    
    NUM_MINES = num_mines
    mines_remaining = num_mines

    GAME_MODE = mode
    AI_DIFFICULTY = difficulty

#  ------------------ MARIE ------------------
# added to connect the AI Solver levels to the game
def execute_ai_move():
    """
    Requests the next move from the selected AI solver and executes it.
    """
    # Verify game is still active before asking the AI to move
    if game_state.get_game_status() != game_state.PLAYING:
        return game_state.get_game_status()

    # If the board doesn't exist yet, pick a random starting coordinate 
    # so we don't pass 'None' into the solver files and crash them.
    if grid is None:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return onLeftClick(x, y)
    
    
    # Ask the correct AI for its move
    move = None
    if GAME_MODE in ["Interactive", "Auto"]:
        if AI_DIFFICULTY == "Easy":
            move = easy_solver.get_next_move(grid)
        elif AI_DIFFICULTY == "Medium": # FIXME Medium & Hard not complete, these are currently broken
            move = medium_solver.get_next_move(grid)
        elif AI_DIFFICULTY == "Hard":
            move = hard_solver.get_next_move(grid)

    # Execute the move as if a human clicked the board
    if move:
        action, x, y = move
        
        if action == "reveal":
            return onLeftClick(x, y)
        elif action == "flag":
            return onRightClick(x, y)
    
    return game_state.get_game_status()


def onLeftClick(x, y):
    """
    Handle the left click event on the Minesweeper grid.

    Inputs: 
        x (int): The x-coordinate (column) of the clicked cell.
        y (int): The y-coordinate (row) of the clicked cell.
    Outputs: 
        Returns (str): The current game status after the click resolves.

    Authors: Group 26 (Original), Group 6 (Comments)

    """
    global first_click

    # Initialize the board on the very first click to ensure the player's 
    # first move never hits a mine.
    if first_click:
        init_grid(x, y)
        first_click = False
    
    # Check bounds to prevent index out of range errors
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        cell = grid[y][x]

        # Ignore clicks on flagged cells; they must be unflagged to be revealed
        if cell.is_flagged:
            return game_state.get_game_status() 

        # If the cell is safe and hidden, reveal it
        if not cell.is_revealed:
            cell.reveal()
            
            # Condition 1: Player clicked a mine -> Trigger Loss
            if cell.is_mine:
                game_over()
            
            # Condition 2: Player clicked a cell with 0 adjacent mines -> Recursively open neighbors
            elif cell.adjacent_mines == 0:
                reveal_adjacent_cells(x, y)
            
            # If the player didn't click a mine, check if this move won the game
            if not cell.is_mine:
                game_state.check_victory(grid)

    return game_state.get_game_status()


def onRightClick(x, y):
    """
    Handles the right-click event to toggle a flag on a cell.
    
    Inputs: 
        x (int): The x-coordinate (column) of the clicked cell.
        y (int): The y-coordinate (row) of the clicked cell.
    
    Outputs: 
        Returns (str): The current game status. Updates flag visual and mine count.
    
    Authors: Group 26 (Original), Group 6 (Comments)

    """
    global mines_remaining

    # Prevent flagging before the grid is initialized by the first left click
    if grid is None:
        # Nothing has been placed yet; there's nothing to flag before the
        # first left click.
        return game_state.get_game_status()

    # Ensure the click is within the board boundaries
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        cell = grid[y][x]

        # Only allow flagging on cells that are still hidden
        if not cell.is_revealed:
            # cell.is_flagged = not cell.is_flagged # Toggle the boolean state
            
            #  ------------------ MARIE ------------------
            # If the cell doesn't have a flag yet, but we are out of flags, ignore the click
            # This block ensures that you do not have access to infinite flags
            if not cell.is_flagged and mines_remaining <= 0:
                return game_state.get_game_status()

            # Toggle the boolean state
            cell.is_flagged = not cell.is_flagged

            # --------------------------------------------

            # Increment or decrement the remaining mine counter based on the toggle
            if cell.is_flagged:
                mines_remaining -= 1
            else:
                mines_remaining += 1

    return game_state.get_game_status()


def init_grid(firstclick_x, firstclick_y):
    """
    Initializes the 2D grid of Cell objects and populates it with mines.
    
    Inputs: 
        firstclick_x (int): The x-coordinate of the first clicked cell.
        firstclick_y (int): The y-coordinate of the first clicked cell.
    
    Outputs: None. Updates global grid state.
    
    Authors: Group 26 (Original), Group 6 (Comments)
    
    """
    global grid

    # Use list comprehension to build a 2D array of Cell objects (Y rows of X columns)
    grid = [[Cell(x, y) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
    
    # Place mines, passing the first click coordinates so they are protected
    place_mines(firstclick_x, firstclick_y)

    # Pre-calculate the numbers for all safe cells based on new mine locations
    calculate_adjacent_mines()


def place_mines(firstclick_x, firstclick_y):
    """
    Randomly place mines in the grid.

    Inputs: 
        firstclick_x (int): The x-coordinate of the first clicked cell.
        firstclick_y (int): The y-coordinate of the first clicked cell.
    
    Outputs: None. Updates the is_mine attribute of specific Cell objects.
    
    Authors: Group 26 (Original), Group 6 (Comments)
    
    """
    
    mines_placed = 0

    # Continue picking random coordinates until the required number of mines are placed
    while mines_placed < NUM_MINES:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)

        # Place a mine ONLY IF the random cell is not already a mine AND 
        # is not the exact cell the user just clicked to start the game.
        if not grid[y][x].is_mine and (x, y) != (firstclick_x, firstclick_y):
            grid[y][x].is_mine = True
            mines_placed += 1


def calculate_adjacent_mines():
    """
    Calculate the number of adjacent mines for each cell in the grid.

    Inputs: None. Relies on the global grid.
    Outputs: None. Updates the adjacent_mines attribute of Cell objects.
    
    Authors: Group 26 (Original), Group 6 (Comments)

    """
    # Iterate through every single cell on the board
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):

            # We only need to calculate numbers for safe cells
            if not grid[y][x].is_mine:
                count = 0

                # Check the 3x3 block around the current cell (dx, dy from -1 to 1)
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy

                        # Ensure the neighboring coordinate is within the board limits
                        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                            if grid[ny][nx].is_mine:
                                count += 1
                
                # Save the final count to the cell object
                grid[y][x].adjacent_mines = count


def reveal_adjacent_cells(x, y):
    """
    A recursive flood-fill algorithm that opens neighboring cells if the 
    current cell has no adjacent mines (a "0" cell).
    
    Inputs: 
        x (int): Column index of the cell to expand from.
        y (int): Row index of the cell to expand from.
    
    Outputs: None. Modifies the is_revealed state of neighboring cells.
    
    Authors: Group 26 (Original), Group 6 (Comments)
    """

    # Loop through all 8 neighboring directions
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy

            # Check boundaries
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                neighbor_cell = grid[ny][nx]
                # (Lauren): Changes made because it did not check whether neighbor_cell was already flagged
                # BUG: The recursive reveal can currently reach that flagged cell and reveal it internally because it doesn't check is_flagged
                if(not neighbor_cell.is_revealed and not neighbor_cell.is_mine and not neighbor_cell.is_flagged):
                    neighbor_cell.reveal()
                    
                    # If this neighbor also has 0 adjacent mines, recursively 
                    # call the function to continue the flood-fill

                    if neighbor_cell.adjacent_mines == 0:
                        reveal_adjacent_cells(nx, ny)


def game_over():
    """
    Triggers the end of the game logic upon a loss.
    
    Inputs: None.
    Outputs: None. Updates global game_state and reveals all mines.
    
    Authors: Group 26 (Original), Group 6 (Comments)
    """
    game_state.set_game_over()
    print("Game Over! You clicked on a mine.")

    # Iterate over the entire board and flip all mine cells to visible
    for row in grid:
        for cell in row:
            if cell.is_mine:
                cell.reveal()


def reset():
    """
    Resets all variables to their initial state for a new game.
    
    Inputs: None.
    Outputs: None. Clears out the grid and resets globals.
    
    Authors: Group 26 (Original), Group 6 (Comments)

    """
    global grid, first_click, mines_remaining
    grid = None
    first_click = True
    mines_remaining = NUM_MINES
    game_state.reset_game_status()
