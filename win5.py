import arcade
import synthizer
from src.audio import SoundManager, BufferCache


class WM(arcade.Window):
    def __init__(self, sound_manager):
        super().__init__(800, 800, "Sound")
        self.sound_manager = sound_manager

    def on_show(self):
        self.sound_manager.stream("sound_example/music.mp3", gain=0.2)
        self.sound_manager.stream("sound_example/boop.wav", gain=0.2, looping=False)

    def on_update(self, delta_time: float):
        self.sound_manager.update()


def main():
    with synthizer.initialized():
        ctx = synthizer.Context()
        bc = BufferCache()
        sm = SoundManager(ctx, bc)
        window = WM(sm)
        arcade.run()


if __name__ == "__main__":
    main()
