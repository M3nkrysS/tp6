"""
Lucas B. Tinkler
Groupe : 401
Jeu de roche papier ciseaux
"""

import arcade
from attack_animation import AttackAnimation, AttackType
import game_state


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Jeu de roche papier ciseaux"

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.sprite_list = arcade.SpriteList()
        self.player_sprite = arcade.Sprite("assets/faceBeard.png", 0.3, SCREEN_WIDTH / 4, 300)
        self.ordinateur_sprite = arcade.Sprite("assets/compy.png", 1.5, SCREEN_WIDTH * 0.75, 300)
        self.roche_animation = AttackAnimation(AttackType.ROCK)
        self.roche_animation.center_x = SCREEN_WIDTH / 4 - 150
        self.roche_animation.center_y = 170
        self.papier_animation = AttackAnimation(AttackType.PAPER)
        self.papier_animation.center_x = SCREEN_WIDTH / 4
        self.papier_animation.center_y = 170
        self.ciseaux_animation = AttackAnimation(AttackType.SCISSORS)
        self.ciseaux_animation.center_x = SCREEN_WIDTH / 4 + 150
        self.ciseaux_animation.center_y = 170

        self.sprite_list.append(self.player_sprite)
        self.sprite_list.append(self.ordinateur_sprite)
        self.sprite_list.append(self.roche_animation)
        self.sprite_list.append(self.papier_animation)
        self.sprite_list.append(self.ciseaux_animation)

        self.etat_jeu = game_state.GameState.NOT_STARTED
        self.player_attack_type = ""

    def on_draw(self):
        self.clear()
        # dessine le texte ------
        title = arcade.Text("Roche, Papier, Ciseaux", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100, arcade.color.RED_BROWN,
                            70, anchor_x="center")
        rules_round_active = arcade.Text("Appuyer sur une image pour faire une attaque!", SCREEN_WIDTH / 2,
                                         SCREEN_HEIGHT - 170, arcade.color.BLIZZARD_BLUE, 40, align="center",
                                         anchor_x="center", multiline=True, width=900)
        pointage_joueur = arcade.Text("Le pointage du joueur est", SCREEN_WIDTH / 4,
                                      70, arcade.color.DARK_PASTEL_GREEN, 20,
                                      anchor_x="center")
        pointage_ordinateur = arcade.Text("Le pointage de l'ordinateur est", SCREEN_WIDTH * 0.75,
                                          70, arcade.color.BLIZZARD_BLUE, 20,
                                          anchor_x="center")

        title.draw()
        rules_round_active.draw()
        pointage_joueur.draw()
        pointage_ordinateur.draw()

        # dessine les cases ------
        arcade.draw_circle_outline(SCREEN_WIDTH / 4, 170, 70, arcade.color.RED, tilt_angle=45, num_segments=4)
        arcade.draw_circle_outline(SCREEN_WIDTH / 4 - 150, 170, 70, arcade.color.RED, tilt_angle=45, num_segments=4)
        arcade.draw_circle_outline(SCREEN_WIDTH / 4 + 150, 170, 70, arcade.color.RED, tilt_angle=45, num_segments=4)
        arcade.draw_circle_outline(SCREEN_WIDTH * 0.75, 170, 70, arcade.color.RED, tilt_angle=45, num_segments=4)

        # dessine les sprites ------
        self.sprite_list.draw()

    def on_update(self, delta_time: float):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        if (self.etat_jeu == game_state.GameState.NOT_STARTED
                or self.etat_jeu == game_state.GameState.GAME_OVER
                or self.etat_jeu == game_state.GameState.ROUND_DONE
                and symbol == arcade.key.SPACE):
            self.etat_jeu = game_state.GameState.ROUND_ACTIVE

        if self.etat_jeu == game_state.GameState.ROUND_ACTIVE:
            pass

        print(self.etat_jeu)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.roche_animation.collides_with_point((x, y)):
            print("vous avez toucher la roche")
            self.player_attack_type = "Rock"
        elif self.papier_animation.collides_with_point((x, y)):
            print("vous avez toucher le papier")
            self.player_attack_type = "Papier"
        elif self.ciseaux_animation.collides_with_point((x, y)):
            print("vous avez toucher les ciseaux")
            self.player_attack_type = "Scisors"


def main():
    my_game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    arcade.run()


if __name__ == "__main__":
    main()