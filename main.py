"""
Lucas B. Tinkler
Groupe : 401
Jeu de roche papier ciseaux
"""
# commit didn't wark
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
        # listes de sprites
        self.sprite_list_statique = arcade.SpriteList()
        self.sprite_attack_player = arcade.SpriteList()
        self.sprite_attack_ordi = arcade.SpriteList()

        # sprites
        self.player_sprite = arcade.Sprite("assets/faceBeard.png", 0.3, SCREEN_WIDTH / 4, 300)
        self.ordinateur_sprite = arcade.Sprite("assets/compy.png", 1.5, SCREEN_WIDTH * 0.75, 300)
        self.roche_ordi = arcade.Sprite("assets/srock-attack.png", 0.5, SCREEN_WIDTH * 0.75, 170)
        self.papier_ordi = arcade.Sprite("assets/spaper.png", 0.5, SCREEN_WIDTH * 0.75, 170)
        self.ciseaux_ordi = arcade.Sprite("assets/scissors.png", 0.5, SCREEN_WIDTH * 0.75, 170)
        # sprites d'animations
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
        self.sprite_attack_player.append(self.roche_animation)
        self.sprite_attack_player.append(self.papier_animation)
        self.sprite_attack_player.append(self.ciseaux_animation)

        self.etat_jeu = game_state.GameState.NOT_STARTED
        self.player_points = 0
        self.ordinateur_points = 0
        self.attack_list = [AttackType.ROCK, AttackType.PAPER, AttackType.SCISSORS]
        self.ordinateur_attack_type = ""
        self.player_attack_type = ""
        self.win = ""
        self.determine = True

    def on_draw(self):
        self.clear()

        self.sprite_attack_player.draw()
        # dessine le texte ------
        title = arcade.Text("Roche, Papier, Ciseaux", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100, arcade.color.RED_BROWN,
                            70, font_name="Handstand", anchor_x="center")
        pointage_joueur = arcade.Text(f"Le pointage du joueur est: {self.player_points}", SCREEN_WIDTH / 4,
                                      70, arcade.color.DARK_PASTEL_GREEN, 19, anchor_x="center",
                                      font_name="Pixelout Personal Use Only")
        pointage_ordinateur = arcade.Text(f"Le pointage de l'ordinateur est: {self.ordinateur_points}",
                                          SCREEN_WIDTH * 0.75, 70, arcade.color.RUSTY_RED, 19, anchor_x="center",
                                          font_name="Pixelout Personal Use Only")

        title.draw()
        pointage_joueur.draw()
        pointage_ordinateur.draw()

        # dessine les cases ------
        arcade.draw_circle_outline(SCREEN_WIDTH / 4, 170, 70, arcade.color.RED, tilt_angle=45, num_segments=4)
        arcade.draw_circle_outline(SCREEN_WIDTH / 4 - 150, 170, 70, arcade.color.RED, tilt_angle=45, num_segments=4)
        arcade.draw_circle_outline(SCREEN_WIDTH / 4 + 150, 170, 70, arcade.color.RED, tilt_angle=45, num_segments=4)
        arcade.draw_circle_outline(SCREEN_WIDTH * 0.75, 170, 70, arcade.color.RED, tilt_angle=45, num_segments=4)

        # déssine les sprites statiques ------
        self.sprite_list_statique.draw()

        if self.etat_jeu == game_state.GameState.NOT_STARTED:
            rules_not_started = arcade.Text("Appuyer sur [Espace] pour commencer la partie", SCREEN_WIDTH / 2,
                                            SCREEN_HEIGHT - 170, arcade.color.BLIZZARD_BLUE, 40,
                                            align="center", anchor_x="center", multiline=True, width=900,
                                            font_name="Pixelout Personal Use Only")
            rules_not_started.draw()

        elif self.etat_jeu == game_state.GameState.ROUND_ACTIVE:
            # dessine les règles
            rules_started = arcade.Text("Appuyer sur une image pour faire une attaque!", SCREEN_WIDTH / 2,
                                        SCREEN_HEIGHT - 170, arcade.color.BLIZZARD_BLUE, 40, align="center",
                                        anchor_x="center", multiline=True, width=900,
                                        font_name="Pixelout Personal Use Only")
            rules_started.draw()

        elif self.etat_jeu == game_state.GameState.ROUND_DONE:
            rules_round_done = arcade.Text("Appuyez sur [Espace] pour lancer la prochaine manche", SCREEN_WIDTH / 2,
                                           SCREEN_HEIGHT - 170, arcade.color.BLIZZARD_BLUE, 40, align="center",
                                           anchor_x="center", multiline=True, width=900,
                                           font_name="Pixelout Personal Use Only")
            rules_round_done.draw()

            # dessine le type d'attaque de l'ordinateur
            self.sprite_attack_ordi.draw()

            # dessine qui gagne un point
            if self.win == "player":
                point_to_player = arcade.Text("+1", SCREEN_WIDTH / 4, 400, arcade.color.GREEN, 40, align="center",
                                              anchor_x="center")
                point_to_player.draw()
            elif self.win == "ordi":
                point_to_ordi = arcade.Text("+1", SCREEN_WIDTH * 0.75, 400, arcade.color.RED, 40, align="center",
                                            anchor_x="center")
                point_to_ordi.draw()
            elif self.win == "match null":
                tie = arcade.Text("Match Nul", SCREEN_WIDTH / 2, 450, arcade.color.AZURE, 49, align="center",
                                  anchor_x="center")
                tie.draw()
            else:
                print("something went wrong")

        elif self.etat_jeu == game_state.GameState.GAME_OVER:
            self.sprite_attack_ordi.clear()

            # montre si le joueur a gagné ou perdu
            game_over = arcade.Text("GAME OVER", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 230, arcade.color.BANANA_MANIA,
                                    80, align="center", bold=True, anchor_x="center",
                                    font_name="Gameplay")
            game_over.draw()
            if self.player_points == 3:
                game_over_win = arcade.Text("Vous avez gagné!", SCREEN_WIDTH / 2, 485, arcade.color.GREEN,
                                            49, align="center", anchor_x="center",
                                            font_name="Pixelout Personal Use Only")
                game_over_win.draw()
            elif self.ordinateur_points == 3:
                game_over_win = arcade.Text("Vous avez perdu", SCREEN_WIDTH / 2, 485, arcade.color.RED,
                                            50, align="center", anchor_x="center",
                                            font_name="Pixelout Personal Use Only")
                game_over_win.draw()

            # dessine la dernière attaque de l'ordinateur
            if self.ordinateur_attack_type == AttackType.ROCK:
                self.sprite_attack_ordi.append(self.roche_ordi)
            elif self.ordinateur_attack_type == AttackType.PAPER:
                self.sprite_attack_ordi.append(self.papier_ordi)
            elif self.ordinateur_attack_type == AttackType.SCISSORS:
                self.sprite_attack_ordi.append(self.ciseaux_ordi)
            self.sprite_attack_ordi.draw()

            # affiche les règles pour lancer une nouvelle partie
            rules_game_over = arcade.Text("Appuyez sur [Espace] pour relancer une partie", SCREEN_WIDTH / 2, 410,
                                          arcade.color.BLIZZARD_BLUE, 40, align="center", anchor_x="center",
                                          multiline=True, width=900, font_name="Pixelout Personal Use Only")
            rules_game_over.draw()

    def on_update(self, delta_time: float = 1 / 60):
        if self.etat_jeu == game_state.GameState.ROUND_ACTIVE:
            # reset les sprites de l'ordi
            self.sprite_attack_ordi.clear()
            self.determine = True

            # fait avancer les animations
            self.roche_animation.on_update()
            self.papier_animation.on_update()
            self.ciseaux_animation.on_update()

        elif self.etat_jeu == game_state.GameState.ROUND_DONE:
            # fait avancer les animations 2
            self.roche_animation.on_update()
            self.papier_animation.on_update()
            self.ciseaux_animation.on_update()

            # détermine qui gagne ou perd un point
            if self.determine:
                self.ordinateur_attack_type = choice(self.attack_list)
                if self.player_attack_type == AttackType.ROCK and self.ordinateur_attack_type == AttackType.PAPER:
                    self.ordinateur_points += 1
                    self.win = "ordi"
                    print("vous avez perdu(e)")

                elif self.player_attack_type == AttackType.ROCK and self.ordinateur_attack_type == AttackType.SCISSORS:
                    self.player_points += 1
                    self.win = "player"
                    print("vous avez gagné(e)")

                elif self.player_attack_type == AttackType.PAPER and self.ordinateur_attack_type == AttackType.ROCK:
                    self.player_points += 1
                    self.win = "player"
                    print("vous avez gagné(e)")

                elif self.player_attack_type == AttackType.PAPER and self.ordinateur_attack_type == AttackType.SCISSORS:
                    self.ordinateur_points += 1
                    self.win = "ordi"
                    print("vous avez perdu(e)")

                elif self.player_attack_type == AttackType.SCISSORS and self.ordinateur_attack_type == AttackType.ROCK:
                    self.ordinateur_points += 1
                    self.win = "ordi"
                    print("vous avez perdu(e)")

                elif self.player_attack_type == AttackType.SCISSORS and self.ordinateur_attack_type == AttackType.PAPER:
                    self.player_points += 1
                    self.win = "player"
                    print("vous avez gagné(e)")

                else:
                    self.win = "match null"
                    print("match null")

                self.determine = False

            self.player_attack_type = ""

            # affiche l'attaque de l'ordi
            if 0 == len(self.sprite_attack_ordi):
                if self.ordinateur_attack_type == AttackType.ROCK:
                    self.sprite_attack_ordi.append(self.roche_ordi)
                elif self.ordinateur_attack_type == AttackType.PAPER:
                    self.sprite_attack_ordi.append(self.papier_ordi)
                elif self.ordinateur_attack_type == AttackType.SCISSORS:
                    self.sprite_attack_ordi.append(self.ciseaux_ordi)
            else:
                pass

            if self.player_points == 3 or self.ordinateur_points == 3:
                self.etat_jeu = game_state.GameState.GAME_OVER

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            if self.etat_jeu == game_state.GameState.NOT_STARTED or self.etat_jeu == game_state.GameState.ROUND_DONE:
                self.etat_jeu = game_state.GameState.ROUND_ACTIVE
            elif self.etat_jeu == game_state.GameState.GAME_OVER:
                self.etat_jeu = game_state.GameState.NOT_STARTED
                self.player_points = 0
                self.ordinateur_points = 0
            else:
                pass
        else:
            pass

        print(self.etat_jeu)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if (self.roche_animation.collides_with_point((x, y))
           or self.papier_animation.collides_with_point((x, y))
           or self.ciseaux_animation.collides_with_point((x, y))):
            if self.etat_jeu == game_state.GameState.ROUND_ACTIVE:
                self.etat_jeu = game_state.GameState.ROUND_DONE
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
