import arcade
import random


class window(arcade.Window):
    def __init__(self):
        super().__init__(800, 800, "Title", True)
        self.num_sprite = []
        self.sudo_sprite = [[None for i in range(9)] for j in range(9)]
        self.sl = arcade.SpriteList()
        self.generate_num()
        print(self.num_sprite)
        # self.sl.append(self.num_sprite[0])
        self.generate_sprite_list()
        self.get_image()
        # print(self.num_sprite[0]._texture)

    def generate_num(self):
        for i in range(0, 9):
            self.num_sprite.append(
                arcade.create_text_sprite(str(i), 0, 0, arcade.color.WHITE, 50, 50)
            )

    def generate_sprite_list(self):
        start_y = int(800 - 800 / 9)
        index = 0
        for x in range(9):
            start_x = (800 / 9) / 2
            for y in range(9):
                tmpspr = arcade.create_text_sprite(
                    str(x),
                    start_x,
                    start_y,
                    arcade.color.WHITE,
                    50,
                    int(800 - 800 / 9),
                )
                self.sudo_sprite[x][y] = tmpspr
                self.sl.insert(index, self.sudo_sprite[x][y])
                start_x += int(800 / 9)
                index += 1
            start_y -= int(800 / 9)

    def get_image(self):
        for i in range(9):
            for j in range(9):
                tmp = random.randint(0, 8)
                self.sudo_sprite[i][j].texture = self.num_sprite[tmp].texture

    def on_draw(self):
        self.sl.draw()


def main():
    win = window()
    arcade.run()


if __name__ == "__main__":
    main()
