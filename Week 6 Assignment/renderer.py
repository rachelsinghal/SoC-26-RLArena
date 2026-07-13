import pygame
from constants import *
from player import Player

def draw_grid(screen):
    x=0
    while(x<WIDTH):
        pygame.draw.line(screen, GRAY, (x,0), (x, HEIGHT), 1)
        x = x+CELL_SIZE
    y=0
    while(y<HEIGHT):
        pygame.draw.line(screen, GRAY, (0,y), (WIDTH, y), 1)
        y = y+CELL_SIZE
    

def draw_player(screen, player):
    row, col = player.pos
    x = col * CELL_SIZE
    y = row * CELL_SIZE
    pygame.draw.rect(screen, player.territory_color, (x,y, CELL_SIZE, CELL_SIZE))

def draw_trail(screen, player):
    for pos in player.trail:
        row, col = pos
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        pygame.draw.rect(screen, player.trail_color, (x, y, CELL_SIZE, CELL_SIZE))

def draw_territory(screen, player):
    for pos in player.territory:
        row, col = pos
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        pygame.draw.rect(screen, player.territory_color, (x, y, CELL_SIZE, CELL_SIZE))
    