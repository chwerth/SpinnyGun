"""This file currently contains all the RAstral Rampart code"""
import random
from math import cos, sin, radians
import sys
import pygame  # pylint: disable=import-error

# Screen width and height
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

# Colors
BLACK = (0, 0, 0)
BLUE = (23, 212, 252)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_YELLOW = (247, 241, 49)

# Difficulty setting
DIFFICULTY = 1

# Pause
PAUSE = False

# Initializing
pygame.mixer.pre_init(22100, -16, 2, 64)
pygame.init()
random.seed()
SCREEN = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Spinny Gun")
ICON = pygame.image.load("assets/gun_icon.png").convert_alpha()
pygame.display.set_icon(ICON)
CLOCK = pygame.time.Clock()

# Text
GIANT_TEXT = pygame.font.Font("freesansbold.ttf", 115)
BIG_TEXT = pygame.font.Font("freesansbold.ttf", 80)
MEDIUM_TEXT = pygame.font.Font("freesansbold.ttf", 30)
SMALL_TEXT = pygame.font.Font("freesansbold.ttf", 20)

# Sound Effects
SHOOT_FX = pygame.mixer.Sound("assets/audio/laser.wav")
EXPLOSION_FX = pygame.mixer.Sound("assets/audio/explosion.wav")


def exit_game():
    """Exits the game"""
    pygame.quit()
    sys.exit()


def rot_center(image, rect, angle):
    """Rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


def text_objects(text, font, color, pos):
    """Return text surface and rect"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    return text_surface, text_rect


def game_over():
    """Game over screen function"""

    pygame.mixer.music.pause()

    game_over_surf_1, game_over_rect_1 = text_objects(
        "GAME OVER",
        GIANT_TEXT,
        RED,
        (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.35),
    )
    game_over_surf_2, game_over_rect_2 = text_objects(
        "Press 'p' to play again",
        MEDIUM_TEXT,
        WHITE,
        (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.55),
    )

    game_over_surf_3, game_over_rect_3 = text_objects(
        "Press 'm' to return to menu",
        MEDIUM_TEXT,
        WHITE,
        (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.65),
    )

    game_over_surf_4, game_over_rect_4 = text_objects(
        "Press 'q' to Quit",
        MEDIUM_TEXT,
        WHITE,
        (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.75),
    )

    SCREEN.fill(WHITE)
    SCREEN.blit(BACKGROUND_2.image, BACKGROUND_2.rect)
    SCREEN.blit(game_over_surf_1, game_over_rect_1)
    SCREEN.blit(game_over_surf_2, game_over_rect_2)
    SCREEN.blit(game_over_surf_3, game_over_rect_3)
    SCREEN.blit(game_over_surf_4, game_over_rect_4)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    game_loop()
                if event.key == pygame.K_m:
                    game_menu()
                if event.key == pygame.K_q:
                    exit_game()

        CLOCK.tick(15)


def unpause():
    """
    Uses global variable
    to unpause
    """
    global PAUSE  # pylint: disable=global-statement
    pygame.mixer.music.unpause()
    PAUSE = False


def paused():
    """Pause screen function"""

    pygame.mixer.music.pause()

    pause_surf_1, pause_rect_1 = text_objects(
        "PAUSED",
        GIANT_TEXT,
        LIGHT_YELLOW,
        (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.35),
    )

    pause_instructions_surf_1, pause_instructions_rect_1 = text_objects(
        "Press 'ESC' to resume",
        MEDIUM_TEXT,
        WHITE,
        (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.55),
    )

    pause_instructions_surf_2, pause_instructions_rect_2 = text_objects(
        "Press 'm' to return to menu",
        MEDIUM_TEXT,
        WHITE,
        (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.65),
    )

    pause_instructions_surf_3, pause_instructions_rect_3 = text_objects(
        "Press 'q' to quit",
        MEDIUM_TEXT,
        WHITE,
        (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.75),
    )

    SCREEN.fill(WHITE)
    SCREEN.blit(BACKGROUND_2.image, BACKGROUND_2.rect)
    SCREEN.blit(pause_surf_1, pause_rect_1)
    SCREEN.blit(pause_instructions_surf_1, pause_instructions_rect_1)
    SCREEN.blit(pause_instructions_surf_2, pause_instructions_rect_2)
    SCREEN.blit(pause_instructions_surf_3, pause_instructions_rect_3)
    pygame.display.update()

    while PAUSE:
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

        CLOCK.tick(15)


class Player(object):
    """Class for holding player information"""

    def __init__(self):
        # Currently we only keep track of the player's health
        # Will add more attributes as needed
        self.health = 3
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


