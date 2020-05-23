"""Global constants and state variables"""
import pygame

# Init
pygame.mixer.pre_init(22100, -16, 2, 64)
pygame.init()

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

# Text
GIANT_TEXT = pygame.font.Font("freesansbold.ttf", 115)
BIG_TEXT = pygame.font.Font("freesansbold.ttf", 80)
MEDIUM_TEXT = pygame.font.Font("freesansbold.ttf", 30)
SMALL_TEXT = pygame.font.Font("freesansbold.ttf", 20)
TINY_TEXT = pygame.font.Font("freesansbold.ttf", 14)

# Sound Effects
SHOOT_FX = pygame.mixer.Sound("assets/audio/laser.wav")
EXPLOSION_FX = pygame.mixer.Sound("assets/audio/explosion.wav")

# Display
SCREEN = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
ICON = pygame.image.load("assets/gun_icon.png").convert_alpha()
pygame.display.set_caption("RAstral Rampart")
pygame.display.set_icon(ICON)

# Clock
CLOCK = pygame.time.Clock()

# Pause
PAUSE = False

# Difficulty setting
DIFFICULTY = 1

SCORE = 0


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
