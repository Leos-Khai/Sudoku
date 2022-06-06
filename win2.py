import arcade


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.F:
            arcade.exit()
