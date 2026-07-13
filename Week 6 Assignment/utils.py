import pygame
from player import Player
from constants import *

def flood_fill_bounded(grid, seeds, old_color, new_color, min_row, max_row, min_col, max_col):
    if old_color == new_color:
        return
    stack = list(seeds)
    while stack:
        i, j = stack.pop()
        if i < min_row or i > max_row or j < min_col or j > max_col:
            continue
        if grid[i][j] != old_color:
            continue
        grid[i][j] = new_color
        stack.extend([(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)])