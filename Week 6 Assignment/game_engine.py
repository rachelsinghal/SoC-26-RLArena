import numpy as np
from utils import flood_fill_bounded
from player import Player
from constants import *

class PaperIoGameBackend:
    def __init__(self, rows=15, cols=15):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        
        # Instantiate the player object
        self.player = Player(1, 1, RED, id=1)
        self.enemy_id = 2
        
    def load_gym_state(self, initial_grid, start_pos):
        """ Ingests layout from Gym and aligns your Player instance states """
        self.grid = initial_grid.copy().astype(int)
        
        # Sync your custom player state to match the new spawn location
        self.player.start_pos = tuple(start_pos)
        self.player.reset()
        
        # Populate initial player territory list based on what Gym generated
        self.player.territory = [
            (int(r), int(c)) for r, c in zip(*np.where(self.grid == self.player.id))
        ]

    def update_step(self, action): #returns tiles_captured, enemy_killed, player dead
        """ Executes game logic utilizing your exact player object properties """
        # Translate discrete gym actions to your player's coordinate velocity tuple
        moves = {
            0: (-1, 0),  # Up
            1: (0, 1),   # Right
            2: (1, 0),   # Down
            3: (0, -1)   # Left
        }
        self.player.dir = moves[action]
        # Calculate destination using your formula: player.pos + player.dir
        nr = self.player.pos[0] + self.player.dir[0]
        nc = self.player.pos[1] + self.player.dir[1]
        
        # 1. Boundary Verification
        in_bounds = (0 <= nr < self.rows and 0 <= nc < self.cols)
        if not in_bounds:
            self.player.alive = False
            return 0, False, True
            
        # 2. Obstacle & Crash Checks (Using your specific logic formulas)
        if self.grid[nr][nc] == self.enemy_id:
            self.player.alive = False
            return 0, False, True
            
        # Crash into own trail (-1 * player.id)
        if self.grid[nr][nc] == -1 * self.player.id:
            self.player.alive = False
            return 0, False, True
            
        # Crash into opponent's trail (-1 * enemy_id)
        if self.grid[nr][nc] == -1 * self.enemy_id:
            self.grid[self.grid == self.enemy_id] = 0
            self.grid[self.grid == -1 * self.enemy_id] = 0
            return 0, True, False

        tiles_captured = 0

        # 3. Territory Expansion Logic
        if self.grid[nr][nc] == self.player.id:  # Enclose territory
            if len(self.player.trail) > 0:
                # Build bounding boxes around trail + last position
                trail_cells = self.player.trail + [self.player.pos]
                rows_list = [pos[0] for pos in trail_cells]
                cols_list = [pos[1] for pos in trail_cells]

                min_row = max(0, min(rows_list) - 1)
                max_row = min(self.rows - 1, max(rows_list) + 1)
                min_col = max(0, min(cols_list) - 1)
                max_col = min(self.cols - 1, max(cols_list) + 1)

                seeds = []
                for c in range(min_col, max_col + 1):
                    seeds.append((min_row, c))
                    seeds.append((max_row, c))
                for r in range(min_row, max_row + 1):
                    seeds.append((r, min_col))
                    seeds.append((r, max_col))

                flood_fill_bounded(self.grid, seeds, 0, 99, min_row, max_row, min_col, max_col)

                # Restore loop 
                for r in range(min_row, max_row + 1):
                    for c in range(min_col, max_col + 1):
                        if self.grid[r][c] == 0:
                            self.grid[r][c] = self.player.id
                            self.player.territory.append((r, c))
                            tiles_captured += 1
                        elif self.grid[r][c] == 99:
                            self.grid[r][c] = 0
                        elif self.grid[r][c] == -1 * self.player.id:
                            self.grid[r][c] = self.player.id
                            self.player.territory.append((r, c))
                            tiles_captured += 1

                self.player.trail.clear()
            self.player.pos = (nr, nc)
            
        else:  # Normal movement trail addition
            self.grid[nr][nc] = -1 * self.player.id
            self.player.trail.append((nr, nc))
            self.player.pos = (nr, nc)

        return tiles_captured, False, not self.player.alive