import arcade
from src.speech import Speech

WIDTH = HEIGHT = 800
TITLE = "test"


class GV(arcade.View):
    def __init__(self, speech=None):
        super().__init__()
        self.speech = speech
        self.string = ""
        self.number = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ESCAPE:
            arcade.exit()
        if key > 48 and key < 58:
            print(f"{chr(key)}, {key}")
            self.string += chr(key)
            self.speech.output(self.string)


def main():
    game = arcade.Window(WIDTH, HEIGHT, TITLE)
    speech = Speech()
    screen1 = GV(speech)
    game.show_view(screen1)
    arcade.run()


if __name__ == "__main__":
    main()
