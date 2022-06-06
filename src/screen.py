import arcade


class View(arcade.View):
    def __init__(self, prior_screen=None):
        super().__init__()
        self.prior_screen = prior_screen
