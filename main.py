"""
Lucas B. Tinkler
Groupe : 401
Jeu de roche papier ciseaux
"""
# commit didnt wirk
import arcade
from attack_animation import AttackAnimation, AttackType
import game_state
from random import choice


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Jeu de roche papier ciseaux"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.sprite_list_statique = arcade.SpriteList()
        self.sprite_list_dynamique = arcade.SpriteList()
        self.sprite_roche_ordi = arcade.SpriteList()
        self.sprite_papier_ordi = arcade.SpriteList()
        self.sprite_ciseaux_ordi = arcade.SpriteList()
        self.player_sprite = arcade.Sprite("assets/faceBeard.png", 0.3, SCREEN_WIDTH / 4, 300)
        self.ordinateur_sprite = arcade.Sprite("assets/compy.png", 1.5, SCREEN_WIDTH * 0.75, 300)
        self.roche_ordi = arcade.Sprite("assets/srock-attack.png", 1, SCREEN_WIDTH * 0.75, 170)
        self.papier_ordi = arcade.Sprite("assets/spaper.png", 1, SCREEN_WIDTH * 0.75, 170)
        self.ciseaux_ordi = arcade.Sprite("assets/scissors.png", 1, SCREEN_WIDTH * 0.75, 170)
        self.roche_animation = AttackAnimation(AttackType.ROCK)
        self.roche_animation.center_x = SCREEN_WIDTH / 4 - 150
        self.roche_animation.center_y = 170
        self.papier_animation = AttackAnimation(AttackType.PAPER)
        self.papier_animation.center_x = SCREEN_WIDTH / 4
        self.papier_animation.center_y = 170
        self.ciseaux_animation = AttackAnimation(AttackType.SCISSORS)
        self.ciseaux_animation.center_x = SCREEN_WIDTH / 4 + 150
        self.ciseaux_animation.center_y = 170

        self.sprite_list_statique.append(self.player_sprite)
        self.sprite_list_statique.append(self.ordinateur_sprite)
        self.sprite_list_dynamique.append(self.roche_animation)
        self.sprite_list_dynamique.append(self.papier_animation)
        self.sprite_list_dynamique.append(self.ciseaux_animation)
        self.sprite_roche_ordi.append(self.roche_ordi)
        self.sprite_papier_ordi.append(self.papier_ordi)
        self.sprite_ciseaux_ordi.append(self.ciseaux_ordi)

        self.etat_jeu = game_state.GameState.NOT_STARTED
        self.player_points = 0
        self.ordinateur_points = 0
        self.attack_list = [AttackType.ROCK, AttackType.PAPER, AttackType.SCISSORS]
        self.ordinateur_attack_type = ""
        self.player_attack_type = ""
        self.win = "player"

    def on_draw(self):
        self.clear()
        # dessine le texte ------
        title = arcade.Text("Roche, Papier, Ciseaux", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100, arcade.color.RED_BROWN,
                            70, anchor_x="center")
        pointage_joueur = arcade.Text(f"Le pointage du joueur est: {self.player_points}", SCREEN_WIDTH / 4,
                                      70, arcade.color.DARK_PASTEL_GREEN, 20,
                                      anchor_x="center")
        pointage_ordinateur = arcade.Text(f"Le pointage de l'ordinateur est: {self.ordinateur_points}", SCREEN_WIDTH * 0.75,
                                          70, arcade.color.RUSTY_RED, 20,
                                          anchor_x="center")

        title.draw()
        pointage_joueur.draw()
        pointage_ordinateur.draw()

        # dessine les cases ------
        arcade.draw_circle_outline(SCREEN_WIDTH / 4, 170, 70, arcade.color.RED, tilt_angle=45, num_segments=4)
        arcade.draw_circle_outline(SCREEN_WIDTH / 4 - 150, 170, 70, arcade.color.RED, tilt_angle=45, num_segments=4)
        arcade.draw_circle_outline(SCREEN_WIDTH / 4 + 150, 170, 70, arcade.color.RED, tilt_angle=45, num_segments=4)
        arcade.draw_circle_outline(SCREEN_WIDTH * 0.75, 170, 70, arcade.color.RED, tilt_angle=45, num_segments=4)

        # dessine les sprites statiques ------
        self.sprite_list_statique.draw()

        # dessine les sprites qui change ------
        self.sprite_list_dynamique.draw()

        if self.etat_jeu == game_state.GameState.NOT_STARTED:
            rules_not_started = arcade.Text("Appuyer sur une image pour faire une attaque!", SCREEN_WIDTH / 2,
                                             SCREEN_HEIGHT - 170, arcade.color.BLIZZARD_BLUE, 40, align="center",
                                             anchor_x="center", multiline=True, width=900)
            rules_not_started.draw()
        elif self.etat_jeu == game_state.GameState.ROUND_DONE:
            # dessine le type d'attaque de l'ordinateur
            if self.ordinateur_attack_type == AttackType.ROCK:
                self.sprite_roche_ordi.draw()
            elif self.ordinateur_attack_type == AttackType.PAPER:
                self.sprite_papier_ordi.draw()
            elif self.ordinateur_attack_type == AttackType.SCISSORS:
                self.sprite_ciseaux_ordi.draw()

            # dessine qui gagne un point
            if self.win == "player":
                point_to_player = arcade.Text("+1", SCREEN_WIDTH / 4, 400, arcade.color.GREEN, 40, align="center",
                                             anchor_x="center")
                point_to_player.draw()
            elif self.win == "ordi":
                point_to_ordi = arcade.Text("+1", SCREEN_WIDTH * 0.75, 400, arcade.color.RED, 40, align="center",
                                             anchor_x="center")
                point_to_ordi.draw()
            else:
                tie = arcade.Text("Match Null", SCREEN_WIDTH / 2, 450, arcade.color.AZURE, 49, align="center",
                                             anchor_x="center")
                tie.draw()

    def on_update(self, delta_time: float = 1 / 60):
        if self.etat_jeu == game_state.GameState.ROUND_ACTIVE:
            self.ordinateur_attack_type = choice(self.attack_list)
            # détermine qui gagne ou perd un point
            if self.player_attack_type == AttackType.ROCK and self.ordinateur_attack_type == AttackType.PAPER:
                self.ordinateur_points += 1
                self.win = "ordi"
                print("vous avez perdu(e)")
                pass
            elif self.player_attack_type == AttackType.ROCK and self.ordinateur_attack_type == AttackType.SCISSORS:
                self.player_points += 1
                self.win = "player"
                print("vous avez gagné(e)")
                pass
            elif self.player_attack_type == AttackType.PAPER and self.ordinateur_attack_type == AttackType.ROCK:
                self.player_points += 1
                self.win = "player"
                print("vous avez gagné(e)")
                pass
            elif self.player_attack_type == AttackType.PAPER and self.ordinateur_attack_type == AttackType.SCISSORS:
                self.ordinateur_points += 1
                self.win = "ordi"
                print("vous avez perdu(e)")
                pass
            elif self.player_attack_type == AttackType.SCISSORS and self.ordinateur_attack_type == AttackType.ROCK:
                self.ordinateur_points += 1
                self.win = "ordi"
                print("vous avez perdu(e)")
                pass
            elif self.player_attack_type == AttackType.SCISSORS and self.ordinateur_attack_type == AttackType.PAPER:
                self.player_points += 1
                self.win = "player"
                print("vous avez gagné(e)")
                pass
            else:
                self.win = "match null"
                print("match null")
                pass
            self.etat_jeu = game_state.GameState.ROUND_DONE
            self.player_attack_type = ""

    def on_key_press(self, symbol: int, modifiers: int):
        if (self.etat_jeu == game_state.GameState.GAME_OVER
                or self.etat_jeu == game_state.GameState.ROUND_DONE
                and symbol == arcade.key.SPACE):
            self.etat_jeu = game_state.GameState.NOT_STARTED

        print(self.etat_jeu)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if (self.roche_animation.collides_with_point((x, y))
           or self.papier_animation.collides_with_point((x, y))
           or self.ciseaux_animation.collides_with_point((x, y))):
            if self.etat_jeu == game_state.GameState.NOT_STARTED:
                self.etat_jeu = game_state.GameState.ROUND_ACTIVE
                if self.roche_animation.collides_with_point((x, y)):
                    print("vous avez toucher la roche")
                    self.player_attack_type = AttackType.ROCK
                elif self.papier_animation.collides_with_point((x, y)):
                    print("vous avez toucher le papier")
                    self.player_attack_type = AttackType.PAPER
                elif self.ciseaux_animation.collides_with_point((x, y)):
                    print("vous avez toucher les ciseaux")
                    self.player_attack_type = AttackType.SCISSORS


def main():
    my_game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    arcade.run()


if __name__ == "__main__":
    main()