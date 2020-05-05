import pygame
import time

display_width = 800
display_height = 800

def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect

class SpinnyGun:
    def __init__(self, screen, position):
        self.image = pygame.image.load('ship.png')
        self.rotated_image = self.image
        self.rect = self.image.get_rect(center=position)
        self.screen = screen

    def blit(self):
        self.screen.blit(self.rotated_image, self.rect)

    def rotate(self, angle):
        self.rotated_image, self.rect = rot_center(self.image, self.rect, angle)

pygame.init()

white = (255, 255, 255)

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Spinny Gun')
clock = pygame.time.Clock()

def game_loop():
    angle = 0
    turningLeft = True

    gameExit = False
    gun = SpinnyGun(screen, (display_width * 0.5, display_height * 0.875))

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

        screen.fill(white)

        if angle >= 60:
            turningLeft = False
        elif angle <= -60:
            turningLeft = True

        if turningLeft:
            angle += 1
        else:
            angle -= 1

        gun.rotate(angle)
        gun.blit()
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
