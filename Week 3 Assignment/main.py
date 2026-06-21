import pygame
from constants import *
from player import Player
from game import Game
from renderer import *
from utils import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RL Arena")
clock = pygame.time.Clock()

player1 = Player(5, 5, RED,1)
player2 = Player(15, 15, BLUE,2)

game = Game(ROWS, COLS)
game.add_player(player1)
game.add_player(player2)

actions_wasd = {pygame.K_a: (0, -1), pygame.K_w: (-1, 0),
                pygame.K_d: (0, 1), pygame.K_s: (1, 0)}
actions_arrows = {pygame.K_LEFT: (0, -1), pygame.K_RIGHT: (0, 1),
                  pygame.K_DOWN: (1, 0), pygame.K_UP: (-1, 0)}

running = True
game_over = False

while running:
    clock.tick(FPS)  
    for event in pygame.event.get():
        # Handle quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Read keyboard, update player directions
        if event.type == pygame.KEYDOWN:
            if event.key in actions_wasd:
                player1.dir = actions_wasd[event.key]
            if event.key in actions_arrows:
                player2.dir = actions_arrows[event.key]    
    game.update()
    # If anyone died, change game_over var
    if player1.alive == False or player2.alive == False:
        game_over = True
        running = False

    # Draw everything
    screen.fill(BLACK)
    draw_grid(screen)
    draw_trail(screen, player1)
    draw_trail(screen, player2)
    draw_territory(screen, player1)
    draw_territory(screen, player2)
    draw_player(screen, player1)
    draw_player(screen, player2)

    # If game over, render text on top
    if game_over: 
        font = pygame.font.SysFont(None, 72)  
        text = font.render("Game Over", True, WHITE)  
        screen.blit(text, (400, 400))  
    pygame.display.update()

pygame.quit()
