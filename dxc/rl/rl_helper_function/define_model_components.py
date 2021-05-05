import numpy as np
import gym
import rl

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Activation, Flatten, Input, Concatenate
from tensorflow.keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.agents import DDPGAgent
from rl.agents import SARSAAgent

from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess

def define_layers(env, nb_actions, num_of_hidden_layers=3):
  model = Sequential()
  model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
  while num_of_hidden_layers > 0:
    model.add(Dense(16))
    model.add(Activation('relu'))
    num_of_hidden_layers -= 1
  model.add(Dense(nb_actions, activation='linear'))
  return model

def define_critic_layers(env, num_of_hidden_layers=3):
  action_input = Input(shape=(env.action_space.shape[0],), name='action_input')
  observation_input = Input(shape=(1,) + env.observation_space.shape, name='observation_input')
  flattened_observation = Flatten()(observation_input)
  x = Concatenate()([action_input, flattened_observation])
  while num_of_hidden_layers > 0:
    x = Dense(16)(x)
    x = Activation('relu')(x)
    num_of_hidden_layers -= 1
  x = Dense(1)(x)
  x = Activation('linear')(x)
  critic = Model(inputs=[action_input, observation_input], outputs=x)

  return action_input, critic

def define_memory():
  memory = SequentialMemory(limit=50000, window_length=1)
  return memory

def define_policy(model_name):
  policy = []
  if (model_name == "DQN" or model_name == "SARSA"):
    policy = BoltzmannQPolicy()
  return policy

def define_random_process(nb_actions):
  random_process = OrnsteinUhlenbeckProcess(size=nb_actions, theta=.15, mu=0., sigma=.3)
  return random_process
