import pygame
import random
from math import cos, sin, radians

# Screen width and height
display_width = 800
display_height = 800

# Colors
white = (255, 255, 255)
gold = (218, 165, 32)

pygame.init()

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Spinny Gun")
clock = pygame.time.Clock()


def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


class SpinnyGun:
    """The rotating gun that the player can fire"""

    def __init__(self, screen, position):
        self.screen = screen
        self.image = pygame.image.load("assets/gun.png")
        self.rotated_image = self.image
        self.rect = self.image.get_rect(center=position)
        self.angle = 0
        self.turningLeft = True

    def blit(self):
        self.screen.blit(self.rotated_image, self.rect)

    def rotate(self):
        if self.angle >= 60:
            self.turningLeft = False
        elif self.angle <= -60:
            self.turningLeft = True

        if self.turningLeft:
            self.angle += 1
        else:
            self.angle -= 1

        self.rotated_image, self.rect = rot_center(self.image, self.rect, self.angle)


class Projectile:
    """This is what the Spinny Gun fires"""

    def __init__(self, screen, position, angle):
        self.screen = screen
        self.x = position[0]
        self.y = position[1]
        self.speed = 5
        self.x_vel = -round(self.speed * sin(radians(angle)))
        self.y_vel = -round(self.speed * cos(radians(angle)))
        self.radius = 8

    def draw(self):
        pygame.draw.circle(screen, gold, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel


class Missile:
    """These missiles rain from the sky to attack the player"""

    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("assets/missiles/missile-1_fly-0.png")
        self.rotated_image = pygame.transform.rotate(self.image, 180)
        self.speed = 5
        self.x = random.randrange(0, display_width)
        self.y = -600

    def blit(self):
        self.screen.blit(self.rotated_image, (self.x, self.y))

    def move(self):
        self.y += self.speed


def game_loop():
    """The main game loop"""

    gameExit = False
    gun = SpinnyGun(screen, (display_width * 0.5, display_height * 0.875))
    missile = Missile(screen)
    projectiles = []

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            # Fire a projectile if the player presses and releases space
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    projectiles.append(Projectile(screen, gun.rect.center, gun.angle))

        # Paint the background white
        screen.fill(white)

        # If a projectile moves off-screen, remove it from the list
        for projectile in projectiles:
            if (
                projectile.x > display_width
                or projectile.x < 0
                or projectile.y > display_height
                or projectile.y < 0
            ):
                projectiles.pop(projectiles.index(projectile))
            projectile.move()
            projectile.draw()

        # Rotate and draw gun
        gun.rotate()
        gun.blit()

        # If the missile gets to the bottom, replace it with a new missile
        if missile.y > display_height:
            missile = Missile(screen)

        # Move and draw missile
        missile.move()
        missile.blit()

        # Move all background changes to the foreground
        pygame.display.update()
        clock.tick(60)


game_loop()
pygame.quit()
quit()
