import pygame
# The screen represents a ROWS x COLS grid.
# Each grid cell is rendered as a square of size CELL_SIZE x CELL_SIZE pixels.
WIDTH = 800
HEIGHT = 800
ROWS = 80
COLS = 80
CELL_SIZE = WIDTH // COLS

FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
GREEN = (0, 255, 0)

BACKGROUND_COLOR = BLACK
GRID_COLOR = GRAY