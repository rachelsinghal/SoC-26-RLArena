import os
import pygame
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from gym_env import RL_Arena_Env

def main():
    # 1. Initialize the Gym environment
    print("Initializing Paper.io Gym Environment...")
    env = RL_Arena_Env(grid_size=15, max_steps=200)

    # 2. Verify environment API matches Gymnasium specifications
    print("Checking environment compatibility...")
    check_env(env)
    print("Environment check passed!")

    # 3. Setup PPO Agent with a spatial Convolutional Network Policy
    print("Configuring PPO Agent...")
    model = PPO(
        "MlpPolicy", 
        env, 
        verbose=1, 
        learning_rate=3e-4,
    )
    
    """# 4. Train the Agent (Set to 300,000 for your final run)
    print("Starting training loop...")
    model.learn(total_timesteps=300_000)

    # 5. Save the trained model
    model.save("paper_io_agent")
    print("Training finished! Model saved.")

    # =================================================================
    # 6. VISUAL EVALUATION LOOP (Using your Pygame render function)
    # =================================================================
    print("\nTraining complete! Launching visual evaluation window...")"""
    
    model = PPO.load("paper_io_agent", env=env)
    pygame.init()
    # Run 5 demonstration episodes back-to-back
    for episode in range(5):
        obs, _ = env.reset()
        terminated = False
        truncated = False
        score = 0
        
        print(f"Starting Visual Demonstration Episode {episode + 1}")
        
        while not (terminated or truncated):
            # Pygame event loop pump to keep the operating system window responsive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Let the trained model pick the absolute best spatial action directional move
            action, _ = model.predict(obs, deterministic=True)
            
            # Step the engine matrix calculations forward
            obs, reward, terminated, truncated, info = env.step(int(action))
            score += reward
            
            # THIS triggers your built-in Pygame rendering code blocks!
            env.render()
            
        print(f"Episode {episode + 1} finished with Total Reward Score: {score:.2f}")

    pygame.quit()

if __name__ == "__main__":
    main()