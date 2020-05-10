"""This file currently contains all the Spinny Gun code"""
import random
from math import cos, sin, radians
import pygame  # pylint: disable=import-error

# Screen width and height
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (218, 165, 32)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_YELLOW = (100, 100, 93)

# Initializing
pygame.init()
SCREEN = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Spinny Gun")
CLOCK = pygame.time.Clock()

# Text
GIANT_TEXT = pygame.font.Font("freesansbold.ttf", 115)
MEDIUM_TEXT = pygame.font.Font("freesansbold.ttf", 30)
SMALL_TEXT = pygame.font.Font("freesansbold.ttf", 20)


def exit_game():
    """Exits the the game"""
    pygame.quit()
    quit()


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


def intersects(rect, radius, center):
    """Test if rect intersects with circle"""
    circle_distance_x = abs(center[0] - rect.centerx)
    circle_distance_y = abs(center[1] - rect.centery)
    if (
        circle_distance_x > rect.w / 2.0 + radius
        or circle_distance_y > rect.h / 2.0 + radius
    ):
        return False
    if circle_distance_x <= rect.w / 2.0 or circle_distance_y <= rect.h / 2.0:
        return True
    corner_x = circle_distance_x - rect.w / 2.0
    corner_y = circle_distance_y - rect.h / 2.0
    corner_distance_sq = corner_x ** 2.0 + corner_y ** 2.0
    return corner_distance_sq <= radius ** 2.0


class Background(
    pygame.sprite.Sprite
):  # pylint: disable=too-few-public-methods
    """Class for the background for convenience"""

    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


BACKGROUND_1 = Background("assets/space/space-1.png", [0, 0])
BACKGROUND_2 = Background("assets/space/space-2.png", [0, 0])


class SpinnyGun(object):
    """The rotating gun that the player can fire"""

    def __init__(self, display, pos):
        self.display = display
        self.image = pygame.image.load("assets/gun.png")
        self.rotated_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.angle = 0
        self.turning_left = True

    def blit(self):
        """Draws gun on display"""
        self.display.blit(self.rotated_image, self.rect)

    def rotate(self):
        """
        Rotates self a set number of degrees,
        changing direction when needed
        """
        if self.angle >= 60:
            self.turning_left = False
        elif self.angle <= -60:
            self.turning_left = True

        if self.turning_left:
            self.angle += 1
        else:
            self.angle -= 1

        self.rotated_image, self.rect = rot_center(
            self.image, self.rect, self.angle
        )


class Projectile(object):
    """This is what the Spinny Gun fires"""

    def __init__(self, display, pos, angle, initial_offset=0):
        self.display = display
        """The change in pos draws the projectile at the nose of the gun"""
        self.x_pos = pos[0] - round(initial_offset * sin(radians(angle)))
        self.y_pos = pos[1] - round(initial_offset * cos(radians(angle)))
        self.speed = 5
        self.x_vel = -round(self.speed * sin(radians(angle)))
        self.y_vel = -round(self.speed * cos(radians(angle)))
        self.radius = 8

    def draw(self):
        """Draws circle on display at x and y pos"""
        pygame.draw.circle(
            self.display, GOLD, (self.x_pos, self.y_pos), self.radius
        )

    def move(self):
        """Moves according to x and y velocity"""
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

    def update(self, projectiles):
        """
        Update position of projectile
        and check it it's off-screen
        """
        if (
            self.x_pos > DISPLAY_WIDTH
            or self.x_pos < 0
            or self.y_pos > DISPLAY_HEIGHT
            or self.y_pos < 0
        ):
            projectiles.pop(projectiles.index(self))
        self.move()
        self.draw()


