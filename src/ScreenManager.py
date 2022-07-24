import arcade
import glob
import json


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
            self.sound_volume = 0.5
            self.music_volume = 0.1
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
        self.sound.play(path, gain=self.sound_volume, **kwargs)

    def stream_music(self, path, **kwargs):
        if str(self.music) == path:
            return
        if self.music == None:
            self.music = self.sound.stream(
                path, gain=self.music_volume, looping=True, **kwargs
            )
        else:
            self.sound.unregister_sound(self.music)
            self.music = self.sound.stream(
                path, gain=self.music_volume, looping=True, **kwargs
            )

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()

    def ajust_sound_volume(self, volume):
        tmpvol = int((self.sound_volume * 100)) + volume
        tmpvol /= 100
        if tmpvol >= 0.01 and tmpvol <= 1.01:
            self.sound_volume = tmpvol
            self.output(f"{int(self.sound_volume*100)}%")

    def ajust_music_volume(self, volume):
        tmpvol = int((self.music_volume * 100)) + volume
        tmpvol /= 100
        if tmpvol >= 0.01 and tmpvol <= 1.01:
            self.music_volume = tmpvol
            self.music.volume = self.music_volume
            self.output(f"{int(self.music_volume*100)}%")

    def on_update(self, delta_time: float):
        self.sound.update()
