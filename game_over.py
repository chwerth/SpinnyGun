import pygame
import global_constants as G
from functions import exit_game, text_objects
import game_loop as game
import game_menu as menu


def game_over():
    """Game over screen function"""

    pygame.mixer.music.pause()

    game_over_surf_1, game_over_rect_1 = text_objects(
        "GAME OVER",
        G.GIANT_TEXT,
        G.RED,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.35),
    )
    game_over_surf_2, game_over_rect_2 = text_objects(
        "Press 'p' to play again",
        G.MEDIUM_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.55),
    )

    game_over_surf_3, game_over_rect_3 = text_objects(
        "Press 'm' to return to menu",
        G.MEDIUM_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.65),
    )

    game_over_surf_4, game_over_rect_4 = text_objects(
        "Press 'q' to Quit",
        G.MEDIUM_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.75),
    )

    G.SCREEN.fill(G.WHITE)
    G.SCREEN.blit(G.BACKGROUND_2.image, G.BACKGROUND_2.rect)
    G.SCREEN.blit(game_over_surf_1, game_over_rect_1)
    G.SCREEN.blit(game_over_surf_2, game_over_rect_2)
    G.SCREEN.blit(game_over_surf_3, game_over_rect_3)
    G.SCREEN.blit(game_over_surf_4, game_over_rect_4)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    game.game_loop()
                if event.key == pygame.K_m:
                    menu.game_menu()
                if event.key == pygame.K_q:
                    exit_game()

        G.CLOCK.tick(15)
