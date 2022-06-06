import arcade
import ScreenManager
from GameScreens import MainMenu, SudokuBoard
from speech import Speech

WIDTH = HEIGHT = 800
TITLE = "Sudoku"


def main():
    speech = Speech()
    game = ScreenManager.ScreenControl(WIDTH, HEIGHT, TITLE, speech)
    screen1 = MainMenu()
    # screen1 = SudokuBoard()
    game.show(screen1)
    # game.show_view(screen1)

    arcade.run()


if __name__ == "__main__":
    main()
