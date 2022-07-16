import arcade
import synthizer
import ScreenManager
from GameScreens import MainMenu, SudokuBoard
from speech import Speech
from audio import BufferCache, SoundManager

WIDTH = HEIGHT = 800
TITLE = "Sudoku"


def main():
    with synthizer.initialized():
        ctx = synthizer.Context()
        ctx.enable_events()
        bc = BufferCache()
        sm = SoundManager(ctx, bc)
        speech = Speech()
        game = ScreenManager.ScreenControl(WIDTH, HEIGHT, TITLE, speech, sm)
        screen1 = MainMenu()
        # screen1 = SudokuBoard()
        game.show(screen1)
        # game.show_view(screen1)

        arcade.run()


if __name__ == "__main__":
    main()
