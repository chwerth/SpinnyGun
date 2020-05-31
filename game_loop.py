"""Main game loop"""

import random
import pygame
import global_variables as G
import sprites
from functions import exit_game, text_objects, fib
import paused
import game_over
import new_round
from hud import Hud


class Player(object):
    """Class for holding player information"""

    def __init__(self):
        self.max_health = 10 + G.PERMANENT_POWER_UPS["higher_max_health"]
        self.health = self.max_health
        self.max_ammo = 10 + G.PERMANENT_POWER_UPS["higher_max_ammo"]
        self.ammo = self.max_ammo
        self.score = 0
        self.reload_duration = 2.5
        self.reload_start_time = 0
        self.piercing_rounds = False
        self.piercing_rounds_start_time = 0
        self.piercing_rounds_duration = 10
        self.fan_of_projectiles = False
        self.fan_of_projectiles_start_time = 0
        self.fan_of_projectiles_duration = 10

    def update_health(self, health_change):
        """Adds health_change to health attribute"""
        self.health += health_change

    def update_ammo(self, ammo_change):
        """Update ammo"""
        self.ammo += ammo_change

    def reload(self):
        """Fills up the players ammo again"""
        self.ammo = self.max_ammo

    def time_to_reload(self, game_time):
        """Check if it's time to reload"""

        return (
            self.ammo == 0
            and game_time - self.reload_start_time > self.reload_duration
        )

    def time_to_piercing_rounds_expire(self, game_time):
        """Check if it's time to let piercing rounds expire"""

        return (
            game_time - self.piercing_rounds_start_time
            > self.piercing_rounds_duration
        )

    def time_to_fan_expire(self, game_time):
        """Check if it's time to let fan of projectiles expire"""

        return (
            game_time - self.fan_of_projectiles_start_time
            > self.fan_of_projectiles_duration
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
    power_up_list = pygame.sprite.Group()

    random.seed()
    missiles_to_spawn = random.choices(
        [1, 2, 3], weights=[1, 2, 3], k=(fib(G.DIFFICULTY + 5))
    )

    power_ups_to_spawn = random.choices(
        sprites.Power_Up.power_up_list,
        weights=[1, 1, 1, 1],
        k=random.randrange(2, 7),
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            # Fire a projectile if the player presses and releases space
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and player.ammo > 0:
                    player.update_ammo(-1)
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
                    if player.fan_of_projectiles:
                        left_projectile = sprites.Projectile(
                            gun.rect.center,
                            gun.angle + 10,
                            gun.image.get_height() * 0.5,
                        )
                        right_projectile = sprites.Projectile(
                            gun.rect.center,
                            gun.angle - 10,
                            gun.image.get_height() * 0.5,
                        )
                        all_sprites_list.add(left_projectile, right_projectile)
                        projectile_list.add(left_projectile, right_projectile)

                if event.key == pygame.K_ESCAPE:
                    G.PAUSE = True
                    paused.paused()

        # Reload
        if player.time_to_reload(game_time):
            player.reload()

        if player.time_to_piercing_rounds_expire(game_time):
            player.piercing_rounds = False

        if player.time_to_fan_expire(game_time):
            player.fan_of_projectiles = False

        if (
            random.randrange(700 // (5 + G.DIFFICULTY)) == 0
            and missiles_to_spawn
        ):
            missile_type = missiles_to_spawn.pop(0)
            new_missile = sprites.Missile(
                (random.randrange(G.DISPLAY_WIDTH), -600), missile_type
            )
            all_sprites_list.add(new_missile)
            missile_list.add(new_missile)

        if random.randrange(500) == 0 and power_ups_to_spawn:
            power_up = power_ups_to_spawn.pop(0)
            new_power_up_sprite = sprites.Power_Up(
                (
                    random.randrange(
                        G.DISPLAY_WIDTH * 0.125, G.DISPLAY_WIDTH * 0.875
                    ),
                    random.randrange(
                        G.DISPLAY_WIDTH * 0.125, G.DISPLAY_HEIGHT * 0.625
                    ),
                ),
                power_up,
            )
            all_sprites_list.add(new_power_up_sprite)
            power_up_list.add(new_power_up_sprite)

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
                if not player.piercing_rounds:
                    projectile.kill()
                G.SCORE += hit_missile.stats["points"]

            hit_power_up_list = pygame.sprite.spritecollide(
                projectile, power_up_list, True
            )
            for hit_power_up in hit_power_up_list:
                pygame.mixer.Sound.play(random.choice(G.POWER_UP_FX_LIST))
                if not hit_power_up.power_up["temporary"]:
                    G.PERMANENT_POWER_UPS[hit_power_up.power_up["type"]] += 1
                if hit_power_up.power_up["type"] == "higher_max_health":
                    player.update_health(1)
                elif hit_power_up.power_up["type"] == "higher_max_ammo":
                    if player.ammo >= 1:
                        player.update_ammo(1)
                    player.max_ammo += 1
                elif hit_power_up.power_up["type"] == "piercing_rounds":
                    player.piercing_rounds = True
                    player.piercing_rounds_start_time = game_time
                elif hit_power_up.power_up["type"] == "fan_of_projectiles":
                    player.fan_of_projectiles = True
                    player.fan_of_projectiles_start_time = game_time

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
        hud.draw_hud(G.SCORE, player.ammo, player.health)

        # Draw all sprites
        all_sprites_list.draw(G.SCREEN)

        # Move all background changes to the foreground
        pygame.display.update()

        # Store time since last tick in seconds
        delta_t = G.CLOCK.tick(60) / 1000

        if not missiles_to_spawn and not missile_list:
            G.DIFFICULTY += 1
            new_round.new_round()
