"""Main menu"""

import pygame
import global_variables as G
from functions import exit_game, text_objects
import sprites
import new_round
import scores


def about_page():
    """The about page of RAstral Rampart"""

    pygame.mixer.music.stop()

    credit_surf_1, credit_rect_1 = text_objects(
        "RAstral Rampart was created by Caleb Werth and",
        G.MEDIUM_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.35),
    )
    credit_surf_2, credit_rect_2 = text_objects(
        "Russell Spry. Original idea by Aaron Werth.",
        G.MEDIUM_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.40),
    )
    instructions_surf, instructions_rect = text_objects(
        "Press space to return to menu",
        G.MEDIUM_TEXT,
        G.WHITE,
        (G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.7),
    )

    pygame_powered = pygame.image.load(
        "assets/pygame_powered.gif"
    ).convert_alpha()
    pygame_powered_rect = pygame_powered.get_rect(
        center=(G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.52)
    )

    G.SCREEN.fill(G.WHITE)
    G.SCREEN.blit(G.BACKGROUND_2.image, G.BACKGROUND_2.rect)
    G.SCREEN.blit(credit_surf_1, credit_rect_1)
    G.SCREEN.blit(credit_surf_2, credit_rect_2)
    G.SCREEN.blit(pygame_powered, pygame_powered_rect)
    G.SCREEN.blit(instructions_surf, instructions_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game_menu()

        pygame.display.update()
        G.CLOCK.tick(15)


def game_menu():
    """The menu for the game"""

    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/audio/bensound-endlessmotion.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    start_button = sprites.Button(
        G.SMALL_TEXT.render("Start", True, G.BLACK),
        ((G.DISPLAY_WIDTH * 0.16), (G.DISPLAY_HEIGHT * 0.65), 100, 50),
        G.GREEN,
        new_round.new_round,
    )
    about_button = sprites.Button(
        G.SMALL_TEXT.render("About", True, G.BLACK),
        ((G.DISPLAY_WIDTH * 0.33), (G.DISPLAY_HEIGHT * 0.5), 100, 50),
        G.LIGHT_YELLOW,
        about_page,
    )
    scores_button = sprites.Button(
        G.SMALL_TEXT.render("Scores", True, G.BLACK),
        ((G.DISPLAY_WIDTH * 0.53), (G.DISPLAY_HEIGHT * 0.5), 100, 50),
        G.GOLD,
        scores.scores_page,
    )
    quit_button = sprites.Button(
        G.SMALL_TEXT.render("Quit", True, G.BLACK),
        ((G.DISPLAY_WIDTH * 0.70), (G.DISPLAY_HEIGHT * 0.65), 100, 50),
        G.RED,
        exit_game,
    )

    text_surf_title, text_rect_title = text_objects(
        "RAstral Rampart",
        G.BIG_TEXT,
        G.WHITE,
        ((G.DISPLAY_WIDTH * 0.5), (G.DISPLAY_HEIGHT * 0.2)),
    )
    text_surf_space, text_rect_space = text_objects(
        "Press Space To Shoot!",
        G.MEDIUM_TEXT,
        G.WHITE,
        ((G.DISPLAY_WIDTH * 0.5), (G.DISPLAY_HEIGHT * 0.32)),
    )

    all_sprites_list = pygame.sprite.Group()
    projectile_list = pygame.sprite.Group()
    buttons_list = pygame.sprite.Group()

    all_sprites_list.add(start_button, about_button, quit_button, scores_button)
    buttons_list.add(start_button, about_button, quit_button, scores_button)

    gun = sprites.Gun((G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.875))
    all_sprites_list.add(gun)

    G.DIFFICULTY = 1
    G.SCORE = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(G.SHOOT_FX)
                    projectile = sprites.Projectile(
                        gun.rect.center,
                        gun.angle,
                        gun.image.get_height() * 0.5,
                    )
                    all_sprites_list.add(projectile)
                    projectile_list.add(projectile)

        all_sprites_list.update()

        for projectile in projectile_list:
            hit_button_list = pygame.sprite.spritecollide(
                projectile, buttons_list, False
            )

            for button in hit_button_list:
                button.function()

            if projectile.off_screen():
                projectile.kill()

        G.SCREEN.fill(G.WHITE)
        G.SCREEN.blit(G.BACKGROUND_2.image, G.BACKGROUND_2.rect)
        G.SCREEN.blit(text_surf_title, text_rect_title)
        G.SCREEN.blit(text_surf_space, text_rect_space)

        all_sprites_list.draw(G.SCREEN)

        pygame.display.update()
        G.CLOCK.tick(60)
