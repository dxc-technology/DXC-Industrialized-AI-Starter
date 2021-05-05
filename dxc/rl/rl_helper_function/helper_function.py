from .define_model_components import define_critic_layers
from .define_model_components import define_layers
from .define_model_components import define_memory
from .define_model_components import define_policy
from .define_model_components import define_random_process

import numpy as np
import gym
from gym import spaces

import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Activation, Flatten, Input, Concatenate
from tensorflow.keras.optimizers import Adam

import rl
from rl.agents.dqn import DQNAgent
from rl.agents import DDPGAgent
from rl.agents import SARSAAgent

from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess


def rl_helper(env, model_name, saved_model_name="model", steps=50000, test_steps=5, visualize=False, hidden_layers=3, critic_hidden_layers=3):
    if (model_name == "DDPG"):
        tf.compat.v1.enable_eager_execution()
        tf_keras_ddpg(env, saved_model_name, steps)
    else:
        tf.compat.v1.disable_eager_execution()
        keras_rl(env, model_name, saved_model_name, steps, test_steps, visualize, hidden_layers, critic_hidden_layers)
    

def keras_rl(env, model_name, saved_model_name="model", steps=50000, test_steps=5, visualize=False, hidden_layers=3, critic_hidden_layers=3):
    nb_actions = 0
    if (model_name == "DQN" or model_name == "SARSA"):
        nb_actions = env.action_space.n
    elif (model_name == "DDPG"):
        nb_actions = env.action_space.shape[0]

    model_structure = define_layers(
        env, nb_actions, num_of_hidden_layers=hidden_layers)
    memory = define_memory()
    policy = define_policy(model_name)

    if (model_name == "DQN"):
        model = DQNAgent(model=model_structure, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100,
                         enable_double_dqn=True, dueling_type='avg', target_model_update=1e-2)
    elif (model_name == "SARSA"):
        model = SARSAAgent(
            model=model_structure, nb_actions=nb_actions, nb_steps_warmup=10, policy=policy)
    elif (model_name == "DDPG"):
        action_input, critic_layers = define_critic_layers(
            env, num_of_hidden_layers=critic_hidden_layers)
        random_process = define_random_process(nb_actions)
        model = DDPGAgent(nb_actions=nb_actions, actor=model_structure, critic=critic_layers, critic_action_input=action_input,
                          memory=memory, nb_steps_warmup_critic=100, nb_steps_warmup_actor=100,
                          random_process=random_process, gamma=.99, target_model_update=1e-3)

    model.compile(Adam(lr=1e-3), metrics=['mae'])
    model.fit(env, nb_steps=steps, visualize=False, verbose=2)
    model.save_weights('{}.h5f'.format(model_name), overwrite=True)
    model.test(env, nb_episodes=test_steps, visualize=visualize)

