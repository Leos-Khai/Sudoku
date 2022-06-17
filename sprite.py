import arcade


class window(arcade.Window):
    def __init__(self):
        super().__init__(800, 800, "Title")
        self.num_sprite = []
        self.sl = arcade.SpriteList()
        for i in range(2, 3):
            self.num_sprite.append(
                arcade.create_text_sprite(
                    str(i), 200+i, 200+i, arcade.color.WHITE, 100, 50
                )
            )
            self.sl.append(self.num_sprite[0])
        print(self.num_sprite)
    def on_draw(self):
        self.sl.draw()
    

def main():
    win = window()
    arcade.run()


if __name__ == "__main__":
    main()
