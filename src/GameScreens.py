from lzma import MODE_FAST
import arcade
from screen import View
from menu import Menu, MenuItem
from datetime import datetime
import copy
from random import shuffle
import json
import glob
import os
from cryptography.fernet import Fernet



class SudokuBoard(View):
    """The view that going to process Sudoku game"""

    def __init__(self, sudoku_game=None, prior_screen=None):
        super().__init__(prior_screen)
        # variables for sudoku logic.
        self.counter = 0
        self.path = []

        # variables for sprite and graphics.
        self.grid_sprite = arcade.SpriteList()
        self.num_textures = []
        self.num_textures_err = []

        # variable for game logic.
        self.grid = []
        self.grid_x = 0
        self.grid_y = 0
        self.sector_x = self.grid_x // 3 * 3
        self.sector_y = self.grid_y // 3 * 3
        self.editable_list = []
        self.error_list = []
        self.editable = False
        self.typing = None
        self.saving = False
        self.answer = None
        self.save_name = sudoku_game
        self.completed = None

        # variables setting for game difficulty.
        self.warn_duplication = True

        if sudoku_game != None:
            self.generate_sprite()
            self.path_to_save = "data/" + self.save_name + "/"
            self.load_game()
            try:
                self.grid = self.load_data["game_grid"]
                self.answer = self.load_data["completed_grid"]
                self.completed = self.load_data["completed"]
                self.editable_list = self.load_data["editable_list"]
            except:
                print("error")
        else:
            self.generate_sprite()
            self.generate_game()
            self.generate_editables()

    def generate_sprite(self):
        for i in range(0, 10):
            name = str(i)
            image = arcade.create_text_image(name, arcade.color.WHITE, 40)
            if i == 0:
                self.num_textures.append(arcade.Texture.create_empty(name, (50, 50)))
            else:
                self.num_textures.append(arcade.Texture(name, image=image))

        for i in range(0, 10):
            name = str(i)
            name = "E" + name
            image = arcade.create_text_image(name, arcade.color.BRIGHT_PINK, 40)
            if i == 0:
                self.num_textures_err.append(
                    arcade.Texture.create_empty(name, (50, 50))
                )
            else:
                self.num_textures_err.append(arcade.Texture(name, image=image))

        for y in range(720, 0, -80):
            for x in range(80, 800, 80):
                self.grid_sprite.append(
                    arcade.Sprite(
                        texture=self.num_textures[1],
                        center_x=x,
                        center_y=y,
                    )
                )

    def save_game(self):
        if self.save_name == None:
            return

        if not glob.glob("data"):
            os.mkdir("data")

        if not glob.glob("data/" + self.save_name):
            os.mkdir("data/" + self.save_name)

        if not glob.glob("data/" + self.save_name + "/thing.thingy"):
            key = Fernet.generate_key()
            with open("data/" + self.save_name + "/thing.thingy", "wb") as file:
                file.write(key)
        else:
            with open("data/" + self.save_name + "/thing.thingy", "rb") as file:
                key = file.read()

        fernet = Fernet(key)
        save_data = {
            "save_name": self.save_name,
            "game_grid": self.grid,
            "completed_grid": self.answer,
            "editable_list": self.editable_list,
            "completed": self.completed,
        }
        encode = json.dumps(save_data, indent=2).encode("utf-8")
        encrypt = fernet.encrypt(encode)
        with open("data/" + self.save_name + "/save.dat", "wb") as file:
            file.write(encrypt)

    def load_game(self):
        if (
            self.save_name == None
            or not glob.glob(self.path_to_save + "thing.thingy")
            or not glob.glob(self.path_to_save + "save.dat")
        ):
            main = MainMenu()
            self.window.show_view(main)
            return

        try:
            with open(self.path_to_save + "thing.thingy", "rb") as file:
                fernet = Fernet(file.read())
        except FileNotFoundError:
            print("File doesn't exist.")

        try:
            with open(self.path_to_save + "save.dat", "rb") as file:
                self.load_data = json.loads(fernet.decrypt(file.read()))
        except FileNotFoundError:
            print("File not found")

    def generate_editables(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 0:
                    self.editable_list.append([y, x])

    def generate_game(self):
        self.grid = [[0 for i in range(9)] for i in range(9)]
        self.generate_solution(self.grid)
        self.answer = copy.deepcopy(self.grid)
        self.remove_numbers_from_grid()
        self.completed = False

    def on_show_view(self):
        if self.save_name == None:
            text = f"Welcome to Sudoku."
        else:
            text = f"The save file '{self.save_name}' has been loaded. Enjoy your game."
        self.window.speech.output(text, True)
        self.window.stream_music("sounds/game_play.mp3")

    def on_update(self, delta_time):
        i = 0
        for sprite in self.grid_sprite:
            row = i // 9
            col = i % 9
            if [row, col] in self.error_list:
                sprite.texture = self.num_textures_err[self.grid[row][col]]
            else:
                sprite.texture = self.num_textures[self.grid[row][col]]
            i += 1

        if (
            not self.find_empty_square(self.grid)
            and not len(self.error_list) > 0
            and self.completed == False
        ):
            self.completed = True
            victory = WinScreen(self)
            self.window.show_view(victory)

    def generate_error_list(self):
        if self.completed == False:
            self.error_list = []
            try:
                for i in range(81):
                    row = i // 9
                    col = i % 9
                    if (
                        self.verify_square(row, col, self.grid[row][col])
                        and self.grid[row][col] != 0
                        and [row, col] in self.editable_list
                    ):
                        self.error_list.append([row, col])
            except IndexError:
                print("An index error has occured")

    def focus_grid(self):
        if [self.grid_y, self.grid_x] in self.editable_list and self.completed == False:
            if self.grid[self.grid_y][self.grid_x] == 0:
                text = f"Empty, editable"
            else:
                text = f"{self.grid[self.grid_y][self.grid_x]}, editable"
        else:
            text = f"{self.grid[self.grid_y][self.grid_x]}"
        if [self.grid_y, self.grid_x] in self.error_list:
            text = f"{text}, error"
        # grid = self.grid
        number = self.grid[self.grid_y][self.grid_x]
        # grid[self.grid_y][self.grid_x] = 0
        # text = f"{text}, {self.valid_location(grid, self.grid_y, self.grid_x, number)}"
        # grid[self.grid_y][self.grid_x] = number
        self.window.speech.output(text, True)

    def move_grid(self, y, x):
        tmp_x = self.grid_x
        tmp_y = self.grid_y
        ox = self.grid_x
        oy = self.grid_y
        osx = self.sector_x
        osy = self.sector_y

        if tmp_x + x < len(self.grid[tmp_y]) and tmp_x + x >= 0:
            # print(f"{len(self.grid[tmp_y])}")
            self.grid_x += x
            self.sector_x = self.grid_x // 3 * 3
        if tmp_y + y < len(self.grid) and tmp_y + y >= 0:
            self.grid_y += y
            self.sector_y = self.grid_y // 3 * 3
        if self.grid_x != ox or self.grid_y != oy:
            self.window.play_sound(
                "sounds/board_move.wav",
                position=((self.grid_x * 5) - 20, (self.grid_y * -5) + 20, 0),
            )
            self.focus_grid()
        if self.sector_x != osx or self.sector_y != osy:
            self.window.play_sound("sounds/diff_section.wav")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.X:
            self.window.output(f"{self.grid_x+1}, {self.grid_y+1}")
        elif key == arcade.key.Q and modifiers == arcade.key.MOD_ALT:
            # self.focus_grid()
            # print(self.error_list)
            self.grid = copy.deepcopy(self.answer)
            print(self.find_empty_square(self.grid))
        if key == arcade.key.S and modifiers == arcade.key.MOD_CTRL:
            self.saving = True
            if self.save_name != None:
                self.save_game()
                self.window.output("Saving!")
                self.saving = False
            else:
                self.window.output("Type in a save name and press enter to continue.")
                self.window.play_sound("sounds/typing.wav")
        elif self.saving == True:
            if (key >= 97 and key <= 122) or (key >= 48 and key <= 57) or key == 95:
                if self.typing == None:
                    self.typing = chr(key)
                    self.window.play_sound("sounds/single_type.wav")
                else:
                    self.typing += chr(key)
                    self.window.play_sound("sounds/single_type.wav")
            elif key == arcade.key.BACKSPACE:
                if self.typing != None and len(self.typing) > 0:
                    delchar = self.typing[-1]
                    self.typing = self.typing[:-1]
                    self.window.output(delchar)
            elif key == arcade.key.RETURN:
                self.save_name = self.typing
                self.typing = None
                self.save_game()
                self.window.play_sound("sounds/menu_close.wav")
                self.window.output("Generating new save file.")
                self.saving = False

        elif self.editable != True and self.saving != True:
            if key == arcade.key.UP:
                self.move_grid(-1, 0)
            elif key == arcade.key.DOWN:
                self.move_grid(1, 0)
            elif key == arcade.key.LEFT:
                self.move_grid(0, -1)
            elif key == arcade.key.RIGHT:
                self.move_grid(0, 1)
            elif key == arcade.key.BACKSPACE and self.completed == False:
                if [self.grid_y, self.grid_x] in self.editable_list and self.grid[
                    self.grid_y
                ][self.grid_x] != 0:
                    self.grid[self.grid_y][self.grid_x] = 0
                    self.window.play_sound("sounds/number_delete.wav")
                    self.generate_error_list()
                    self.window.speech.output(f"Removed number")
            elif key == arcade.key.RETURN and self.completed == False:
                if (
                    self.editable == False
                    and [self.grid_y, self.grid_x] in self.editable_list
                ):
                    self.editable = True
                    self.window.play_sound("sounds/typing.wav")
                    self.window.speech.output("Editing")
        elif self.editable == True and self.saving != True:
            if key > 48 and key < 58:
                tmp_number = int(chr(key))
                self.editable = False
                self.grid[self.grid_y][self.grid_x] = tmp_number
                self.window.play_sound("sounds/number_input.wav")
                self.generate_error_list()
                self.focus_grid()

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
        # start = datetime.now()
        self.clear()
        self.draw_grid()
        self.window.ctx.flush()
        self.grid_sprite.draw()
        # end = datetime.now()
        # print(end - start)

    """
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.window.speech.output(f"{x}, {y}")
        print(x)
        print(y)
        """

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

    def verify_square(self, row, col, num):
        number = self.grid[row][col]
        self.grid[row][col] = 0
        if self.valid_location(self.grid, row, col, number):
            self.grid[row][col] = number
            return False
        self.grid[row][col] = number
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
        super().__init__(name="Main menu")
        self.add_item("New game", self.new_game)
        self.add_item("Load game", self.load_game)
        self.add_item("Options", self.options)
        self.add_item("Exit game", arcade.exit)

    def on_show_view(self):
        self.window.stream_music("sounds/menu_music.mp3")

    def new_game(self):
        new_game = SudokuBoard()
        self.window.show_view(new_game)

    def load_game(self):
        if len(glob.glob("data/*")) < 1:
            print(glob.glob("data/*"))
            self.window.speech.output("No save files exist.")
            return
        load_game = LoadMenu(self)
        self.window.show_view(load_game)

    def options(self):
        options = OptionsMenu(self)
        self.window.show_view(options)


class LoadMenu(Menu):
    def __init__(self, prior_screen=None):
        super().__init__(name="Load game", prior_screen=prior_screen)
        self.save_dir = "data/"

    def on_show(self):
        if len(glob.glob(self.save_dir)) <= 0:
            self.window.show_view(self.prior_screen)
        self.list_saves()
        super().on_show()

    def list_saves(self):
        self.menu_item = []
        for i in glob.iglob(self.save_dir + "*"):
            self.add_item(os.path.basename(i), self.load)

    def load(self):
        action = LoadOptions(self, self.current_item())
        self.window.show_view(action)


class LoadOptions(Menu):
    def __init__(self, prior_screen, save):
        super().__init__(name="Actions", prior_screen=prior_screen)
        self.save = save
        self.add_item("Load game", self.load)
        self.add_item("Delete save", self.delete)

    def load(self):
        if not glob.glob("data/" + self.save + "/thing.thingy") or not glob.glob(
            "data/" + self.save + "/save.dat"
        ):
            self.window.speech.output("WARNING:: Save has been corrupted.")
            return
        game = SudokuBoard(self.save)
        self.window.show_view(game)

    def delete(self):
        os.remove("data/" + self.save + "/save.dat")
        os.remove("data/" + self.save + "/thing.thingy")
        os.rmdir("data/" + self.save)
        main = MainMenu()
        self.window.show_view(main)


class OptionsMenu(Menu):
    def __init__(self, prior_screen):
        super().__init__(name="Options", prior_screen=prior_screen)
        self.prior_screen = prior_screen
        self.add_item("Sound volume")
        self.add_item("Music volume")
        self.add_item("Save", self.save)

    def save(self):
        self.window.show_view(self.prior_screen)

    def on_hide_view(self):
        self.window.save_options()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            if self.current_item() == "Sound volume":
                self.window.ajust_sound_volume(-5)
                self.window.play_sound("sounds/board_move.wav")
            elif self.current_item() == "Music volume":
                self.window.ajust_music_volume(-5)

        elif key == arcade.key.RIGHT:
            if self.current_item() == "Sound volume":
                self.window.ajust_sound_volume(5)
                self.window.play_sound("sounds/board_move.wav")
            elif self.current_item() == "Music volume":
                self.window.ajust_music_volume(5)
        super().on_key_press(key, key_modifiers)


class PauseMenu(Menu):
    def __init__(self, prior_screen):
        super().__init__(name="Paused", prior_screen=prior_screen)
        self.prior_screen = prior_screen
        self.add_item("Resume game", self.resume)
        self.add_item("Options", self.options)
        self.add_item("Back to main menu", self.main_menu)
        self.add_item("Exit", arcade.exit)


class WinScreen(Menu):
    def __init__(self, prior_screen):
        super().__init__(name="Victory!", prior_screen=None)
        self.prior_screen = prior_screen
        self.add_item(
            "Congradulation you have achieve VICTORY! Do you wish to return to the main menu? Or do you wish to explore the winning board.",
            None,
        )
        self.add_item("Back to main menu.", self.main_menu)
        self.add_item("Back to sudoku board.", self.back_to_board)

    def main_menu(self):
        main = MainMenu()
        self.window.show_view(main)

    def back_to_board(self):
        self.window.show_view(self.prior_screen)
