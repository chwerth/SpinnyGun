"""This file currently contains all the Spinny Gun code"""
import random
from math import cos, sin, radians
import pygame  # pylint: disable=import-error

# Screen width and height
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
GOLD = (218, 165, 32)

# Initializing
pygame.init()
SCREEN = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Spinny Gun")
CLOCK = pygame.time.Clock()


def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


class SpinnyGun(object):
    """The rotating gun that the player can fire"""

    def __init__(self, display, position):
        self.display = display
        self.image = pygame.image.load("assets/gun.png")
        self.rotated_image = self.image
        self.rect = self.image.get_rect(center=position)
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

    def __init__(self, display, position, angle):
        self.display = display
        self.x_pos = position[0]
        self.y_pos = position[1]
        self.speed = 5
        self.x_vel = -round(self.speed * sin(radians(angle)))
        self.y_vel = -round(self.speed * cos(radians(angle)))
        self.radius = 8

    def draw(self):
        """Draws circle on display at x and y position"""
        pygame.draw.circle(
            self.display, GOLD, (self.x_pos, self.y_pos), self.radius
        )

    def move(self):
        """Moves according to x and y velocity"""
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel


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
        """Draws self at current position"""
        self.display.blit(self.rotated_image, (self.x_pos, self.y_pos))

    def move(self):
        """Updates y position to move down"""
        self.y_pos += self.speed


def game_loop():
    """The main game loop"""

    game_exit = False
    gun = SpinnyGun(SCREEN, (DISPLAY_WIDTH * 0.5, DISPLAY_HEIGHT * 0.875))
    missile = Missile(SCREEN)
    projectiles = []

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            # Fire a projectile if the player presses and releases space
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    projectiles.append(
                        Projectile(SCREEN, gun.rect.center, gun.angle)
                    )

        # Paint the background WHITE
        SCREEN.fill(WHITE)

        # If a projectile moves off-screen, remove it from the list
        for projectile in projectiles:
            if (
                projectile.x_pos > DISPLAY_WIDTH
                or projectile.x_pos < 0
                or projectile.y_pos > DISPLAY_HEIGHT
                or projectile.y_pos < 0
            ):
                projectiles.pop(projectiles.index(projectile))
            projectile.move()
            projectile.draw()

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


game_loop()
pygame.quit()
quit()