def tf_keras_ddpg(env, saved_model_name, steps=50000):
    num_states = env.observation_space.shape[0]
    print("Size of State Space ->  {}".format(num_states))
    num_actions = env.action_space.shape[0]
    print("Size of Action Space ->  {}".format(num_actions))

    upper_bound = env.action_space.high[0]
    lower_bound = env.action_space.low[0]

    print("Max Value of Action ->  {}".format(upper_bound))
    print("Min Value of Action ->  {}".format(lower_bound))

    def get_actor():
        # Initialize weights between -3e-3 and 3-e3
        last_init = tf.random_uniform_initializer(minval=-0.003, maxval=0.003)

        inputs = layers.Input(shape=(num_states,))
        out = layers.Dense(256, activation="relu")(inputs)
        out = layers.Dense(256, activation="relu")(out)
        outputs = layers.Dense(1, activation="tanh", kernel_initializer=last_init)(out)

        # Our upper bound is 2.0 for Pendulum.
        outputs = outputs * upper_bound
        model = tf.keras.Model(inputs, outputs)
        return model

    def get_critic():
        # State as input
        state_input = layers.Input(shape=(num_states))
        state_out = layers.Dense(16, activation="relu")(state_input)
        state_out = layers.Dense(32, activation="relu")(state_out)

        # Action as input
        action_input = layers.Input(shape=(num_actions))
        action_out = layers.Dense(32, activation="relu")(action_input)

        # Both are passed through seperate layer before concatenating
        concat = layers.Concatenate()([state_out, action_out])

        out = layers.Dense(256, activation="relu")(concat)
        out = layers.Dense(256, activation="relu")(out)
        outputs = layers.Dense(1)(out)

        # Outputs single value for give state-action
        model = tf.keras.Model([state_input, action_input], outputs)

        return model

    def policy(state, noise_object):
        sampled_actions = tf.squeeze(actor_model(state))
        noise = noise_object()
        # Adding noise to action
        sampled_actions = sampled_actions.numpy() + noise

        # We make sure action is within bounds
        legal_action = np.clip(sampled_actions, lower_bound, upper_bound)

        return [np.squeeze(legal_action)]

    class OUActionNoise:
        def __init__(self, mean, std_deviation, theta=0.15, dt=1e-2, x_initial=None):
            self.theta = theta
            self.mean = mean
            self.std_dev = std_deviation
            self.dt = dt
            self.x_initial = x_initial
            self.reset()

        def __call__(self):
            # Formula taken from https://www.wikipedia.org/wiki/Ornstein-Uhlenbeck_process.
            x = (
                self.x_prev
                + self.theta * (self.mean - self.x_prev) * self.dt
                + self.std_dev * np.sqrt(self.dt) * np.random.normal(size=self.mean.shape)
            )
            # Store x into x_prev
            # Makes next noise dependent on current one
            self.x_prev = x
            return x

        def reset(self):
            if self.x_initial is not None:
                self.x_prev = self.x_initial
            else:
                self.x_prev = np.zeros_like(self.mean)

    class Buffer:
        def __init__(self, buffer_capacity=100000, batch_size=64):
            # Number of "experiences" to store at max
            self.buffer_capacity = buffer_capacity
            # Num of tuples to train on.
            self.batch_size = batch_size

            # Its tells us num of times record() was called.
            self.buffer_counter = 0

            # Instead of list of tuples as the exp.replay concept go
            # We use different np.arrays for each tuple element
            self.state_buffer = np.zeros((self.buffer_capacity, num_states))
            self.action_buffer = np.zeros((self.buffer_capacity, num_actions))
            self.reward_buffer = np.zeros((self.buffer_capacity, 1))
            self.next_state_buffer = np.zeros((self.buffer_capacity, num_states))

        # Takes (s,a,r,s') obervation tuple as input
        def record(self, obs_tuple):
            # Set index to zero if buffer_capacity is exceeded,
            # replacing old records
            index = self.buffer_counter % self.buffer_capacity

            self.state_buffer[index] = obs_tuple[0]
            self.action_buffer[index] = obs_tuple[1]
            self.reward_buffer[index] = obs_tuple[2]
            self.next_state_buffer[index] = obs_tuple[3]

            self.buffer_counter += 1

        # Eager execution is turned on by default in TensorFlow 2. Decorating with tf.function allows
        # TensorFlow to build a static graph out of the logic and computations in our function.
        # This provides a large speed up for blocks of code that contain many small TensorFlow operations such as this one.
        @tf.function
        def update(
            self, state_batch, action_batch, reward_batch, next_state_batch,
        ):
            # Training and updating Actor & Critic networks.
            # See Pseudo Code.
            with tf.GradientTape() as tape:
                target_actions = target_actor(next_state_batch, training=True)
                y = reward_batch + gamma * target_critic(
                    [next_state_batch, target_actions], training=True
                )
                critic_value = critic_model([state_batch, action_batch], training=True)
                critic_loss = tf.math.reduce_mean(tf.math.square(y - critic_value))

            critic_grad = tape.gradient(critic_loss, critic_model.trainable_variables)
            critic_optimizer.apply_gradients(
                zip(critic_grad, critic_model.trainable_variables)
            )

            with tf.GradientTape() as tape:
                actions = actor_model(state_batch, training=True)
                critic_value = critic_model([state_batch, actions], training=True)
                # Used `-value` as we want to maximize the value given
                # by the critic for our actions
                actor_loss = -tf.math.reduce_mean(critic_value)

            actor_grad = tape.gradient(actor_loss, actor_model.trainable_variables)
            actor_optimizer.apply_gradients(
                zip(actor_grad, actor_model.trainable_variables)
            )

        # We compute the loss and update parameters
        def learn(self):
            # Get sampling range
            record_range = min(self.buffer_counter, self.buffer_capacity)
            # Randomly sample indices
            batch_indices = np.random.choice(record_range, self.batch_size)

            # Convert to tensors
            state_batch = tf.convert_to_tensor(self.state_buffer[batch_indices])
            action_batch = tf.convert_to_tensor(self.action_buffer[batch_indices])
            reward_batch = tf.convert_to_tensor(self.reward_buffer[batch_indices])
            reward_batch = tf.cast(reward_batch, dtype=tf.float32)
            next_state_batch = tf.convert_to_tensor(self.next_state_buffer[batch_indices])

            self.update(state_batch, action_batch, reward_batch, next_state_batch)


    # This update target parameters slowly
    # Based on rate `tau`, which is much less than one.
    @tf.function
    def update_target(target_weights, weights, tau):
        for (a, b) in zip(target_weights, weights):
            a.assign(b * tau + a * (1 - tau))    

    std_dev = 0.2
    ou_noise = OUActionNoise(mean=np.zeros(1), std_deviation=float(std_dev) * np.ones(1))

    actor_model = get_actor()
    critic_model = get_critic()

    target_actor = get_actor()
    target_critic = get_critic()

    # Making the weights equal initially
    target_actor.set_weights(actor_model.get_weights())
    target_critic.set_weights(critic_model.get_weights())

    # Learning rate for actor-critic models
    critic_lr = 0.002
    actor_lr = 0.001

    critic_optimizer = tf.keras.optimizers.Adam(critic_lr)
    actor_optimizer = tf.keras.optimizers.Adam(actor_lr)

    total_episodes = steps
    # Discount factor for future rewards
    gamma = 0.99
    # Used to update target networks
    tau = 0.005

    buffer = Buffer(50000, 64)

    # To store reward history of each episode
    ep_reward_list = []
    # To store average reward history of last few episodes
    avg_reward_list = []

    # Takes about 4 min to train
    for ep in range(total_episodes):

        prev_state = env.reset()
        episodic_reward = 0

        while True:
            # Uncomment this to see the Actor in action
            # But not in a python notebook.
            # env.render()

            tf_prev_state = tf.expand_dims(tf.convert_to_tensor(prev_state), 0)

            action = policy(tf_prev_state, ou_noise)
            # Recieve state and reward from environment.
            state, reward, done, info = env.step(action)

            buffer.record((prev_state, action, reward, state))
            episodic_reward += reward

            buffer.learn()
            update_target(target_actor.variables, actor_model.variables, tau)
            update_target(target_critic.variables, critic_model.variables, tau)

            # End this episode when `done` is True
            if done:
                break

            prev_state = state

        ep_reward_list.append(episodic_reward)

        # Mean of last 40 episodes
        avg_reward = np.mean(ep_reward_list[-40:])
        print("Episode * {} * Avg Reward is ==> {}".format(ep, avg_reward))
        avg_reward_list.append(avg_reward)

    # Plotting graph
    # Episodes versus Avg. Rewards
    plt.plot(avg_reward_list)
    plt.xlabel("Episode")
    plt.ylabel("Avg. Epsiodic Reward")
    plt.show()

    # Save the weights
    actor_model.save_weights("{}_actor.h5".format(saved_model_name))
    critic_model.save_weights("{}_critic.h5".format(saved_model_name))

    target_actor.save_weights("{}_target_actor.h5".format(saved_model_name))
    target_critic.save_weights("{}_target_critic.h5".format(saved_model_name))
