"""
Lucas B. Tinkler
Groupe : 401
Jeu de roche papier ciseaux
"""

import arcade


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Jeu de roche papier ciseaux"

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

    def on_draw(self):
        self.clear()
        title = arcade.Text("Roche, Papier, Ciseaux", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100, arcade.color.RED_BROWN,
                            70, anchor_x="center")
        rules_round_active = arcade.Text("Appuyer sur une image pour faire une attaque!", SCREEN_WIDTH / 2,
                                         SCREEN_HEIGHT - 170, arcade.color.BLIZZARD_BLUE, 40, align="center",
                                         anchor_x="center", multiline=True, width=900)
        pointage_joueur = arcade.Text("Le pointage du joueur est", SCREEN_WIDTH / 4,
                                      SCREEN_HEIGHT - 750, arcade.color.DARK_PASTEL_GREEN, 20,
                                      anchor_x="center")
        pointage_ordinateur = arcade.Text("Le pointage de l'ordinateur est", 740,
                                          SCREEN_HEIGHT - 750, arcade.color.BLIZZARD_BLUE, 20,
                                          anchor_x="center")

        title.draw()
        rules_round_active.draw()
        pointage_joueur.draw()
        pointage_ordinateur.draw()

def main():
    my_game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    arcade.run()


if __name__ == "__main__":
    main()