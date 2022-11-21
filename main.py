import random

import pyxel

LEVEL = [0]


def identify_level_y(lev=None):
    # TODO: Remove this function!
    return 0


# The below function is a tool for simplifying
# the text displays. To use another color/appearance
# configuration, you'll have to do it yourself
def display_text(x, y, msg):
    pyxel.text(x, y, msg, 1)
    pyxel.text(x + 1, y, msg, 7)


# Functions to detect collisions/interactions
# (Some functions are based on work from Pyxel's
# examples, by Takashi Kitao)

SCROLL_BORDER_X = 80
WALL_TILE_X = 4
TILES_FLOOR = [
    (32, 0),
    (32, 8),
    (40, 0),
    (40, 8),
    (48, 0),
    (48, 8),
    (56, 0),
    (56, 8),
]  # Modified, and ignored the fire images for now
TILE_SPAWN1 = (0, 1)
TILE_SPAWN2 = (1, 1)
TILE_SPAWN3 = (2, 1)

scroll_x = 0
player = None
enemies = []


def get_tile(tile_x, tile_y):
    tile_y += identify_level_y(LEVEL[0])
    return pyxel.tilemap(1).pget(tile_x, tile_y)


def detect_collision(x, y, dy):
    x1 = x // 8
    y1 = y // 8
    x2 = (x + 8 - 1) // 8
    y2 = (y + 8 - 1) // 8
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if get_tile(xi, yi)[0] >= WALL_TILE_X:
                return True
    if dy > 0 and y % 8 == 1:
        for xi in range(x1, x2 + 1):
            if get_tile(xi, y1 + 1) in TILES_FLOOR:
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


def is_wall(x, y):
    tile = get_tile(x // 8, y // 8)
    return tile in TILES_FLOOR or tile[0] >= WALL_TILE_X


def cleanup_list(list):
    i = 0
    while i < len(list):
        elem = list[i]
        if elem.is_alive:
            i += 1
        else:
            list.pop(i)


class Diddi:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.r_facing = True
        self.is_falling = False
        self.has_shooter = False
        self.aspects = {
            # [D]eath
            "d": ((0, 8) for i in range(3)),
            # [R]ight-facing
            "r": ((8, 0), (16, 0), (24, 0)),
            # [L]eft-facing
            "l": ((8, 8), (16, 8), (24, 8)),
        }
        self.alive = True

    def update(self):
        global scroll_x
        last_y = self.y
        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx = -2
            self.r_facing = False
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.dx = 2
            self.r_facing = True
        self.dy = min(self.dy + 1, 3)
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.dy = -6
            # pyxel.play(3, 8)
        self.x, self.y, self.dx, self.dy = push_back(self.x, self.y, self.dx, self.dy)
        if self.x < scroll_x:
            self.x = scroll_x
        if self.y < 0:
            self.y = 0
        self.dx = int(self.dx * 0.8)
        self.is_falling = self.y > last_y

        if self.x > scroll_x + SCROLL_BORDER_X:
            last_scroll_x = scroll_x
            scroll_x = min(self.x - SCROLL_BORDER_X, 240 * 8)

    def draw(self):
        if self.is_falling:
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


class App:
    "This will run the game."

    def __init__(self, level=1):
        pyxel.load("resource.pyxres")  # Load our own pyxres to test

        self.level = level
        LEVEL[0] = self.level
        # self.player = Diddi()
        self.winner = False
        self.playing = False

        self.setup_menu()
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.playing:
            self.update_menu()
        else:
            self.update_game()

    def draw(self):
        if not self.playing:
            self.draw_menu()
        else:
            self.draw_game()

    # --- Menu stuff ---
    def setup_menu(self):
        self.playing = False
        self.menu_c = False
        self.menu_g = False

    def update_menu(self):
        if pyxel.btnp(pyxel.KEY_P):
            # [P]lay
            self.setup_game()
        elif pyxel.btnp(pyxel.KEY_G) and not self.menu_c:
            # [G]uide
            self.menu_g = not self.menu_g
        elif pyxel.btnp(pyxel.KEY_C) and not self.menu_g:
            # [C]redits
            self.menu_c = not self.menu_c

    def draw_menu(self):
        pyxel.cls(0)
        # Draw the decorative tilemap
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128, 0)
        if not self.menu_c and not self.menu_g:
            # Display title
            display_text(30, 35, "Abandon the ship!")
            # Display options:
            # [P]lay
            display_text(30, 45, "[P]lay")
            # [G]uide
            display_text(30, 55, "[G]uide")
            # [C]redits
            display_text(30, 65, "[C]redits")
        elif self.menu_g:
            # Display a guide
            display_text(30, 35, "== How to play ==")
            # Diddi's controls
            display_text(30, 45, "Left key - Left")
            display_text(30, 55, "Right key - Right")
            display_text(30, 65, "Space key - Fly")
        elif self.menu_c:
            # Display a small credits sequence
            display_text(30, 35, "== Credits ==")
        # [Q]uit (always available)
        display_text(30, 90, "Press Q to quit")

    # --- Game stuff ---
    def setup_game(self):
        self.playing = True
        self.player = Diddi()

    def update_game(self):
        if pyxel.btn(pyxel.KEY_Q):
            self.game_over()
        self.player.update()
        for enemy in enemies:
            if abs(self.player.x - enemy.x) < 6 and abs(self.player.y - enemy.y) < 6:
                self.game_over()
                return
            enemy.update()
            if enemy.x < scroll_x - 8 or enemy.x > scroll_x + 160 or enemy.y > 160:
                enemy.is_alive = False
        cleanup_list(enemies)

    def draw_game(self):
        pyxel.cls(0)
        pyxel.camera()
        # pyxel.bltm(0, 0, 0, (scroll_x // 4) % 128, 128, 128, 128)
        pyxel.bltm(0, 0, 1, scroll_x, identify_level_y(self.level), 128, 128, 0)
        pyxel.camera(scroll_x, 0)
        self.player.draw()

    def game_over(self):
        # TODO: Get rid of this!
        print("Game Over?")
        pyxel.quit()


if __name__ == "__main__":
    pyxel.init(128, 128, "Abandon the ship! (Internal test 1)")
    App()
