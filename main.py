import pyxel


class Diddi:
    "The hero of this game."

    def __init__(self):
        # Coordinates
        self.x, self.y = 0, 0
        # The position of each aspect,
        # ordered by situation
        self.aspects = {
            # [D]eath
            "d": ((0, 8) for i in range(3)),
            # [R]ight-facing
            "r": ((8, 0), (16, 0), (24, 0)),
            # [L]eft-facing
            "l": ((8, 8), (16, 8), (24, 8)),
        }
        self.size = 8

    def update(self):
        pass

    def draw(self):
        pass


class App:
    "The main class that puts everything together."

    # Main functions (and misc tools)

    def __init__(self):
        pyxel.load("resource.pyxres")
        self.startup()

    def startup(self):
        self.setup_menu()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if not self.playing:
            self.update_menu()
        else:
            self.update_game()

    def draw(self):
        if not self.playing:
            self.draw_menu()
        else:
            self.draw_game()

    # Menu functions

    def setup_menu(self):
        self.playing = False

    def update_menu(self):
        pass

    def draw_menu(self):
        pass

    # Game functions

    def setup_game(self):
        self.playing = True
        self.game_hero = Diddi()

    def update_game(self):
        pass

    def draw_game(self):
        pass


if __name__ == '__main__':
    # Initialize Pyxel here, not before!
    pyxel.init(180, 180, title="Abandon the ship!")
    # Call the App() class, which will make all the job
    App()
