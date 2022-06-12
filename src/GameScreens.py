from ast import Return
import arcade
from screen import View
from menu import Menu, MenuItem

import copy
from random import shuffle

# import json
# import glob
# import numpy


class SudokuBoard(View):
    """The view that going to process Sudoku game"""

    def __init__(self, sudoku_game=None, prior_screen=None):
        super().__init__(prior_screen)
        self.counter = 0
        self.path = []
        self.grid_x = 0
        self.grid_y = 0
        self.editable_list = []
        self.editable = False
        self.answer = None
        self.save_name = None
        self.completed = False
        if sudoku_game != None:
            # self.load_sudoku(sudoku_game)
            print("Wait")
        else:
            self.generate_game()
            self.generate_editables()

    def generate_editables(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 0:
                    self.editable_list.append((y, x))

    def generate_game(self):
        self.grid = [[0 for i in range(9)] for i in range(9)]
        self.generate_solution(self.grid)
        self.answer = copy.deepcopy(self.grid)
        self.remove_numbers_from_grid()

    def on_show_view(self):
        # self.window.printtext()
        self.window.speech.output("Welcome to a new game of Sudoku.")

    def on_update(self, delta_time):
        pass

    def focus_grid(self):
        if (self.grid_y, self.grid_x) in self.editable_list:
            if self.grid[self.grid_y][self.grid_x] == 0:
                text = f"Empty, editable"
            else:
                text = f"{self.grid[self.grid_y][self.grid_x]}, editable"
        else:
            text = f"{self.grid[self.grid_y][self.grid_x]}"
        grid = self.grid
        number = self.grid[self.grid_y][self.grid_x]
        # grid[self.grid_y][self.grid_x] = 0
        text = f"{text}, {self.valid_location(grid, self.grid_y, self.grid_x, number)}, {self.find_empty_square(grid)}"
        grid[self.grid_y][self.grid_x] = number
        self.window.speech.output(text)

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
            elif key == arcade.key.BACKSPACE:
                if (self.grid_y, self.grid_x) in self.editable_list and self.grid[
                    self.grid_y
                ][self.grid_x] != 0:
                    self.grid[self.grid_y][self.grid_x] = 0
                    self.window.speech.output(f"Removed number")
            elif key == arcade.key.RETURN:
                if (
                    self.editable == False
                    and (self.grid_y, self.grid_x) in self.editable_list
                ):
                    self.editable = True
                    self.window.speech.output("Editing")
        elif self.editable == True:
            if key > 48 and key < 58:
                tmp_number = int(chr(key))
                self.editable = False
                self.grid[self.grid_y][self.grid_x] = tmp_number
                self.focus_grid()

    def on_draw(self):
        self.clear()
        arcade.start_render()
        tmp = 0
        for x in range(0, 800, int(800 / 9)):
            tmp += 1
            if tmp in (4, 7):
                arcade.draw_line(x, 0, x, 800, arcade.color.WHITE, 5)
            else:
                arcade.draw_line(x, 0, x, 800, arcade.color.WHITE, 2)
        tmp = 0
        for y in range(0, 800, int(800 / 9)):
            tmp += 1
            if tmp in (4, 7, 10):
                arcade.draw_line(0, y, 800, y, arcade.color.WHITE, 5)
            else:
                arcade.draw_line(0, y, 800, y, arcade.color.WHITE, 2)
        container = []
        start_y = int(800 - 800 / 9)
        for x in self.grid:
            start_x = 0
            for y in x:
                if y == 0:
                    start_x += int(800 / 9)
                    continue
                tmp = arcade.Text(
                    str(y),
                    start_x,
                    start_y,
                    arcade.color.WHITE,
                    50,
                    int(800 / 9),
                    font_name=(
                        "Times New Roman",
                        "Times",
                    ),
                    align="center",
                )
                container.append(tmp)
                start_x += int(800 / 9)
            start_y -= int(800 / 9)

        for item in container:
            item.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.window.speech.output(f"{x}, {y}")
        print(x)
        print(y)

    def solve_input_sudoku(self):
        """solves a puzzle"""
        self.generate_solution(self.grid)
        return

    def generate_puzzle(self):
        """generates a new puzzle and solves it"""
        self.generate_solution(self.grid)
        self.print_grid("full solution")
        self.remove_numbers_from_grid()
        self.print_grid("with removed numbers")
        return

    def print_grid(self, grid_name=None):
        if grid_name:
            print(grid_name)
        for row in self.grid:
            print(row)
        return

    def test_sudoku(self, grid):
        """tests each square to make sure it is a valid puzzle"""
        for row in range(9):
            for col in range(9):
                num = grid[row][col]
                # remove number from grid to test if it's valid
                grid[row][col] = 0
                if not self.valid_location(grid, row, col, num):
                    return False
                else:
                    # put number back in grid
                    grid[row][col] = num
        return True

    def num_used_in_row(self, grid, row, number):
        """returns True if the number has been used in that row"""
        if number in grid[row]:
            return True
        return False

    def num_used_in_column(self, grid, col, number):
        """returns True if the number has been used in that column"""
        for i in range(9):
            if grid[i][col] == number:
                return True
        return False

    def num_used_in_subgrid(self, grid, row, col, number):
        """returns True if the number has been used in that subgrid/box"""
        sub_row = (row // 3) * 3
        sub_col = (col // 3) * 3
        for i in range(sub_row, (sub_row + 3)):
            for j in range(sub_col, (sub_col + 3)):
                if grid[i][j] == number:
                    return True
        return False

    def valid_location(self, grid, row, col, number):
        """return False if the number has been used in the row, column or subgrid"""
        if self.num_used_in_row(grid, row, number):
            return False
        elif self.num_used_in_column(grid, col, number):
            return False
        elif self.num_used_in_subgrid(grid, row, col, number):
            return False
        return True

    def find_empty_square(self, grid):
        """return the next empty square coordinates in the grid"""
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return

    def solve_puzzle(self, grid):
        """solve the sudoku puzzle with backtracking"""
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            # find next empty cell
            if grid[row][col] == 0:
                for number in range(1, 10):
                    # check that the number hasn't been used in the row/col/subgrid
                    if self.valid_location(grid, row, col, number):
                        grid[row][col] = number
                        if not self.find_empty_square(grid):
                            self.counter += 1
                            break
                        else:
                            if self.solve_puzzle(grid):
                                return True
                break
        grid[row][col] = 0
        return False

    def generate_solution(self, grid):
        """generates a full solution with backtracking"""
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            # find next empty cell
            if grid[row][col] == 0:
                shuffle(number_list)
                for number in number_list:
                    if self.valid_location(grid, row, col, number):
                        self.path.append((number, row, col))
                        grid[row][col] = number
                        if not self.find_empty_square(grid):
                            return True
                        else:
                            if self.generate_solution(grid):
                                # if the grid is full
                                return True
                break
        grid[row][col] = 0
        return False

    def get_non_empty_squares(self, grid):
        """returns a shuffled list of non-empty squares in the puzzle"""
        non_empty_squares = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] != 0:
                    non_empty_squares.append((i, j))
        shuffle(non_empty_squares)
        return non_empty_squares

    def remove_numbers_from_grid(self):
        """remove numbers from the grid to create the puzzle"""
        # get all non-empty squares from the grid
        non_empty_squares = self.get_non_empty_squares(self.grid)
        non_empty_squares_count = len(non_empty_squares)
        rounds = 3
        while rounds > 0 and non_empty_squares_count >= 17:
            # there should be at least 17 clues
            row, col = non_empty_squares.pop()
            non_empty_squares_count -= 1
            # might need to put the square value back if there is more than one solution
            removed_square = self.grid[row][col]
            self.grid[row][col] = 0
            # make a copy of the grid to solve
            grid_copy = copy.deepcopy(self.grid)
            # initialize solutions counter to zero
            self.counter = 0
            self.solve_puzzle(grid_copy)
            # if there is more than one solution, put the last removed cell back into the grid
            if self.counter != 1:
                self.grid[row][col] = removed_square
                non_empty_squares_count += 1
                rounds -= 1
        return


class MainMenu(Menu):
    def __init__(self):
        super().__init__()
        self.add_item("New game", self.new_game)
        self.add_item("Load game", self.load_game)
        self.add_item("Exit game", self.window.close)

    def new_game(self):
        new_game = SudokuBoard()
        self.window.show_view(new_game)

    def load_game(self):
        self.window.speech.output("Load game.")
