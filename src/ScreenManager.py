import arcade


class ScreenControl(arcade.Window):
    def __init__(self, width, height, title, speech, sound_manager):
        super().__init__(width, height, title)
        self.view_list = []
        self.speech = speech
        self.sound = sound_manager
        self.sound_volume = 0.5
        self.music_volume = 0.3

    def show(self, view):
        self.view_list.append(view)
        self.show_view(view)

    def output(self, text: str):
        self.speech.output(text, True)

    def play_sound(self, path, **kwargs):
        self.sound.play(path, gain=self.sound_volume, on_finish=print("hi"), **kwargs)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()

    def on_update(self, delta_time: float):
        self.sound.update()
