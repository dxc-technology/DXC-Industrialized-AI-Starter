# Reinforcement Learning

## Set up the development environment

This code installs all the packages you will need. Run it first. It should take 30 seconds or so to complete. If you get missing module errors later, it may be because you have not run this code. Restart the runtime/session after executing the below code.

```python
! pip install git+https://github.com/dxc-technology/DXC-Industrialized-AI-Starter.git -qq
```
```python
from dxc import rl
from gym import spaces
import numpy as np
import gym
```
## Reinforcement Learning Basics

Reinforcement learning is machine learning using rewards given to an agent acting in an environment. Instead of learning from historical data, the agent learns how to maneuver through the environment by receiving positive or negative rewards depending on the actions that it takes.

### Train an OpenAI Gym environment
Gym is a toolkit used for reinforcement learning created by OpenAI that includes several premade environments to test your models on. View OpenAI Gym environments

### Models
There are several models that can be used to train an agent in an environment. The model that needs to be used can be generally determined by the type of actions an agent can take.

If a discrete set of actions are given, DQN or SARSA can be used. A discrete set of actions are actions that you can count. Examples of this include 3 actions for Rock, Paper, Scissors or 2 actions in TicTacToe for X and O. If the action space were between 1 to 5, the actions would be 1, 2, 3, 4, and 5.

If a continous set of actions are given, DDPG can be used. A continuous set of actions are actions that you can measure. Examples of this include how fast a car should run (mph) or how likely a card will appear in a board game (%). If the action space were between 1 to 5, the actions would be all numbers between 1 to 5, including all decimal values.

### Calling the Reinforcement Learning Helper

rl_helper() accepts 2 parameters to run. The first parameter is the environment. The second parameter is the type of model the environment will train in.

There are extra parameters that can be defined, but aren't necessary. These are used to further refine your model. Listing them down and defining the default values in parenthesis after the parameter name, the parameters that can be set for both discrete and continuous environments are:

	- steps (50000): number of episodes that the model will run for
	- saved_model_name (model): name of the saved model files
	- visualize (False): boolean (True or False) if there is visualization for the model, set True to display it

The other parameters are only used for discrete environments.

	- test_steps (5): number of episodes the model will test
	- critic_hidden_layers (3): number of critic hidden layers
	- hidden_layers (3): number of hidden layers
	
To call a gym environment, simply use the gym.make() function and pass the name of the gym environment. You can get the name of the gym environment here.

## Continuous Example

In the following example code, the Pendulum environment is used. This is an environment where the goal of the agent is to balance a pendulum upright. Unlike the cartpole example, the actions set for this environment are continuous, so DDPG will be used to train it.

```python
env = gym.make("Pendulum-v0")
rl.rl_helper(env=env, 
             model_name="DDPG", 
             saved_model_name="pendulum_model", 
             steps=1000)
```

## Discrete Example

In the following example code, the Cart Pole environment is used. This is an environment where the goal of the agent (which is a cart) is to balance a pole. The model used is DQN (discrete actions) since the actions that the cart can take is move left or right. SARSA may also be used since it is a discrete environment.

```python
import gym

gym_env = gym.make("CartPole-v0")
rl.rl_helper(env=gym_env, 
             model_name="DQN", #SARSA
             steps=25000, 
             test_steps=5,
             visualize=False,
             saved_model_name="cartpole_model",
             critic_hidden_layers=2,
             hidden_layers=2)
```