class Missile(object):
    """These missiles rain from the sky to attack the player"""

    def __init__(self, display):
        self.display = display
        self.image = pygame.image.load("assets/missiles/missile-1_fly-0.png")
        self.rotated_image = pygame.transform.rotate(self.image, 180)
        self.speed = 5
        self.x_pos = random.randrange(0, DISPLAY_WIDTH)
        self.y_pos = -600

    def blit(self):
        """Draws self at current pos"""
        self.display.blit(self.rotated_image, (self.x_pos, self.y_pos))

    def move(self):
        """Updates y pos to move down"""
        self.y_pos += self.speed


class Button(object):
    """Generic button with text"""

    def __init__(self, text, rect_dim, color, function):
        self.rect = pygame.Rect(rect_dim)
        self.text = text
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.color = color
        self.function = function

    def draw(self):
        """Draw button with text"""
        pygame.draw.rect(SCREEN, self.color, self.rect)
        SCREEN.blit(self.text, self.text_rect)

    def hit(self):
        """What the button does when hit"""
        self.function()


def about_page():
    """The about page of Spinny Gun"""

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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game_menu()

        SCREEN.fill(WHITE)
        SCREEN.blit(BACKGROUND_2.image, BACKGROUND_2.rect)
        SCREEN.blit(credit_surf_1, credit_rect_1)
        SCREEN.blit(credit_surf_2, credit_rect_2)
        SCREEN.blit(instructions_surf, instructions_rect)

        pygame.display.update()
        CLOCK.tick(60)


def game_menu():
    """The menu for the game"""

    gun = SpinnyGun(SCREEN, (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.875))
    projectiles = []
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
    buttons = [start_button, about_button, quit_button]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    projectiles.append(
                        Projectile(
                            SCREEN,
                            gun.rect.center,
                            gun.angle,
                            gun.image.get_height() * 0.5,
                        )
                    )

        SCREEN.fill(WHITE)
        SCREEN.blit(BACKGROUND_2.image, BACKGROUND_2.rect)
        text_surf_title, text_rect_title = text_objects(
            "Spinny Gun",
            GIANT_TEXT,
            WHITE,
            ((DISPLAY_WIDTH * 0.5), (DISPLAY_HEIGHT * 0.2)),
        )
        SCREEN.blit(text_surf_title, text_rect_title)

        text_surf_space, text_rect_space = text_objects(
            "Press Space To Shoot!",
            MEDIUM_TEXT,
            WHITE,
            ((DISPLAY_WIDTH * 0.5), (DISPLAY_HEIGHT * 0.32)),
        )
        SCREEN.blit(text_surf_space, text_rect_space)

        gun.rotate()
        gun.blit()

        for button in buttons:
            button.draw()

        for projectile in projectiles:
            projectile.update(projectiles)
            for button in buttons:
                if intersects(
                    button.rect,
                    projectile.radius,
                    (projectile.x_pos, projectile.y_pos),
                ):
                    button.hit()

        pygame.display.update()
        CLOCK.tick(60)


def game_loop():
    """The main game loop"""

    gun = SpinnyGun(SCREEN, (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.875))
    missile = Missile(SCREEN)
    projectiles = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            # Fire a projectile if the player presses and releases space
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    projectiles.append(
                        Projectile(
                            SCREEN,
                            gun.rect.center,
                            gun.angle,
                            gun.image.get_height() * 0.5,
                        )
                    )

        # Paint the background WHITE
        SCREEN.fill(WHITE)
        SCREEN.blit(BACKGROUND_1.image, BACKGROUND_1.rect)

        # If a projectile moves off-screen, remove it from the list
        for projectile in projectiles:
            projectile.update(projectiles)

        # Rotate and draw gun
        gun.rotate()
        gun.blit()

        # If the missile gets to the bottom, replace it with a new missile
        if missile.y_pos > DISPLAY_HEIGHT:
            missile = Missile(SCREEN)

        # Move and draw missile
        missile.move()
        missile.blit()

        # Move all background changes to the foreground
        pygame.display.update()
        CLOCK.tick(60)


if __name__ == "__main__":
    game_menu()
