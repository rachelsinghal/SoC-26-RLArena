import gymnasium as gym
import numpy as np
import pygame
from game_engine import PaperIoGameBackend

class RL_Arena_Env(gym.Env):
    def __init__(self, grid_size=15, max_steps=200):
        super().__init__()
        self.grid_size = grid_size
        self.max_steps = max_steps
        
        self.game = PaperIoGameBackend(rows=grid_size, cols=grid_size)
        
        self.observation_space = gym.spaces.Box(
            low=0.0, high=1.0, shape=(grid_size, grid_size, 3), dtype=np.float32
        )
        self.action_space = gym.spaces.Discrete(4)
        
        # Window configuration parameters
        self.window = None
        self.clock = None
        self.window_size = 600

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._steps = 0
        
        setup_grid = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        
        # Enemy Random Generation Sequence
        e_r = self.np_random.integers(4, self.grid_size - 3)
        e_c = self.np_random.integers(4, self.grid_size - 3)
        
        for r in range(e_r, e_r + 3):
            for c in range(e_c, e_c + 3):
                setup_grid[r][c] = 2  # Enemy Territory
                
        for offset in range(1, 4):
            setup_grid[(e_r - offset) % self.grid_size][e_c] = -2  # Enemy Trail

        # Player spawn baseline coordinates mapping (ID = 1)
        agent_start = [1, 1]
        agent_initial_land = [(1, 1), (1, 2), (2, 1)]
        for (r, c) in agent_initial_land:
            setup_grid[r][c] = 1

        self.game.load_gym_state(setup_grid, agent_start)
        return self._get_obs(), {}

    def step(self, action):
        self._steps += 1
        
        tiles_captured, enemy_killed, is_dead = self.game.update_step(action)
        
        reward = -0.01
        terminated = False
        truncated = False
        
        if is_dead:
            return self._get_obs(), -6.0, True, False, {}
            
        if enemy_killed:
            return self._get_obs(), 30.0, True, False, {}
            
        if tiles_captured > 0:
            reward += tiles_captured * 1.2
            
        if self._steps >= self.max_steps:
            truncated = True
            my_score = np.sum(self.game.grid == 1)
            en_score = np.sum(self.game.grid == 2)
            reward += 10.0 if my_score > en_score else -5.0
            
        return self._get_obs(), reward, terminated, truncated, {}

    def _get_obs(self):
        obs = np.zeros((self.grid_size, self.grid_size, 3), dtype=np.float32)
        obs[:, :, 0] = (self.game.grid == 1).astype(np.float32)
        obs[:, :, 1] = (self.game.grid == 2).astype(np.float32)
        obs[:, :, 2] = (self.game.grid == -2).astype(np.float32) * 1.0
        obs[self.game.player.pos[0], self.game.player.pos[1], 2] = 0.5
        return obs

    def render(self):
        """ Reuses and adapts your original drawing core logic functions """
        if self.window is None:
            pygame.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
            pygame.display.set_caption("Paper.io RL Arena - Visualizer")
            self.clock = pygame.time.Clock()

        # Calculate cell size dynamically relative to screen configuration boundaries
        CELL_SIZE = self.window_size // self.grid_size
        
        # Color palettes matching your specification requirements
        BG_COLOR = (240, 240, 240)    # Light gray backdrop
        GRAY = (200, 200, 200)        # Grid lines color
        
        # Player 1 Asset Colors (RED)
        RED_TERRITORY = (231, 76, 60)
        RED_TRAIL = (192, 41, 43)
        RED_HEAD = (255, 100, 100)
        
        # Enemy Asset Colors (BLUE)
        BLUE_TERRITORY = (52, 152, 219)
        BLUE_TRAIL = (41, 128, 185)

        # Clear screen with light default backdrop color
        self.window.fill(BG_COLOR)

        # --- 1. YOUR ORIGINAL GRID RENDERER LOOP ---
        x = 0
        while x < self.window_size:
            pygame.draw.line(self.window, GRAY, (x, 0), (x, self.window_size), 1)
            x += CELL_SIZE
        y = 0
        while y < self.window_size:
            pygame.draw.line(self.window, GRAY, (0, y), (self.window_size, y), 1)
            y += CELL_SIZE

        # --- 2. STATIC ENEMY RENDERER (BLUE) ---
        # Scan and draw the static enemy elements directly from the grid layer matrix
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.game.grid[r, c] == 2:    # Enemy Base
                    pygame.draw.rect(self.window, BLUE_TERRITORY, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif self.game.grid[r, c] == -2: # Enemy Footprint Trail
                    pygame.draw.rect(self.window, BLUE_TRAIL, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # --- 3. YOUR ORIGINAL PLAYER TERRITORY RENDERER ---
        for pos in self.game.player.territory:
            row, col = pos
            pygame.draw.rect(self.window, RED_TERRITORY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # --- 4. YOUR ORIGINAL PLAYER TRAIL RENDERER ---
        for pos in self.game.player.trail:
            row, col = pos
            pygame.draw.rect(self.window, RED_TRAIL, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # --- 5. YOUR ORIGINAL PLAYER POSITION HEAD RENDERER ---
        row, col = self.game.player.pos
        pygame.draw.rect(self.window, RED_HEAD, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()
        self.clock.tick(10)  # Steps window animations at 10 frames per second