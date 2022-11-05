import pyxel


class App:
    "The main class that puts everything together."

    def __init__(self):
        pyxel.load("resource.pyxres")
        self.startup()

    def startup(self):
        pyxel.run(self.update, self.run)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pass


if __name__ == '__main__':
    pyxel.init(180, 180, title="Abandon the ship!")
    App()
