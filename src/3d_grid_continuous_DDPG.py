from stable_baselines3.common.env_checker import check_env
import gym
import numpy as np
import gym
from gym import spaces
from stable_baselines3 import A2C, DDPG, SAC
from stable_baselines3.common.env_util import make_vec_env

class ReachEndEnv(gym.Env):
    """
    This is a simple env where the agent must learn to reach the destination with obstacles in between. 
    """
    metadata = {'render.modes': ['console']}
    # Define constants
    # LEFT = 0
    # RIGHT = 1
    # UP = 2
    # DOWN = 3

    def __init__(self, grid_size=4,block_low=1,block_high=2):
        super(ReachEndEnv, self).__init__()

        # Size of the 2D-grid
        self.grid_size = grid_size
        # Initialize the agent at the top left corner
        self.initial_pos = np.zeros((3,),dtype=np.float32) 
        self.agent_pos = np.zeros((3,),dtype=np.float32)
        # Specify the blocked region
        self.block_low =block_low
        self.block_high =block_high
        self.act_low = -1.0
        self.act_high = 1.0
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions, we have two: left and right
        self.action_space = spaces.Box(low=self.act_low, high=self.act_high, shape=(3,), dtype=np.float32)
        # The observation will be the coordinate of the agent
        # this can be described both by Discrete and Box space
        self.observation_space = spaces.Box(low=0, high=self.grid_size, shape=(3,), dtype=np.float32)
        # Check if goal is reached
        self.endcheck = False

    def reset(self):
        """
        Important: the observation must be a numpy array
        :return: (np.array) 
        """
        # Initialize the agent at the right of the grid
        self.agent_pos = np.zeros((3,),dtype=np.float32)#self.initial_pos
        # here we convert to float32 to make it more general (in case we want to use continuous actions)
        # return np.array([self.agent_pos]).astype(np.float32)
        return self.agent_pos

    def step(self, action):

            
        self.agent_pos += action
        if action[0]<self.act_low or action[0]>self.act_high:
            raise ValueError("Received invalid action={} which is not part of the action space".format(action))
        if action[1]<self.act_low or action[1]>self.act_high:
            raise ValueError("Received invalid action={} which is not part of the action space".format(action)) 
        if action[2]<self.act_low or action[2]>self.act_high:
            raise ValueError("Received invalid action={} which is not part of the action space".format(action))    

        # Account for the boundaries of the grid
        self.agent_pos = np.clip(self.agent_pos, 0, self.grid_size-1)

        # Are we at the end?
        done = bool(self.agent_pos[0] == self.grid_size-1 and self.agent_pos[1]==self.grid_size-1 and \
                    self.agent_pos[2]==self.grid_size-1)

        # Null reward everywhere except when reaching the goal (right corner)
        if self.agent_pos[0] == self.grid_size-1 and self.agent_pos[1]==self.grid_size-1 and \
        self.agent_pos[2]==self.grid_size-1: 
            reward = 1
        elif self.agent_pos[0]>=self.block_low and self.agent_pos[0]<=self.block_high and \
        self.agent_pos[1]>=self.block_low and self.agent_pos[1]<=self.block_high and\
        self.agent_pos[2]>=self.block_low and self.agent_pos[2]<=self.block_high:
            reward = -10
        else:
            reward = -1

        # Optionally we can pass additional info, we are not using that for now
        info = {}
        self.endcheck = done

        return self.agent_pos, reward, done, info

    def render(self, mode='console'):
        if mode != 'console':
            raise NotImplementedError()        

    def close(self):
        pass

    
env = ReachEndEnv()
# If the environment don't follow the interface, an error will be thrown
check_env(env, warn=True)

# Instantiate the env
env = ReachEndEnv(grid_size=10,block_low=3,block_high=6)
# wrap it
env = make_vec_env(lambda: env, n_envs=1)

# Train the agent
# Using Deep Deterministic Policy gradient
model = DDPG('MlpPolicy', env, train_freq= 4, tensorboard_log='./log_files/',verbose=1).learn(500000)

# Test the trained agent
obs = env.reset()
OBS = np.zeros((14,3))
n_steps = 1000
for step in range(n_steps):
    action, _ = model.predict(obs, deterministic=True)
    print("Step {}".format(step + 1))
    print("Action: ", action)
    obs, reward, done, info = env.step(action)
    print('obs=', obs, 'reward=', reward, 'done=', done)
    # env.render(mode='console')
    OBS[step+1] = obs
    if done:
        # Note that the VecEnv resets automatically
        # when a done signal is encountered
        print("Goal reached!", "reward=", reward)
        break
        
# Save the model
model.save('3d_grid_obstacle_continuous10x10')

# Load the model
# model = SAC.load('3d_grid_obstacle_continuous10x10')

# Save the results
from scipy import io
io.savemat('3d_grid_obstacle.mat',{'OBS':OBS})