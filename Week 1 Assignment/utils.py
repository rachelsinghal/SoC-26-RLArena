from constants import *

def clear_screen():
    print("\n" * 40)


def print_grid(grid):
    for row in grid:
        print(" ".join(row))

def move_up(grid, player_row, player_col):
    if player_row == 0: 
        print('invalid move')
        return player_row, player_col
    elif grid[player_row-1][player_col] == 'X': 
        print('invalid move: Obstacle')
        return player_row, player_col
    else:
        grid[player_row][player_col] = '.'
        grid[player_row-1][player_col] = 'P'
        print_grid(grid)
        return player_row-1, player_col
    

def move_down(grid, player_row, player_col):
    if player_row == ROWS-1: 
        print('invalid move')
        return player_row, player_col
    elif grid[player_row+1][player_col] == 'X': 
        print('invalid move: Obstacle')
        return player_row, player_col
    else:
        grid[player_row][player_col] = '.'
        grid[player_row+1][player_col] = 'P'
        print_grid(grid)
        return player_row+1, player_col

def move_left(grid, player_row, player_col):
    if player_col == 0: 
        print('invalid move')
        return player_row, player_col
    elif grid[player_row][player_col-1] == 'X': 
        print('invalid move: Obstacle')
        return player_row, player_col
    else:
        grid[player_row][player_col] = '.'
        grid[player_row][player_col-1] = 'P'
        print_grid(grid)
        return player_row, player_col-1

def move_right(grid, player_row, player_col):
    if player_col == COLS-1: 
        print('invalid move')
        return player_row, player_col
    elif grid[player_row][player_col+1] == 'X': 
        print('invalid move: Obstacle')
        return player_row, player_col
    else:
        grid[player_row][player_col] = '.'
        grid[player_row][player_col+1] = 'P'
        print_grid(grid)
        return player_row, player_col+1
    
def add_obstacle(grid, row, column):
    grid[row][column] = 'X'

    