"""Contains pause screen and unpause screen"""
import pygame
import global_constants as G
from functions import exit_game, text_objects


def unpause():
    """
    Uses global variable
    to unpause
    """
    pygame.mixer.music.unpause()
    G.PAUSE = False


def paused():
    """Pause screen function"""

    pygame.mixer.music.pause()

    pause_surf_1, pause_rect_1 = text_objects(
        "PAUSED",
        G.GIANT_TEXT,
        G.LIGHT_YELLOW,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.35),
    )

    pause_instructions_surf_1, pause_instructions_rect_1 = text_objects(
        "Press 'ESC' to resume",
        G.MEDIUM_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.55),
    )

    pause_instructions_surf_2, pause_instructions_rect_2 = text_objects(
        "Press 'm' to return to menu",
        G.MEDIUM_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.65),
    )

    pause_instructions_surf_3, pause_instructions_rect_3 = text_objects(
        "Press 'q' to quit",
        G.MEDIUM_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.75),
    )

    G.SCREEN.fill(G.WHITE)
    G.SCREEN.blit(G.BACKGROUND_2.image, G.BACKGROUND_2.rect)
    G.SCREEN.blit(pause_surf_1, pause_rect_1)
    G.SCREEN.blit(pause_instructions_surf_1, pause_instructions_rect_1)
    G.SCREEN.blit(pause_instructions_surf_2, pause_instructions_rect_2)
    G.SCREEN.blit(pause_instructions_surf_3, pause_instructions_rect_3)
    pygame.display.update()

    while G.PAUSE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    unpause()
                if event.key == pygame.K_m:
                    game_menu()
                if event.key == pygame.K_q:
                    exit_game()

        G.CLOCK.tick(15)