class Background(
    pygame.sprite.Sprite
):  # pylint: disable=too-few-public-methods
    """Class for the background for convenience"""

    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


BACKGROUND_1 = Background("assets/space/space-1.png", [0, 0])
BACKGROUND_2 = Background("assets/space/space-2.png", [0, 0])


class Gun(pygame.sprite.Sprite):
    """The rotating gun the player fires"""

    def __init__(self, pos):
        super(Gun, self).__init__()

        self.original_image = pygame.image.load(
            "assets/gun.png"
        ).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)
        self.turning_left = True
        self.angle = 0

    def update(self):
        """Rotate the gun"""
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        if self.angle >= 70:
            self.turning_left = False
        elif self.angle <= -70:
            self.turning_left = True

        if self.turning_left:
            self.angle += 2
        else:
            self.angle -= 2
        self.rect = self.image.get_rect(center=self.rect.center)

    def kill(self):
        """Remove the gun from the game"""
        pygame.sprite.Sprite.kill(self)


class Projectile(pygame.sprite.Sprite):
    """This is what the rotating gun fires"""

    def __init__(self, pos, angle, initial_offset=0):
        super(Projectile, self).__init__()
        self.image = pygame.image.load("assets/projectile.png").convert_alpha()
        self.rect = self.image.get_rect(
            center=(
                pos[0] - round(initial_offset * sin(radians(angle))),
                pos[1] - round(initial_offset * cos(radians(angle))),
            )
        )
        self.speed = 5
        self.x_vel = -round(self.speed * sin(radians(angle)))
        self.y_vel = -round(self.speed * cos(radians(angle)))

    def update(self):
        """Update position of projectile"""
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def off_screen(self):
        """Check to see if projectile is off screen"""

        return (
            self.rect.x > DISPLAY_WIDTH
            or self.rect.x < 0
            or self.rect.y > DISPLAY_HEIGHT
            or self.rect.y < 0
        )

    def kill(self):
        """Remove the projectile from the game"""
        pygame.sprite.Sprite.kill(self)


class Missile(pygame.sprite.Sprite):
    """These missiles rain from the sky to attack the player"""

    def __init__(self, pos):
        super(Missile, self).__init__()
        self.image = pygame.image.load(
            "assets/missiles/missile-1_fly-0.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.speed = 4

    def update(self):
        """Updates y pos to move down"""
        self.rect[1] += self.speed

    def off_screen(self):
        """Check if missile is off screen"""
        return self.rect.y > DISPLAY_HEIGHT - self.image.get_height()

    def kill(self):
        """Remove the projectile from the game"""
        pygame.sprite.Sprite.kill(self)


class Button(pygame.sprite.Sprite):
    """Generic button with text"""

    def __init__(self, button_text, rect, color, function):
        super(Button, self).__init__()
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size)

        button_rect = button_text.get_rect()
        button_rect.center = (
            pygame.Vector2(self.rect.center) - self.rect.topleft
        )

        pygame.draw.rect(
            self.image, color, self.image.get_rect(), border_radius=12
        )
        self.image.blit(button_text, button_rect)
        self.function = function

    def hit(self):
        """What the button does when hit"""
        self.function()

    def kill(self):
        """Remove button from game"""
        pygame.sprite.Sprite.kill(self)


