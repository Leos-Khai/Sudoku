import arcade
import glob
import json
import os
from decimal import Decimal


class ScreenControl(arcade.Window):
    def __init__(self, width, height, title, speech, sound_manager):
        super().__init__(width, height, title)
        self.view_list = []
        self.speech = speech
        self.sound = sound_manager
        self.music = None
        self.generate_options()

    def on_close(self):
        """Clean up before window closes"""
        try:
            if hasattr(self, "sound"):
                self.sound.destroy_all()
        except Exception as e:
            print(f"Error during window cleanup: {e}")
        super().on_close()

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

    def normalize_position(self, position):
        """Normalize position coordinates for OpenAL 3D audio"""
        if position:
            x, y, z = position
            # Convert from pixel coordinates to normalized OpenAL coordinates
            # OpenAL uses right-handed coordinate system where:
            # +X is right, +Y is up, -Z is towards viewer
            normalized_x = (x - 400) / 400  # Center and normalize to [-1, 1]
            normalized_y = (y - 400) / 400  # Center and normalize to [-1, 1]
            normalized_z = z / 100 if z else 0  # Scale z coordinate
            return (normalized_x, normalized_y, normalized_z)
        return None

    def play_sound(self, path, **kwargs):
        try:
            position = kwargs.pop("position", None)
            if position:
                kwargs["position"] = self.normalize_position(position)
            sound = self.sound.play(path, gain=10 ** (self.sound_volume / 20), **kwargs)
            if not sound:
                print(f"Warning: Failed to play sound {path}")
            return sound
        except Exception as e:
            print(f"Error playing sound {path}: {e}")
            return None

    def stream_music(self, path, **kwargs):
        """Stream music with fallback to WAV format"""
        try:
            if str(self.music) == path:
                return

            # Stop and cleanup previous music if any
            if self.music:
                self.sound.unregister_sound(self.music)
                self.music = None

            # Try to find WAV version if original is not WAV
            if not path.lower().endswith(".wav"):
                wav_path = os.path.join("src", path.rsplit(".", 1)[0] + ".wav")
                if os.path.exists(wav_path):
                    print(f"Using WAV alternative: {wav_path}")
                    path = wav_path
                else:
                    print(
                        f"Note: Music playback requires WAV format. Convert {path} to WAV for audio support."
                    )
                    return None

            # Start new music stream
            self.music = self.sound.stream(
                path, gain=10 ** (self.music_volume / 20), looping=True, **kwargs
            )

            if not self.music:
                print(f"Warning: Failed to stream music {path}")

            return self.music
        except Exception as e:
            print(f"Error streaming music {path}: {e}")
            return None

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()

    def ajust_sound_volume(self, volume):
        try:
            tmpvol = self.sound_volume + volume
            if tmpvol > -60 and tmpvol <= 0:
                self.sound_volume = tmpvol
                volume_percent = abs(int((60 + self.sound_volume) / 60 * 100))
                self.output(f"{volume_percent}%")
                # Play a test sound to demonstrate new volume
                self.play_sound("sounds/board_move.wav")
        except Exception as e:
            print(f"Error adjusting sound volume: {e}")

    def ajust_music_volume(self, volume):
        try:
            tmpvol = self.music_volume + volume
            if tmpvol > -60 and tmpvol <= 0:
                self.music_volume = tmpvol
                if self.music:
                    self.music.volume = 10 ** (self.music_volume / 20)
                volume_percent = abs(int((60 + self.music_volume) / 60 * 100))
                self.output(f"{volume_percent}%")
        except Exception as e:
            print(f"Error adjusting music volume: {e}")

    def on_update(self, delta_time: float):
        self.sound.update()
