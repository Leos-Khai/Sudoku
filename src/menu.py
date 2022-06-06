import arcade
from screen import View


class MenuItem:
    # Menu items: will be objects added to the Menu class in an array.

    def __init__(self, name: str, action):
        """menu items

        Args:
            name (str): The name of the menu item
            action (func): A callback/action to execute.
        """
        self.name = name
        self.action = action

    def __repr__(self) -> str:
        """return the menu item name

        Returns:
            str: The name of the menu item I.E Load Game.
        """
        return self.name

    def invoke(self):
        """Trigger menu item. I.E Play"""
        self.action()


class Menu(View):
    """The menu class of the menu screen.

    Args:
        View (View): The View object from screen.
    """

    def __init__(self, prior_screen=None):
        super().__init__(prior_screen)
        self.menu_pos = 0
        self.menu_item = []

    def add_item(self, name: str, action):
        """Append a menu item to the list

        Args:
            name (str): Name of the MenuItem
            action (func): The callback that will trigger on invoke.
        """
        self.menu_item.append(MenuItem(name, action))

    def focus_item(self):
        """
        focus_item: Read menu item name

        Will read the associated text of a menu item via TTS.
        """
        self.window.speech.output(f"{self.menu_item[self.menu_pos]}", True)

    def scroll(self, direction):
        """
        scroll

        Scroll menu item up and down

        Args:
            direction (Integer ): Usually +1 or -1 to move up and down from the list. Length of array if home and end key is use to jump to start and end of menu respectively.
        """
        tmp = self.menu_pos + direction
        if tmp < 0:
            tmp = 0
        elif tmp >= len(self.menu_item) - 1:
            tmp = len(self.menu_item) - 1

        if tmp != self.menu_pos:
            self.menu_pos = tmp
            self.focus_item()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP:
            self.scroll(-1)
        elif key == arcade.key.DOWN:
            self.scroll(+1)
        elif key == arcade.key.HOME:
            self.scroll(-len(self.menu_item))
        elif key == arcade.key.END:
            self.scroll(+len(self.menu_item))
        elif key == arcade.key.RETURN:
            self.window.speech.output(f"Trigger {self.menu_item[self.menu_pos]}", True)
            self.menu_item[self.menu_pos].invoke()
