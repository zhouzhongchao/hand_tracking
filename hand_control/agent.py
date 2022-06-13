
import numpy as np
import random

class Agent():
    def __init__(self,epsilon,discount):
        self.learning_rate = 0.1
        #self.env = Enviorment()
        self.epsilon  = epsilon # 定义探索和利用的比例
        self.discount = discount
        self.Q_table = np.zeros(13000).reshape(1000,13)#记录共130个状态 13个动作
    def policy(self, state):
        # the agent here: it chooses random action for epsilon probability otherwise it exploits
        if (np.random.random() < self.epsilon):
            return random.randint(0,11)
        else:
            return np.argmax(self.Q_table[state])
    def learned_policy(self, state):
        # the agent here: it chooses random action for epsilon probability otherwise it exploits
            return np.argmax(self.Q_table[state])
    def SARSAupdate(self, state, action, reward, new_state, next_action):
        # TD error
        #print(state,action)
        delta = (reward + self.discount * self.Q_table[new_state][next_action] - self.Q_table[state][action])
        # update q table
        self.Q_table[state][action] += self.learning_rate * delta