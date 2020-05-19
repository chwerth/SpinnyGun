import pygame
import global_variables as G
import game_loop as game
from functions import text_objects


def new_round():
    pygame.mixer.music.stop()

    round_surf, round_rect = text_objects(
        f"ROUND {G.DIFFICULTY}",
        G.GIANT_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.5),
    )

    G.SCREEN.fill(G.WHITE)
    G.SCREEN.blit(G.BACKGROUND_2.image, G.BACKGROUND_2.rect)
    G.SCREEN.blit(round_surf, round_rect)
    pygame.display.update()

    pygame.time.delay(2500)
    game.game_loop()
