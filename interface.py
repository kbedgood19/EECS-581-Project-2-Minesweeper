"""
Module Name: interface.py
Class Name: MinesweeperUI

Description: Handles the graphical user interface for the Minesweeper game using 
             the tkinter library. Manages window creation, rendering, image scaling, 
             grid drawing, and visual state updates based on the underlying game logic.

Inputs: Callback functions for left and right mouse clicks, and the game state grid.
Outputs: A Tkinter GUI window displaying the interactive game board and status bar.

External sources: Inherited codebase from Project 1.

Authors: Original code by Group 26 (Caleb Harmsen). 
         Comments and bug fixes added by Group 6: Marie Biernacki, Lauren Lee.

Creation Date: 9/29/2026 (Inherited)
Modified Date(s): 10/4/2026 (Group 6 Comments + Updates)

"""

import tkinter as tk
import sys # (Lauren): Added for synchronized UI on both Windows and macOS.

# --- GUI Constants ---
BOARD_SIZE = 10
TILE_SIZE = 40


class MinesweeperUI:
    def __init__(self, on_left_click, on_right_click):
        """
        Initializes the Tkinter window, loads assets, and builds the UI layout.
        
        Inputs: 
            on_left_click (callable): Function to execute when a tile is left-clicked fn(row, col).
            on_right_click (callable): Function to execute when a tile is right-clicked fn(row, col).
        
        Outputs: None. Instantiates UI components.
        
        Authors: Group 26 (Original), Group 6 (Comments)
        
        """
        # Create the main application window
        self.root = tk.Tk()
        self.root.title("EECS 581 - Minesweeper - Group 6") # Updated to reflect current team

        # Pre-load and scale images so they fit precisely inside the button tiles
        self.mine_image = self._load_scaled_image("mine.png", TILE_SIZE)
        self.flag_image = self._load_scaled_image("flag.png", TILE_SIZE)

        # --- Status Bar Setup ---
        # Create a container frame at the top for the scores/mine counts
        self.status_bar = tk.Frame(self.root)
        self.status_bar.pack(padx=10, pady=(10, 0), fill="x")

        # Initialize and pack the dynamic label tracking remaining mines (left side)
        self.mine_count_var = tk.StringVar(value="Mines: 0")
        tk.Label(
            self.status_bar,
            textvariable=self.mine_count_var,
            font=("TkDefaultFont", 11, "bold")
        ).pack(side="left")

        # Initialize and pack the dynamic label tracking flags placed (right side)
        self.score_var = tk.StringVar(value="Flags: 0/0")
        tk.Label(
            self.status_bar,
            textvariable=self.score_var,
            font=("TkDefaultFont", 11, "bold")
        ).pack(side="right")

        # --- Game Board Setup ---
        # Create a central frame to hold the grid of clickable buttons
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.tiles = []
        self._build_board(on_left_click, on_right_click)



    def update_mine_count(self, count):
        """
        Updates the UI text showing how many unflagged mines remain.
        
        Inputs: count (int) - The calculated remaining mines.
        Outputs: None. Updates a Tkinter StringVar.
        
        Authors: Group 26 (Original), Group 6 (Comments)
        """
        self.mine_count_var.set(f"Mines: {count}")

    
    
    def update_score(self, flags_placed, total_mines):
        """
        Updates the scoreboard showing the ratio of flags placed to total mines.
        
        Inputs: 
            flags_placed (int): Number of flags currently on the board.
            total_mines (int): Total number of mines in the game.
        
        Outputs: None. Updates a Tkinter StringVar.
        
        Authors: Group 26 (Original), Group 6 (Comments)
        """
        self.score_var.set(f"Flags: {flags_placed}/{total_mines}")

    
    
    def _load_scaled_image(self, path, target_size):
        """
        Loads a PhotoImage from disk and scales it to match the TILE_SIZE.
        
        Inputs: 
            path (str): Filepath to the image.
            target_size (int): The desired pixel width/height.
        
        Outputs: Returns (tk.PhotoImage) - The properly scaled image object.
       
        Authors: Group 26 (Original), Group 6 (Comments)
        """
        image = tk.PhotoImage(file=path)
        width = image.width()
        
        # Failsafe if image doesn't load properly
        if width <= 0:
            return image

        # Scale up using zoom if the image is too small
        if width < target_size:
            factor = max(1, target_size // width)
            image = image.zoom(factor, factor)

        # Scale down using subsample if the image is too large
        elif width > target_size:
            factor = max(1, round(width / target_size))
            image = image.subsample(factor, factor)

        return image

    
    
    def _build_board(self, on_left_click, on_right_click):
        """
        Constructs the 2D grid of Tkinter buttons representing the game board.
        
        Inputs: 
            on_left_click (callable): Game logic trigger for left clicks.
            on_right_click (callable): Game logic trigger for right clicks.
        
        Outputs: None. Populates the self.tiles 2D array.
        
        Authors: Group 26 (Original), Group 6 (Modified to fix Mac/Linux bug)
        """
        # A transparent 1x1 image used to enforce consistent button dimensions in Tkinter
        self.blank_image = tk.PhotoImage(width=TILE_SIZE, height=TILE_SIZE)

        for r in range(BOARD_SIZE):
            row_tiles = []
            for c in range(BOARD_SIZE):
                
                # Create a button for every coordinate in the grid
                tile = tk.Button(
                    self.frame,
                    image=self.blank_image,
                    width=TILE_SIZE,
                    height=TILE_SIZE,
                    compound="center",
                    borderwidth=1,
                    relief="raised", # 'raised' gives it a 3D clickable look
                    command=lambda row=r, col=c: on_left_click(row, col) # Bind Left Click
                )
                # (Lauren): changed made to allow right click to work on macOS and Windows
                if sys.platform == "darwin":  # macOS
                    # Assigning the right-click event to Button-2 for macOS
                    tile.bind(
                        "<Button-2>",
                        lambda event, row=r, col=c: on_right_click(row, col)
                    )
                else:  # Windows/Linux
                    # Assigning the right-click event to Button-3 for Windows/Linux
                    tile.bind(
                        "<Button-3>",
                        lambda event, row=r, col=c: on_right_click(row, col)
                    )
                tile.grid(row=r, column=c, padx=1, pady=1)
                row_tiles.append(tile)

            self.tiles.append(row_tiles)

    
    
    def set_tile(self, row, col, tile_type, number=0):
        """
        Updates the visual appearance of a specific tile based on its current state.
        
        Inputs: 
            row (int): The y-coordinate of the tile.
            col (int): The x-coordinate of the tile.
            tile_type (str): The state to render ("covered", "uncovered", "flag", "mine").
            number (int, optional): The adjacent mine count to display if uncovered.
        
        Outputs: None. Configures the Tkinter button widget.
        
        Authors: Group 26 (Original), Group 6 (Comments)

        """
        tile = self.tiles[row][col]

        # State 1: Default unclicked tile
        if tile_type == "covered":
            tile.config(
                image=self.blank_image,
                text="",
                compound="center",
                relief="raised",
                bg="SystemButtonFace"
            )

        # State 2: Safely opened tile (shows number, or blank if 0)
        elif tile_type == "uncovered":
            tile.config(
                image=self.blank_image,
                text=str(number) if number else "",  # Only print the number if > 0
                compound="center",
                relief="sunken", # 'sunken' indicates it has been pressed
                bg="lightgray"
            )

        # State 3: User flagged tile
        elif tile_type == "flag":
            tile.config(image=self.flag_image, text="", compound="center", relief="raised")

        # State 4: Revealed mine (usually shown on Game Over)
        elif tile_type == "mine":
            tile.config(image=self.mine_image, text="", compound="center", relief="sunken")

    
    
    def render(self, grid):
        """
        Iterates over the backend logic grid and synchronizes the entire UI.
        
        Inputs: grid (list of lists): The 2D array of Cell objects from minesweeper.py.
        Outputs: None. Calls set_tile for every coordinate.
        
        Authors: Group 26 (Original), Group 6 (Comments)
        """
        # Do not attempt to render if the backend grid hasn't been initialized yet
        if grid is None:
            return

        # Loop through every backend cell and map its boolean attributes to a visual state
        for row in grid:
            for cell in row:
                if cell.is_flagged:
                    self.set_tile(cell.y, cell.x, "flag")
                elif not cell.is_revealed:
                    self.set_tile(cell.y, cell.x, "covered")
                # (Lauren): "and cell.is_revealed" added to fix where the UI prevents from showing a mine when the cell is flagged
                elif cell.is_mine and cell.is_revealed:
                    self.set_tile(cell.y, cell.x, "mine")
                else:
                    self.set_tile(cell.y, cell.x, "uncovered", cell.adjacent_mines)

   
   
    def run(self):
        """
        Starts the Tkinter main event loop, keeping the window open and responsive.
        
        Inputs: None.
        Outputs: None. Blocks execution until window is closed.
        
        Authors: Group 26 (Original), Group 6 (Comments)
        """
        self.root.mainloop()
