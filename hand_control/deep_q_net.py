import q_network as q
import collections
import random
import numpy as np
import torch.optim as optim
import torch.nn as nn
import torch
class RelayMemory():
    def __init__(self,max_size):
        self.buffer = collections.deque(maxlen = max_size)#不太懂什么意思

    def append(self,exp):
        self.buffer.append(exp)  


    def sample(self,batch_size):
        if batch_size>=len(self.buffer):
            batch_size = len(self.buffer)
        mini_batch = random.sample(self.buffer,batch_size)
        state_batch, action_batch, reward_batch, next_state_batch = [], [], [], []
        for experience in mini_batch:
            s,a,r,s_p = experience
            state_batch.append(s)
            action_batch.append(a)
            reward_batch.append(r)
            next_state_batch.append(s_p)
        return np.array(state_batch).astype('float32'), np.array(action_batch).astype('float32'),\
                np.array(reward_batch).astype('float32'), np.array(next_state_batch).astype('float32')

class DQN():
    
    def __init__(self):
        super(DQN, self).__init__()
        self.target_net,self.act_net = q.Net(1,13),q.Net(1,13)
        self.learning_rate = 0.03
        self.optimizer = optim.Adam(self.act_net.parameters(),self.learning_rate )
        self.loss_func = nn.MSELoss()
        self.gamma = 0.995
    def policy(self,state):
        state = torch.tensor(state)
        # print(state)
        state = torch.tensor(state).reshape(1,1).float()
        value  = self.act_net(state)
        action_max_value, index = torch.max(value,1)
        action = index

        if np.random.rand(1) >= 0.9:
            action = random.randint(0,11)
        return action

    def learn(self,memory,batch_size):
        state_batch, action_batch, reward_batch,next_state_batch = memory.sample(batch_size)
        print(state_batch)
        # for state, action, reward, next_state in state_batch,action_batch,reward_batch,next_state_batch:
        #     with torch.no_grad():
        #         next_state = torch.tesnor(next_state)
        #         index = torch.argmax(self.target_net(next_state))
        #         trage_v = reward + self.gamma*self.target_net(next_state).max(1)
        #     v = (self.act_net(state).gather(1, action))[index]
        #     loss = self.loss_func(trage_v,v)
        #     for _ in range(50):
        #         self.optimizer.zero_grad()
        #         loss.backward()
        #         self.optimizer.step()
        for i in range(len(state_batch)):
            with torch.no_grad():
                next_state = torch.tensor(next_state_batch[i]).reshape(1,1).float()
                index = torch.argmax(self.target_net(next_state))
                a = torch.max(self.target_net(next_state))
                print(a)
                trage_v = reward_batch[i] + self.gamma*torch.max(self.target_net(next_state)) #按照q learning的更新方式找到这个state的q（s,a）是多少
            state_batch_input = torch.tensor(state_batch[i]).reshape(1,1).float()
            v = (self.act_net(state_batch_input))
            print(v)
            v = (self.act_net(state_batch_input))[0,index]#利用网络得到这个点的q(s,a)是多少 然后让这个两个相减
            loss = self.loss_func(trage_v,v)
            
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
