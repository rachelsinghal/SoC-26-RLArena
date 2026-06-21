from constants import *
from utils import *

# Create empty grid

grid = []

# Player starting position
player_row = 0
player_col = 0


# Obstacles
obstacles = []

running = True

    # Reset grid
for _ in range(ROWS):
    row = [EMPTY_CELL] * COLS
    grid.append(row)
print_grid(grid)

    # Add obstacles
add_obstacle(grid, 1, 3)
add_obstacle(grid, 2, 7)
add_obstacle(grid, 1, 6)
add_obstacle(grid, 0, 5)
add_obstacle(grid, 2, 1)
print_grid(grid)

    # Add player
grid[player_row][player_col] = 'P'
print_grid(grid)

while running:
        # Take input and update position
    command = input("enter a command: ")
        
    if command == 'W': 
        player_row, player_col = move_up(grid, player_row, player_col)  

    if command == 'A': 
        player_row, player_col = move_left(grid, player_row, player_col)  

    if command == 'S': 
        player_row, player_col = move_down(grid, player_row, player_col)  

    if command == 'D': 
        player_row, player_col = move_right(grid, player_row, player_col) 






    
    
