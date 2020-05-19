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
