from constants import *
import numpy as np
from utils import *

class Game:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.players = []

    def add_player(self,player):
        self.players.append(player)
        row, col = player.start_pos
        self.grid[row][col] = player.id  #territory = id, trail = -id

    def update(self):
        # compute all next positions
        next_pos = {}
        for player in self.players:
            next_pos[player] = (player.pos[0] + player.dir[0], player.pos[1] + player.dir[1])
        # head-on — same target cell kills both
        if next_pos[self.players[0]] == next_pos[self.players[1]]:
            for player in self.players:
                player.alive = False

        for player in self.players:
            nr, nc = next_pos[player]
            opponent = [p for p in self.players if p != player][0]
            in_bounds = (0 <= nr < 80 and 0 <= nc < 80)
            blocked = (not in_bounds) or (in_bounds and self.grid[nr][nc] == opponent.id)
            if blocked:
                player.dir = (0, 0)
                next_pos[player] = player.pos
            else:
                if self.grid[nr][nc] == -1 * player.id and player.dir!= (0,0):  # crash into own trail
                    player.alive = False
                if self.grid[nr][nc] == -1* opponent.id: #crash into opponents trail kills opponent
                    player.alive = False
            #move the players who survived
            if player.alive: 
                if self.grid[next_pos[player][0]][next_pos[player][1]] == player.id:  # enclose territory
                    # build bounding box around the trail (+ the cell they're reconnecting from)
                    trail_cells = player.trail + [player.pos]
                    rows_list = [pos[0] for pos in trail_cells]
                    cols_list = [pos[1] for pos in trail_cells]

                    min_row = max(0, min(rows_list) - 1)
                    max_row = min(ROWS - 1, max(rows_list) + 1)
                    min_col = max(0, min(cols_list) - 1)
                    max_col = min(COLS - 1, max(cols_list) + 1)


                    seeds = []
                    for c in range(min_col, max_col + 1):
                        seeds.append((min_row, c))
                        seeds.append((max_row, c))
                    for r in range(min_row, max_row + 1):
                        seeds.append((r, min_col))
                        seeds.append((r, max_col))

                    flood_fill_bounded(self.grid, seeds, 0, 99, min_row, max_row, min_col, max_col)

                    # restore loop, scoped to the bounding box only
                    for r in range(min_row, max_row + 1):
                        for c in range(min_col, max_col + 1):
                            if self.grid[r][c] == 0:
                                self.grid[r][c] = player.id          # enclosed -> territory
                                player.territory.append((r, c))
                            elif self.grid[r][c] == 99:
                                self.grid[r][c] = 0                   # restore outside cells
                            elif self.grid[r][c] == -1 * player.id:
                                self.grid[r][c] = player.id            # trail -> territory
                                player.trail.remove((r, c))
                                player.territory.append((r,c))
                    player.pos = next_pos[player]
                else: #just normal adding to trail
                    self.grid[next_pos[player][0]][next_pos[player][1]] = -1*player.id
                    player.trail.append(next_pos[player])
                    player.pos = next_pos[player]


    def reset(self):
        for player in self.players:
            player.reset()
        self.grid = np.zeros((self.rows, self.cols), dtype=int)

