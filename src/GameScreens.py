from ast import Return
import arcade
from screen import View
from menu import Menu, MenuItem

# import json
# import glob
# import copy
# from random import shuffle
# import numpy


class SudokuBoard(View):
    """The view that going to process Sudoku game"""

    def __init__(self, sudoku_game=None, prior_screen=None):
        super().__init__(prior_screen)
        # self.counter = 0
        # self.path = []
        self.grid_x = 0
        self.grid_y = 0
        self.editable_list = [(0, 0), (1, 1), (2, 2)]
        self.editable = False
        self.tmp_number = 0
        if sudoku_game != None:
            # self.load_sudoku(sudoku_game)
            print("Wait")
        else:
            self.generate_game()

    def generate_game(self):
        # self.grid = [[0 for i in range(9)] for i in range(9)]
        self.grid = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
        ]

    def on_show_view(self):
        # self.window.printtext()
        self.window.speech.output("Welcome to a new game of Sudoku.")

    def on_update(self, delta_time):
        pass

    def focus_grid(self):
        self.window.speech.output(f"{self.grid[self.grid_y][self.grid_x]}")

    def move_grid(self, y, x):
        tmp_x = self.grid_x
        tmp_y = self.grid_y
        ox = self.grid_x
        oy = self.grid_y
        if tmp_x + x < len(self.grid[tmp_y]) and tmp_x + x >= 0:
            # print(f"{len(self.grid[tmp_y])}")
            self.grid_x += x
        if tmp_y + y < len(self.grid) and tmp_y + y >= 0:
            self.grid_y += y
        if self.grid_x != ox or self.grid_y != oy:
            self.focus_grid()

    def on_key_press(self, key, modifiers):
        if self.editable != True:
            if key == arcade.key.UP:
                self.move_grid(-1, 0)
            elif key == arcade.key.DOWN:
                self.move_grid(1, 0)
            elif key == arcade.key.LEFT:
                self.move_grid(0, -1)
            elif key == arcade.key.RIGHT:
                self.move_grid(0, 1)
            elif key == arcade.key.RETURN:
                if (
                    self.editable == False
                    and (self.grid_y, self.grid_x) in self.editable_list
                ):
                    self.editable = True
                    self.window.speech.output("Editing")
        elif self.editable == True:
            if key > 48 and key < 58:
                self.window.speech.output(f"{key}")
                self.tmp_number = chr(key)
                print(self.tmp_number)
                self.editable = False
                print(self.editable)
                self.grid[self.grid_y][self.grid_x] = self.tmp_number
                print(self.grid[self.grid_y][self.grid_x])
                self.tmp_number = 0
                print(self.tmp_number)


"""
    def on_draw(self):
        arcade.start_render()
        for x in range(0, 801, 100):
            arcade.draw_line(x, 0, x, 800, arcade.color.WHITE, 5)
        for y in range(0, 801, 100):
            arcade.draw_line(0, y, 800, y, arcade.color.WHITE, 5)
"""


class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        self.add_item("New game", self.new_game)
        self.add_item("Load game", self.load_game)
        self.add_item("Exit game", self.window.close)

    def new_game(self):
        new_game = SudokuBoard()
        self.window.show_view(new_game)
        print("new game")

    def load_game(self):
        self.window.speech.output("Load game.")
