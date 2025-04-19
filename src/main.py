import arcade
import ScreenManager
from GameScreens import MainMenu, SudokuBoard
from speech import Speech
from audio import BufferCache, SoundManager

WIDTH = HEIGHT = 800
TITLE = "Sudoku"


def main():
    # Initialize audio system
    bc = BufferCache()
    sm = SoundManager(bc)
    speech = Speech()

    # Create and run game
    game = ScreenManager.ScreenControl(WIDTH, HEIGHT, TITLE, speech, sm)
    screen1 = MainMenu()
    game.show(screen1)

    arcade.run()


if __name__ == "__main__":
    main()
