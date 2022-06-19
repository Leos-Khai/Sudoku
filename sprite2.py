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

    def draw_grid(self):
        listp = []
        tmpx = 40
        tmpy = 760
        for x in range(11):
            listp.append([tmpx, tmpy])
            listp.append([tmpx, 40])
            tmpx += 80
        for y in range(11):
            listp.append([40, tmpy])
            listp.append([760, tmpy])
            tmpy -= 80
        arcade.draw_lines(
            listp,
            arcade.color.WHITE,
            2,
        )
        listp2 = [
            [40, 760],
            [40, 40],
            [280, 760],
            [280, 40],
            [520, 760],
            [520, 40],
            [760, 760],
            [760, 40],
            [40, 760],
            [760, 760],
            [40, 520],
            [760, 520],
            [40, 280],
            [760, 280],
            [40, 40],
            [760, 40],
        ]

        arcade.draw_lines(
            listp2,
            arcade.color.WHITE,
            5,
        )

    def on_draw(self):
        self.clear()
        self.draw_grid()
        # self.sl.draw()

    def on_update(self, delta_time: float):
        self.frame += 1
        if self.frame % 2 == 0:
            for sprite in self.sl:
                sprite.texture = choice(self.textures)
                # print(self.sl.index(sprite))


Test().run()
