from keras.models import Sequential
from keras.layers import *
from keras.optimizers import *

import random as rnd
import numpy as np

from fake_cms import Fcms

class Agent():
  def __init__(self, features, actions, batch_size, gamma, epilson):
    self.model = self.build(features, actions)
    self.memory = []
    self.first_time = True
    self.action_space = actions
    self.observation_space = features
    self.batch_size = batch_size
    self.gamma = gamma
    self.epilson = epilson

  def build(self, features, actions):
    model = Sequential()
    model.add(Dense(24, input_dim=features, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    model.compile(loss='mse', optimizer='adam')
    return model

  def store(self, transition):
    self.memory.append(transition)

  def act(self, state):
    if rnd.uniform(0, 1) < self.epilson and not self.first_time:
        self.first_time = False
        return rnd.randint(self.action_space - 1)
    return np.argmax(self.model.predict(state)[0])

  def optimise(self, done):
    batch = rnd.sample(self.memory, self.batch_size)
    for s, a, r, s_ in batch:
        target = r
        if not done:
            target = r + self.gamma * np.amax(self.model.predict(s_)[0])

        new_rewards = self.model.predict(s)
        new_rewards[0][a] = target

        self.model.fit(state, new_rewards, verbose=0)

EPISODES = 100000
STEPS = 250
AVERAGE = 10

if __name__ == '__main__':
  env = Fcms(1, 1, 3, 3, False)
  agent = Agent(5, len(env.action_space), 32, 0.95, 0.01)
	
  number_of_rewards = 0
  
  rewards = np.zeros(AVERAGE)

  for episode in range(EPISODES):
    env.reset()
    state = np.array(env.observation_keras())
    state = np.reshape(state, [1,5])

    total_reward = 0

    for step in range(STEPS):
      action = agent.act(state)

      _, reward, done, _ = env.step(action)
      # if done:
      #   print("See you next Tuesday?!", reward)

      next_state = np.array(env.observation_keras())
      next_state = np.reshape(next_state, [1,5])

      total_reward += reward

      agent.store((state, action, reward, next_state))
      state = next_state

      if done:
        agent.optimise(done)
        break
    
    # print(total_reward)
    rewards[number_of_rewards % AVERAGE] = total_reward
    # np.insert(rewards, number_of_rewards % AVERAGE, total_reward)
    number_of_rewards += 1
    if number_of_rewards % AVERAGE == 0:
      print(np.mean(rewards))
    
