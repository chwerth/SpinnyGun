import pygame
import global_variables as G
from functions import text_objects


class Hud(object):
    def __init__(self, health, score, ammo):
        self.health = health
        self.score = score
        self.image = pygame.image.load("assets/gun_icon.png").convert_alpha()
        self.ammo_text = G.SMALL_TEXT

    def draw_health(self, health):
        for i in range(health):
            img_rect = self.image.get_rect(
                center=(
                    G.DISPLAY_WIDTH - (30 * (i + 1)),
                    G.DISPLAY_HEIGHT * 0.97,
                )
            )
            G.SCREEN.blit(self.image, img_rect)

    def draw_score(self, score):
        scoreboard_surf, scoreboard_rect = text_objects(
            "Score: " + str(score),
            G.SMALL_TEXT,
            G.WHITE,
            ((G.DISPLAY_WIDTH * 0.065), (G.DISPLAY_HEIGHT * 0.025)),
        )
        G.SCREEN.blit(scoreboard_surf, scoreboard_rect)

    def draw_ammo(self, ammo):
        if ammo == 0:
            ammo_status = "Reloading"
            self.ammo_text = G.SMALL_ITALIC_TEXT
        else:
            ammo_status = str(ammo)
            self.ammo_text = G.SMALL_TEXT
        ammo_surf, ammo_rect = text_objects(
            "Ammo: " + ammo_status,
            self.ammo_text,
            G.WHITE,
            ((G.DISPLAY_WIDTH * 0.87), (G.DISPLAY_HEIGHT * 0.93)),
        )
        G.SCREEN.blit(ammo_surf, ammo_rect)

    def draw_controls(self):
        control_surf, control_rect = text_objects(
            "Press 'SPACE' to Fire!",
            G.TINY_TEXT,
            G.WHITE,
            ((G.DISPLAY_WIDTH * 0.11), (G.DISPLAY_HEIGHT * 0.97)),
        )
        G.SCREEN.blit(control_surf, control_rect)

    def draw_controls2(self):
        control_surf, control_rect = text_objects(
            "Press 'ESC' to Pause!",
            G.TINY_TEXT,
            G.WHITE,
            ((G.DISPLAY_WIDTH * 0.109), (G.DISPLAY_HEIGHT * 0.94)),
        )
        G.SCREEN.blit(control_surf, control_rect)

    def draw_hud(self, score, ammo, health):
        self.draw_score(score)
        self.draw_ammo(ammo)
        self.draw_controls()
        self.draw_controls2()
        self.draw_health(health)
