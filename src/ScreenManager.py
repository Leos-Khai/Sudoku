import arcade
from screen import View


class ScreenControl(arcade.Window):
    def __init__(self, width, height, title, speech=None):
        super().__init__(width, height, title)
        self.view_list = []
        self.speech = speech

    def show(self, view):
        self.view_list.append(view)
        self.show_view(view)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            self.close()
