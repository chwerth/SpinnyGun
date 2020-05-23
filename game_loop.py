"""Main game loop"""

import random
import pygame
import global_variables as G
import sprites
from functions import exit_game, text_objects
import paused
import game_over
import new_round
from hud import Hud


class Player(object):
    """Class for holding player information"""

    def __init__(self):
        # Currently we only keep track of the player's health
        # Will add more attributes as needed
        self.health = 10
        self.score = 0
        self.max_ammo = 10
        self.ammo = self.max_ammo
        self.reload_duration = 3
        self.reload_start_time = 0

    def update_health(self, health_change):
        """Adds health_change to health attribute"""
        self.health += health_change

    def update_score(self, score_change):
        """Adds score_change to score attribute"""
        self.score += score_change

    def reload(self):
        """Fills up the players ammo again"""
        self.ammo = self.max_ammo

    def pew(self):
        """Fire the gun"""
        self.ammo -= 1

    def time_to_reload(self, game_time):
        """Check if it's time to reload"""

        return (
            self.ammo == 0
            and game_time - self.reload_start_time > self.reload_duration
        )


def game_loop():
    """The main game loop"""

    # This is for the in-game background music
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/audio/electric_jazz.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    all_sprites_list = pygame.sprite.Group()
    missile_list = pygame.sprite.Group()
    projectile_list = pygame.sprite.Group()

    random.seed()
    missiles_to_spawn = random.choices(
        [1, 2, 3], weights=[1, 2, 3], k=(G.DIFFICULTY * 10)
    )

    player = Player()
    gun = sprites.Gun((G.DISPLAY_WIDTH * 0.5, G.DISPLAY_HEIGHT * 0.875))
    all_sprites_list.add(gun)

    hud = Hud(player.health, player.score, player.ammo)

    delta_t = 0
    game_time = 0

    while True:

        # Add last iteration's time to running game_time
        game_time += delta_t

        # Creates scoreboard

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            # Fire a projectile if the player presses and releases space
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and player.ammo > 0:
                    player.pew()
                    if player.ammo == 0:
                        player.reload_start_time = game_time
                    pygame.mixer.Sound.play(G.SHOOT_FX)
                    projectile = sprites.Projectile(
                        gun.rect.center,
                        gun.angle,
                        gun.image.get_height() * 0.5,
                    )
                    all_sprites_list.add(projectile)
                    projectile_list.add(projectile)
                if event.key == pygame.K_ESCAPE:
                    G.PAUSE = True
                    paused.paused()

        # Reload
        if player.time_to_reload(game_time):
            player.reload()

        if random.randrange(150 // G.DIFFICULTY) == 0:
            if missiles_to_spawn:
                missile_type = missiles_to_spawn.pop(0)
                new_missile = sprites.Missile(
                    (random.randrange(G.DISPLAY_WIDTH), -600), missile_type
                )
                all_sprites_list.add(new_missile)
                missile_list.add(new_missile)

        all_sprites_list.update()

        for projectile in projectile_list:
            hit_missile_list = pygame.sprite.spritecollide(
                projectile, missile_list, True
            )
            for hit_missile in hit_missile_list:
                all_sprites_list.add(
                    sprites.Missile_Explosion(
                        hit_missile.rect.center, hit_missile.missile_type
                    )
                )
                pygame.mixer.Sound.play(G.EXPLOSION_FX)
                projectile.kill()
                player.update_score(1)

            if projectile.off_screen():
                projectile.kill()

        for missile in missile_list:
            if missile.off_screen():
                missile.kill()
                all_sprites_list.add(
                    sprites.Missile_Explosion(
                        missile.rect.center, missile.missile_type
                    )
                )
                pygame.mixer.Sound.play(G.EXPLOSION_FX)
                player.update_health(missile.stats["damage"])
                if player.health <= 0:
                    game_over.game_over()

        # Paint the background G.WHITE
        G.SCREEN.fill(G.WHITE)
        G.SCREEN.blit(G.BACKGROUND_1.image, G.BACKGROUND_1.rect)
        hud.draw_hud(player.score, player.ammo, player.health)

        # Draw all sprites
        all_sprites_list.draw(G.SCREEN)

        # Move all background changes to the foreground
        pygame.display.update()

        # Store time since last tick in seconds
        delta_t = G.CLOCK.tick(60) / 1000

        if not missiles_to_spawn and not missile_list:
            G.DIFFICULTY += 1
            new_round.new_round()
