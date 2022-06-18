import arcade
from random import choice


class Test(arcade.Window):
    def __init__(self):
        super().__init__(800, 800, "Title")
        self.frame = 0
        self.textures = []
        for i in range(10):
            name = str(i)
            image = arcade.create_text_image(
                name, font_size=50, text_color=arcade.color.AERO_BLUE
            )
            if i == 0:
                self.textures.append(arcade.Texture.create_empty(name, (50, 50)))
            else:
                self.textures.append(arcade.Texture(name, image=image))
        print(self.textures[0].name)
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

    def on_draw(self):
        self.clear()
        self.sl.draw()

    def on_update(self, delta_time: float):
        self.frame += 1
        if self.frame % 2 == -5:
            for sprite in self.sl:
                sprite.texture = choice(self.textures)


Test().run()
