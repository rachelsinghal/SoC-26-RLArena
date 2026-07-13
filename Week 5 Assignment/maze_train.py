import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
import pygame 


class MazeEnv(gym.Env):

    def __init__(self):
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(0.0, 1.0, (1, 10, 10), dtype=np.float32)
        # TODO
        self._max_steps = 200
        self._steps = 0
        self._maze = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1], 
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ], dtype=np.int8) 
        self.start_pos = (1,1)
        self.goal_pos = (8,8)
        self.agent_pos = self.start_pos
        pass

    def _get_obs(self):

        obs_grid = self._maze.copy()

        obs_grid[self.goal_pos[0], self.goal_pos[1]] = 2
        obs_grid[self.agent_pos[0], self.agent_pos[1]] = 3
        
        # 3. NOW convert the snapshot to float32 and normalize it
        obs_grid = obs_grid.astype(np.float32) / 3.0
    
        return np.expand_dims(obs_grid, axis=0)
        pass

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.agent_pos = self.start_pos
        self._steps = 0
        return self._get_obs(), {} # Returns observation and an empty info dict

    def step(self, action):
        self._steps += 1
        
        # 0: Up, 1: Right, 2: Down, 3: Left
        # Map actions to coordinate changes: (delta_row, delta_column)
        moves = {
            0: (-1, 0),
            1: (0, 1),
            2: (1, 0),
            3: (0, -1)
        }
        
        delta_r, delta_c = moves[action]
        next_r = self.agent_pos[0] + delta_r
        next_c = self.agent_pos[1] + delta_c
        
        reward = -0.01  # Default small step penalty to encourage short paths
        terminated = False
        truncated = False
        
        # Check wall collision
        if self._maze[next_r, next_c] == 1:
            # Hit a wall! Apply penalty, agent position stays unchanged
            reward = -0.5
        else:
            # Path is clear! Move the agent
            self.agent_pos = (next_r, next_c)
            
        # Check if the agent reached the goal
        if self.agent_pos == self.goal_pos:
            reward = 10.0  # Big reward for success
            terminated = True
            
        # Check if max step limit has been reached
        if self._steps >= self._max_steps:
            truncated = True
            
        # Return observation, reward, terminated, truncated, and empty info dictionary
        return self._get_obs(), reward, terminated, truncated, {}
        pass

    def _render_rgb(self):
        # Note: Return shape (height, width, 3) with uint8 values 0-255.
    
        # Create an empty 10x10 grid with 3 channels for RGB colors (default black)
        rgb_matrix = np.zeros((10, 10, 3), dtype=np.uint8)
        
        # Define clean, contrasting color values [Red, Green, Blue]
        COLOR_WALL = [40, 40, 40]       # Dark Charcoal for walls
        COLOR_PATH = [240, 240, 240]   # Off-White for open tracks
        COLOR_GOAL = [46, 204, 113]    # Vibrant Green for the exit flag
        COLOR_AGENT = [52, 152, 219]   # Bright Blue for the moving agent
        
        # Color the base map layer based on the maze layout
        for r in range(10):
            for c in range(10):
                if self._maze[r, c] == 1:
                    rgb_matrix[r, c] = COLOR_WALL
                else:
                    rgb_matrix[r, c] = COLOR_PATH
                    
        # Layer the dynamic elements on top using their current positions
        rgb_matrix[self.goal_pos[0], self.goal_pos[1]] = COLOR_GOAL
        rgb_matrix[self.agent_pos[0], self.agent_pos[1]] = COLOR_AGENT
        
        return rgb_matrix
        pass


def main():
    env = MazeEnv()
    """
    - PPO's default ent_coef=0 means NO exploration pressure. If your agent gets stuck at the start, try ent_coef=0.01 to encourage trying things.
    - Try different learning rates (lr=0.0003 is the default):
      - too high -> unstable training
      - too low  -> slow progress
    - Increase total_timesteps if the agent hasn't converged.
    """
    model = PPO("MlpPolicy", env, verbose=1, n_steps=1024, batch_size=64, ent_coef=0.01)
    model.learn(total_timesteps=50_000)
    model.save("maze_ppo")


if __name__ == "__main__":
    main()