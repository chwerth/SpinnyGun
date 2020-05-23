"""Game over screen"""

import pygame
import global_variables as G
from functions import exit_game, text_objects
import new_round
import game_menu as menu
from names import NAMES
import json
import os
import random


def game_over():
    """Game over screen function"""

    player_name = random.choice(NAMES)
    final_score = G.SCORE * G.DIFFICULTY
    score_entry = {"player": player_name, "score": final_score}
    G.SCORE = 0

    if os.path.isfile("scores.json"):
        with open('scores.json', 'r') as scores_file:
            score_data = json.load(scores_file)
            score_data['scores'].append(score_entry)

        with open('scores.json', 'w') as scores_file:
            json.dump(score_data, scores_file)


    else:
        score_data = {}
        score_data['scores'] = []
        score_data['scores'].append(score_entry)
        with open('scores.json', 'w') as scores_file:
            json.dump(score_data, scores_file)

    pygame.mixer.music.pause()

    game_over_surf_1, game_over_rect_1 = text_objects(
        "GAME OVER",
        G.GIANT_TEXT,
        G.RED,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.25),
    )
    player_name_surf, player_name_rect = text_objects(
        f"Thanks for playing, {player_name}!",
        G.MEDIUM_TEXT,
        G.LIGHT_YELLOW,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.40),
    )
    player_score_surf, player_score_rect = text_objects(
        f"Final Score: {final_score}",
        G.MEDIUM_TEXT,
        G.LIGHT_YELLOW,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.46),
    )
    game_over_surf_2, game_over_rect_2 = text_objects(
        "Press 'p' to play again",
        G.MEDIUM_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.60),
    )

    game_over_surf_3, game_over_rect_3 = text_objects(
        "Press 'm' to return to menu",
        G.MEDIUM_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.70),
    )

    game_over_surf_4, game_over_rect_4 = text_objects(
        "Press 'q' to Quit",
        G.MEDIUM_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.80),
    )

    G.SCREEN.fill(G.WHITE)
    G.SCREEN.blit(G.BACKGROUND_2.image, G.BACKGROUND_2.rect)
    G.SCREEN.blit(game_over_surf_1, game_over_rect_1)
    G.SCREEN.blit(player_name_surf, player_name_rect)
    G.SCREEN.blit(player_score_surf, player_score_rect)
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
                    G.DIFFICULTY = 1
                    new_round.new_round()
                if event.key == pygame.K_m:
                    menu.game_menu()
                if event.key == pygame.K_q:
                    exit_game()

        G.CLOCK.tick(15)
