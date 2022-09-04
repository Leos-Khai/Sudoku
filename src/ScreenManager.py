import arcade
import glob
import json
from decimal import Decimal


class ScreenControl(arcade.Window):
    def __init__(self, width, height, title, speech, sound_manager):
        super().__init__(width, height, title)
        self.view_list = []
        self.speech = speech
        self.sound = sound_manager
        self.music = None
        self.generate_options()

    def generate_options(self):
        if not glob.glob("options.dat"):
            self.sound_volume = -12
            self.music_volume = -24
            options = {
                "sound_volume": self.sound_volume,
                "music_volume": self.music_volume,
            }
            with open("options.dat", "w") as f:
                json.dump(options, f)
            return
        with open("options.dat", "r") as f:
            data = json.load(f)
        self.sound_volume = data["sound_volume"]
        self.music_volume = data["music_volume"]

    def save_options(self):
        data = {"sound_volume": self.sound_volume, "music_volume": self.music_volume}
        with open("options.dat", "w") as f:
            json.dump(data, f)

    def show(self, view):
        self.view_list.append(view)
        self.show_view(view)

    def output(self, text: str):
        self.speech.output(text, True)

    def play_sound(self, path, **kwargs):
        self.sound.play(path, gain=10 ** (self.sound_volume / 20), **kwargs)

    def stream_music(self, path, **kwargs):
        if str(self.music) == path:
            return
        if self.music == None:
            self.music = self.sound.stream(
                path, gain=10 ** (self.music_volume / 20), looping=True, **kwargs
            )
        else:
            self.sound.unregister_sound(self.music)
            self.music = self.sound.stream(
                path, gain=10 ** (self.music_volume / 20), looping=True, **kwargs
            )

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()

    def ajust_sound_volume(self, volume):
        tmpvol = self.sound_volume + volume
        if tmpvol > -60 and tmpvol <= 0:
            self.sound_volume = tmpvol
            self.output(f"{abs(int((60 + self.sound_volume)/60*100))}%")

    def ajust_music_volume(self, volume):
        tmpvol = self.music_volume + volume
        if tmpvol > -60 and tmpvol <= 0:
            self.music_volume = tmpvol
            self.music.volume = 10 ** (self.music_volume / 20)
            self.output(f"{abs(int((60 + self.music_volume)/60*100))}%")

    def on_update(self, delta_time: float):
        self.sound.update()
