"""
Module Name: setup_menu.py
Class Name: N/A

Description: Handles the pre-game configuration UI. Prompts the user to select 
             the number of mines, the game mode (Solo, Interactive, Auto), and 
             the AI difficulty (Easy, Medium, Hard) before launching the main board.

Inputs: User interactions via Tkinter UI.
Outputs: Returns a dictionary containing the configuration settings.

External sources: FIXME

Authors: Group 6 - Sabelli Antebi Delmas
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
    # 1. Initialize the main Tkinter window (root) and set its title and geometry.

    # 2. Create Tkinter Variables to store the selected options.
    # You will need an IntVar for the mines (default 10), and StringVars for 
    # mode (default "Solo") and difficulty (default "Easy").

    # 3. Build the Mine Count Section.
    # Create a tk.Label prompting for the number of mines (10-20).
    # Create a tk.Spinbox bound to your IntVar, restricted from 10 to 20.
    # Remember to pack() both widgets!

    # 4. Build the Game Mode Section.
    # Create a tk.Label for "Game Mode:".
    # Create tk.Radiobuttons for "Solo", "Interactive", and "Auto". 
    # Bind them all to your mode StringVar.
    
    # 5. Build the AI Difficulty Section.
    # Create a tk.Label for "AI Difficulty:".
    # Create tk.Radiobuttons for "Easy", "Medium", and "Hard"[cite: 1].
    # Bind them all to your difficulty StringVar.

    # 6. Create an empty dictionary named 'config' to store the final choices.

    # 7. Create a submission callback function (e.g., 'def on_start():').
    # Inside this function, use the .get() method on your Tkinter variables 
    # to populate the 'config' dictionary with the keys "mines", "mode", and "difficulty".
    # Finally, call root.destroy() inside this function to close the window.

    # 8. Create a "Start Game" tk.Button and set its command to your callback function.
    # Pack the button into the window.

    # 9. Call root.mainloop() to block execution and keep the window open until 
    # the user clicks Start.

    # 10. Fallback Safety: Check if 'config' is empty (which happens if the user 
    # clicks the 'X' to close the window instead of clicking Start). 
    # If it is empty, set default values so the game doesn't crash.

    # 11. Return the 'config' dictionary.
    pass