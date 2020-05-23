import pygame
import shelve
import global_variables as G
import os
import game_menu
from functions import text_objects, exit_game


def scores_page():
    pygame.mixer.music.stop()

    page_title_surf, page_title_rect = text_objects(
        "High Scores",
        G.BIG_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.15),
    )

    instructions_surf, instructions_rect = text_objects(
        "Press space to return to menu",
        G.MEDIUM_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.9),
    )

    G.SCREEN.fill(G.WHITE)
    G.SCREEN.blit(G.BACKGROUND_2.image, G.BACKGROUND_2.rect)
    G.SCREEN.blit(page_title_surf, page_title_rect)
    G.SCREEN.blit(instructions_surf, instructions_rect)

    if not os.path.isfile("scores.dat"):
        no_scores_surf, no_scores_rect = text_objects(
            "No Scores Found",
            G.BIG_TEXT,
            G.RED,
            (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.5),
        )
        G.SCREEN.blit(no_scores_surf, no_scores_rect)
    else:
        score_file = shelve.open("scores.dat")
        sorted_records = sorted(
            score_file["scores"], key=lambda k: k["score"], reverse=True
        )
        y_pos = 0.28
        for i, record in enumerate(sorted_records[0:10]):
            record_surf, record_rect = text_objects(
                f"{i+1})  {record['player']}  -  {record['score']}",
                G.SMALL_TEXT,
                G.GOLD,
                (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * y_pos),
            )
            G.SCREEN.blit(record_surf, record_rect)
            y_pos += 0.06
        score_file.close()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game_menu.game_menu()

        pygame.display.update()
        G.CLOCK.tick(15)
