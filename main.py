import random

import pyxel

# Variables that help us identify certain
# elements (set up without any class, so
# they can be accessed anywhere)
FLOOR_IMAGES = ((32, 0), (32, 8), (40, 0), (40, 8), (48, 0), (48, 8), (56, 0), (56, 8))
FIRE_IMAGES = ((0, 16), (0, 24), (8, 16), (8, 24))
TRANSPARENT_COLOR = 0

# Functions to detect collisions/interactions
# (Some functions are based on work from Pyxel's
# examples, by Takashi Kitao)
SCROLL_BORDER_X = 80
WALL_TILE_X = 4


def prepare_coords(x, y):
    x1 = x // 8
    y1 = y // 8
    x2 = (x + 8 - 1) // 8
    y2 = (y + 8 - 1) // 8
    return x1, x2, y1, y2


def get_tile(tile_x, tile_y):
    return pyxel.tilemap(0).pget(tile_x, tile_y)


def detect_collision(x, y, dy):
    "Check if you hit with something."
    x1, x2, y1, y2 = prepare_coords(x, y)
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if get_tile(xi, yi)[0] >= WALL_TILE_X:
                return True
    if dy > 0 and y % 8 == 1:
        for xi in range(x1, x2 + 1):
            if get_tile(xi, y1 + 1) in FLOOR_IMAGES:
                return True
    return False


def push_back(x, y, dx, dy):
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    if abs_dx > abs_dy:
        sign = 1 if dx > 0 else -1
        for _ in range(abs_dx):
            if detect_collision(x + sign, y, dy):
                break
            x += sign
        sign = 1 if dy > 0 else -1
        for _ in range(abs_dy):
            if detect_collision(x, y + sign, dy):
                break
            y += sign
    else:
        sign = 1 if dy > 0 else -1
        for _ in range(abs_dy):
            if detect_collision(x, y + sign, dy):
                break
            y += sign
        sign = 1 if dx > 0 else -1
        for _ in range(abs_dx):
            if detect_collision(x + sign, y, dy):
                break
            x += sign
    return x, y, dx, dy


# Diddi class
class Diddi:
    "The hero of this game."

    def __init__(self):
        # Coordinates
        self.x, self.y, self.dx, self.dy = 0, 0, 0, 0
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
        self.alive = True
        self.falling = False
        self.r_facing = True  # True = right, False = left
        self.size = 8
        self.scroll_x = 0

    def update(self):
        last_y = self.y
        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx = -2
            self.r_facing = False
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.dx = 2
            self.r_facing = True

        self.dy = min(self.dy + 1, 3)
        self.x, self.y, self.dx, self.dy = push_back(self.x, self.y, self.dx, self.dy)
        if self.x < self.scroll_x:
            self.x = self.scroll_x
        if self.y < 0:
            self.y = 0
        self.dx = int(self.dx * 0.8)
        self.falling = self.y > last_y

        if self.x > self.scroll_x + SCROLL_BORDER_X:
            last_scroll_x = self.scroll_x
            self.scroll_x = min(self.x - SCROLL_BORDER_X, 240 * 8)

    def draw(self):
        if self.falling:
            situation = 2
        else:
            situation = random.choice([0, 1])
        if not self.alive:
            face = "d"
        elif self.r_facing:
            face = "r"
        else:
            face = "l"
        img_x, img_y = self.aspects[face][situation]
        pyxel.blt(self.x, self.y, 0, img_x, img_y, 8, 8, 0)


# Main app class
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
        pyxel.cls(0)

    # Game functions

    def setup_game(self):
        self.playing = True
        self.game_hero = Diddi()

    def update_game(self):
        self.game_hero.update()

    def draw_game(self):
        pyxel.cls(0)
        self.game_hero.draw()


if __name__ == "__main__":
    # Initialize Pyxel here, not before!
    pyxel.init(110, 110, title="Abandon the ship!")
    # Call the App() class, which will make all the job
    App()
