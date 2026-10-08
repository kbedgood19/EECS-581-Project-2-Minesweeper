"""
Module Name: setup_menu.py
Class Name: N/A

Description: Handles the pre-game configuration UI. Prompts the user to select 
             the number of mines, the game mode (Solo, Interactive, Auto), and 
             the AI difficulty (Easy, Medium, Hard) before launching the main board.

Inputs: User interactions via Tkinter UI.
Outputs: Returns a dictionary containing the configuration settings.

External sources: Gemini, https://www.geeksforgeeks.org/python/python-gui-tkinter/

Authors: Group 6 - Marie Biernacki
Creation Date: 10/4/2026

Basic Code Template/Outline: Marie Biernacki, Gemini
"""

import tkinter as tk # MUST IMPORT TKINTER

def get_game_config(): # DO NOT CHANGE FUNCTION SIGNATURE OR RETURN TYPE
    """
    Launches a blocking Tkinter window to gather game settings.
    
    Inputs: None.
    Outputs: Returns (dict) - {"mines": int, "mode": str, "difficulty": str}
    """
    # Initialize the main Tkinter window (root) and set its title and geometry
    root = tk.Tk()
    root.title("Minesweeper - Game Setup")
    root.geometry("350x450")

    # Tkinter Variables to store the selected options.
    # set to default options (10 mines, Solo mode, Easy difficulty)
    mineVar = tk.IntVar(value = 10)
    modeVar = tk.StringVar(value = "Solo")
    difficultyVar = tk.StringVar(value = "Easy")

    # Mine Count Prompt
    # tk.Label prompting for the number of mines (10-20).
    tk.Label(root, text = "Number of Mines (10-20):", font=("Arial", 12, "bold")).pack(pady=(20, 5))
    # Spinbox window to select a number from a fixed range using up/down arrows
    tk.Spinbox(root, from_=10, to=20, textvariable=mineVar, state="readonly").pack()

   # --- Dynamic Disable/Enable ---
    diff_radiobuttons = []  # List to store the difficulty button widgets

    def on_mode_change():
        """Disables AI difficulty buttons if Solo mode is selected."""
        if modeVar.get() == "Solo":
            for rb in diff_radiobuttons:
                rb.config(state=tk.DISABLED)
        else:
            for rb in diff_radiobuttons:
                rb.config(state=tk.NORMAL)

    # Game Mode Prompt
    tk.Label(root, text="Game Mode:", font=("Arial", 12, "bold")).pack(pady=(20, 5))
    modes = ["Solo", "Interactive", "Auto"]
    for mode in modes:
        # Added command=on_mode_change to trigger the check whenever a new mode is clicked
        tk.Radiobutton(root, text=mode, variable=modeVar, value=mode, command=on_mode_change).pack(anchor="w", padx=40)
    
    # AI Difficulty Prompt
    tk.Label(root, text="AI Difficulty:", font=("Arial", 12, "bold")).pack(pady=(20, 5))
    difficulties = ["Easy", "Medium", "Hard"]
    for diff in difficulties:
        rb = tk.Radiobutton(root, text=diff, variable=difficultyVar, value=diff)
        rb.pack(anchor="w", padx=40)
        diff_radiobuttons.append(rb) # Save the widget reference to list

    # call at startup to ensure buttons start disabled (since "Solo" is the default)
    on_mode_change()
    

    # dictionary to store the final configuration
    config = {}

   # submission callback function
    def on_start():
        """Callback function for when the Start button is clicked.
        
        Inputs: None.
        Outputs: Gets the number of mines, mode, and difficulty selections.
        """
        
        config["mines"] = mineVar.get()
        config["mode"] = modeVar.get()

        # Optional: If Solo is selected, set difficulty to None instead of the greyed-out default
        if config["mode"] == "Solo":
            config["difficulty"] = "None"
        else:
            config["difficulty"] = difficultyVar.get()

        # destroy the window to exit the mainloop and return to main.py
        root.destroy()


    # "Start Game" tk.Button and set command to on_start()
    tk.Button(root, text="Start Game", command=on_start, font=("Arial", 12, "bold"), bg="lightgray").pack(pady=30)
    
    # root.mainloop() to block execution and keep the window open until the user clicks Start Game
    root.mainloop()

    # Fallback Safety: Check if 'config' is empty (which happens if the user  clicks the 'X' to close the window)
    # Set default values so the game doesn't crash.
    if not config:
        config = {"mines": 10, "mode": "Solo", "difficulty": "Easy"}

    return config