def about_page():
    """The about page of Spinny Gun"""

    pygame.mixer.music.stop()

    credit_surf_1, credit_rect_1 = text_objects(
        "Spinny Gun was created by Caleb Werth,",
        MEDIUM_TEXT,
        WHITE,
        (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.375),
    )
    credit_surf_2, credit_rect_2 = text_objects(
        "Russell Spry, and Aaron Werth",
        MEDIUM_TEXT,
        WHITE,
        (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.4375),
    )
    instructions_surf, instructions_rect = text_objects(
        "Press space to return to menu",
        MEDIUM_TEXT,
        WHITE,
        (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.65),
    )

    SCREEN.fill(WHITE)
    SCREEN.blit(BACKGROUND_2.image, BACKGROUND_2.rect)
    SCREEN.blit(credit_surf_1, credit_rect_1)
    SCREEN.blit(credit_surf_2, credit_rect_2)
    SCREEN.blit(instructions_surf, instructions_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game_menu()

        pygame.display.update()
        CLOCK.tick(15)


def game_menu():
    """The menu for the game"""

    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/audio/bensound-endlessmotion.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    start_button = Button(
        SMALL_TEXT.render("Start", True, BLACK),
        ((DISPLAY_WIDTH * 0.16), (DISPLAY_HEIGHT * 0.65), 100, 50),
        GREEN,
        game_loop,
    )
    about_button = Button(
        SMALL_TEXT.render("About", True, BLACK),
        ((DISPLAY_WIDTH * 0.43), (DISPLAY_HEIGHT * 0.5), 100, 50),
        LIGHT_YELLOW,
        about_page,
    )
    quit_button = Button(
        SMALL_TEXT.render("Quit", True, BLACK),
        ((DISPLAY_WIDTH * 0.70), (DISPLAY_HEIGHT * 0.65), 100, 50),
        RED,
        exit_game,
    )

    text_surf_title, text_rect_title = text_objects(
        "RAstral Rampart",
        BIG_TEXT,
        WHITE,
        ((DISPLAY_WIDTH * 0.5), (DISPLAY_HEIGHT * 0.2)),
    )
    text_surf_space, text_rect_space = text_objects(
        "Press Space To Shoot!",
        MEDIUM_TEXT,
        WHITE,
        ((DISPLAY_WIDTH * 0.5), (DISPLAY_HEIGHT * 0.32)),
    )

    all_sprites_list = pygame.sprite.Group()
    projectile_list = pygame.sprite.Group()
    buttons_list = pygame.sprite.Group()

    all_sprites_list.add(start_button, about_button, quit_button)
    buttons_list.add(start_button, about_button, quit_button)

    gun = Gun((DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.875))
    all_sprites_list.add(gun)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(SHOOT_FX)
                    projectile = Projectile(
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

        SCREEN.fill(WHITE)
        SCREEN.blit(BACKGROUND_2.image, BACKGROUND_2.rect)
        SCREEN.blit(text_surf_title, text_rect_title)
        SCREEN.blit(text_surf_space, text_rect_space)

        all_sprites_list.draw(SCREEN)

        pygame.display.update()
        CLOCK.tick(60)


def game_loop():
    """The main game loop"""
    global PAUSE  # pylint: disable=global-statement

    # This is for the in-game background music
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/audio/electric_jazz.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    all_sprites_list = pygame.sprite.Group()
    missile_list = pygame.sprite.Group()
    projectile_list = pygame.sprite.Group()

    player = Player()
    gun = Gun((DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.875))
    all_sprites_list.add(gun)

    delta_t = 0
    game_time = 0

    while True:

        # Add last iteration's time to running game_time
        game_time += delta_t

        # Creates scoreboard
        scoreboard_surf, scoreboard_rect = text_objects(
            "Score: " + str(player.score),
            SMALL_TEXT,
            WHITE,
            ((DISPLAY_WIDTH * 0.058), (DISPLAY_HEIGHT * 0.025)),
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            # Fire a projectile if the player presses and releases space
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and player.ammo > 0:
                    player.pew()
                    if player.ammo == 0:
                        player.reload_start_time = game_time
                    pygame.mixer.Sound.play(SHOOT_FX)
                    projectile = Projectile(
                        gun.rect.center,
                        gun.angle,
                        gun.image.get_height() * 0.5,
                    )
                    all_sprites_list.add(projectile)
                    projectile_list.add(projectile)
                if event.key == pygame.K_ESCAPE:
                    PAUSE = True
                    paused()

        # Reload
        if player.time_to_reload(game_time):
            player.reload()

        # Randomly spawn missiles at rate based on difficulty level
        if random.randrange(150 // DIFFICULTY) == 0:
            missile = Missile((random.randrange(DISPLAY_WIDTH), -600))
            all_sprites_list.add(missile)
            missile_list.add(missile)

        all_sprites_list.update()

        for projectile in projectile_list:
            if pygame.sprite.spritecollide(projectile, missile_list, True):
                pygame.mixer.Sound.play(EXPLOSION_FX)
                projectile.kill()
                player.update_score(1)

            if projectile.off_screen():
                projectile.kill()

        for missile in missile_list:
            if missile.off_screen():
                missile.kill()
                player.update_health(-1)
                if player.health <= 0:
                    game_over()

        # Paint the background WHITE
        SCREEN.fill(WHITE)
        SCREEN.blit(BACKGROUND_1.image, BACKGROUND_1.rect)
        SCREEN.blit(scoreboard_surf, scoreboard_rect)

        # Draw all sprites
        all_sprites_list.draw(SCREEN)

        # Move all background changes to the foreground
        pygame.display.update()

        # Store time since last tick in seconds
        delta_t = CLOCK.tick(60) / 1000


if __name__ == "__main__":
    game_menu()
