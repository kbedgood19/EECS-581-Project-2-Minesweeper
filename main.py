from tkinter import Tk, simpledialog

import game_state
import minesweeper
from interface import MinesweeperUI

DEFAULT_MINES = 10


def get_mine_count():
    root = Tk()
    root.withdraw()
    count = simpledialog.askinteger(
        "Mine Count",
        "How many mines? (10-20)",
        minvalue=10,
        maxvalue=20,
        initialvalue=DEFAULT_MINES
    )
    root.destroy()
    return count if count is not None else DEFAULT_MINES


def main():
    minesweeper.reset() # (Lauren): Reset the game state before starting a new game.
    minesweeper.configure(get_mine_count())
    game_state.reset_game_status()

    def refresh_status_bar():
        ui.update_mine_count(minesweeper.mines_remaining)
        flags_placed = minesweeper.NUM_MINES - minesweeper.mines_remaining
        ui.update_score(flags_placed, minesweeper.NUM_MINES)

    def handle_left_click(row, col):
        if game_state.get_game_status() != game_state.PLAYING:
            return
        status = minesweeper.onLeftClick(col, row)
        ui.render(minesweeper.grid)
        refresh_status_bar()
        report_status(status)

    def handle_right_click(row, col):
        if game_state.get_game_status() != game_state.PLAYING:
            return
        status = minesweeper.onRightClick(col, row)
        ui.render(minesweeper.grid)
        refresh_status_bar()
        report_status(status)

    def report_status(status):
        if status == game_state.VICTORY:
            print("You win!")
        elif status == game_state.LOSS:
            print("You lose!")

    ui = MinesweeperUI(handle_left_click, handle_right_click)
    refresh_status_bar()
    ui.run()


if __name__ == "__main__":
    main()
