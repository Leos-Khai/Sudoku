import arcade

import screen_manager
from audio import BufferCache, SoundManager
from game_screens import MainMenu
from speech import Speech

WIDTH = HEIGHT = 800
TITLE = "Sudoku"


def main():
    # Initialize audio system
    bc = BufferCache()
    sm = SoundManager(bc)
    speech = Speech()

    # Create and run game
    game = screen_manager.ScreenControl(WIDTH, HEIGHT, TITLE, speech, sm)
    screen1 = MainMenu()
    game.show(screen1)

    arcade.run()


if __name__ == "__main__":
    main()
