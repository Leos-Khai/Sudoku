import arcade
from random import choice


class Test(arcade.View):
    def __init__(self):
        super().__init__()
        self.frame = 0
        self.textures = []
        for i in range(10):
            name = str(i)
            image = arcade.create_text_image(
                name, font_size=50, text_color=arcade.color.AERO_BLUE
            )
            self.textures.append(arcade.Texture(name, image=image))

        self.sl = arcade.SpriteList()
        for y in range(9):
            for x in range(9):
                self.sl.append(
                    arcade.Sprite(
                        texture=choice(self.textures),
                        center_x=x * 80 + 75,
                        center_y=y * 80 + 75,
                    )
                )

    def draw_grid(self):
        tmp = 0
        for x in range(9):
            tmp += 1
            if tmp in (4, 7):
                arcade.draw_line(
                    x * 80 + 80, 0, x * 80 + 80, 800, arcade.color.WHITE, 1
                )
            else:
                arcade.draw_line(
                    x * 80 + 80, 0, x * 80 + 80, 800, arcade.color.WHITE, 1
                )
        tmp = 0
        for y in range(9):
            tmp += 1
            if tmp in (4, 7, 10):
                arcade.draw_line(
                    0, y * 80 + 80, 800, y * 80 + 80, arcade.color.WHITE, 1
                )
            else:
                arcade.draw_line(
                    0, y * 80 + 80, 800, y * 80 + 80, arcade.color.WHITE, 1
                )

    def on_draw(self):
        self.clear()
        self.draw_grid()
        self.window.ctx.flush()
        self.sl.draw()

    def on_update(self, delta_time: float):
        self.frame += 1
        if self.frame % 2 == 0:
            for sprite in self.sl:
                sprite.texture = choice(self.textures)


# Test().run()
def main():
    window = arcade.Window(800, 800, "Title")
    view = Test()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
