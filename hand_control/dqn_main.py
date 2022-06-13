
import random
from agent import Agent
import serial
import cv2
import hand_tracting as ht
import time
import deep_q_net as dqn
import torch

class Enviorment():
    def __init__(self):
        super(Enviorment,self).__init__() #set 12 action for agent
        self.action_space = ['3000','0300','0030','-3000','0-300','00-30','300','030','003','-300','0-30','00-3','000']
        self.n_action = len(self.action_space)
        self.ser = serial.Serial('com3',115200,bytesize=8,timeout=1)
        # self.state = ht.search_state()
        self.cap = cv2.VideoCapture(1)
        self.cap.open(1)
        self.success, self.frame = self.cap.read()
        if self.success == True :
            self.frame,self.state = ht.process_frame(self.frame)#如果能够不开摄像头直接读取状态
            # cv2.imshow('my_window', self.frame)

            # if cv2.waitKey(1) in [ord('q'),27]: # 按键盘上的q或esc退出
            #     break
            if self.state >= 200:
                self.state = self.reset()
                print("camera is restarting")

    def step(self,action):
        self.action = self.action_space[action]
        if self.action == '3000':
            self.ser.write('01'.encode())
            self.ser.write('s'.encode())
            print('+')
        if self.action == '0300':
            self.ser.write('02'.encode())
            self.ser.write('s'.encode())
            print('+')
        if self.action == '0030':
            self.ser.write('03'.encode())
            self.ser.write('s'.encode())
            print('+')
        if self.action == '-3000':
            self.ser.write('04'.encode())
            self.ser.write('s'.encode())
            print('-')
        if self.action == '0-300':
            self.ser.write('05'.encode())
            self.ser.write('s'.encode())
            print('-')
        if self.action == '00-30':
            self.ser.write('06'.encode())
            self.ser.write('s'.encode())
            print('-')
        if self.action == '300':
            self.ser.write('07'.encode())
            self.ser.write('s'.encode())
            # print('-1+0')
        if self.action == '030':
            self.ser.write('08'.encode())
            self.ser.write('s'.encode())
            # print('1+0')
        if self.action == '003':
            self.ser.write('09'.encode())
            self.ser.write('s'.encode())
            # print('+0.1+0.1')
        if self.action == '-300':
            self.ser.write('10'.encode())
            self.ser.write('s'.encode())
        if self.action == '0-30':
            self.ser.write('11'.encode())
            self.ser.write('s'.encode())
            # print('+0.1-0.1')
        if self.action == '00-3':
            self.ser.write('12'.encode())
            self.ser.write('s'.encode())
            # print('-0.1+0.1')
        if self.action == '000':
            self.ser.write('13'.encode())
            self.ser.write('s'.encode())
            # print('00')
        self.success, self.frame = self.cap.read()
        if self.success == True :
            _,self.state = ht.process_frame(self.frame)#这里怎么读取一个状态？
        else : self.reset()
        # print(self.state)
        # print(self.state.type)
        done =  (int(self.state) <= 80 ) or (int(self.state) >=250)
        done = bool(done)

        if not done:
            reward = -1
        else:
            if int(self.state) <= 80:
                reward = 100
            else: reward = -100

        return self.state, reward,done,{}
    
    def reset(self):
        #self.cap.release()
        #self.cap.open(0)
        self.success, self.frame = self.cap.read()
        if self.success == True :
            _,self.state = ht.process_frame(self.frame)#如果能够不开摄像头直接读取状态
            self.ser.write('14'.encode())
            self.ser.write('s'.encode())
            print("cameera is restarting")
            # time.sleep(3)
            if self.state >= 200:
                self.state = self.reset()
        return self.state
    
    def close(self):
        self.cap.release()

if __name__ == "__main__":
    env = Enviorment()
    age = dqn.DQN()
    memory = dqn.RelayMemory(200)

    for episode in range (30):
        state = env.reset()
        done = False
        total_reward = 0
        actions = []
        total_rewards = []
        while not done:
            action = age.policy(state)
            state_, reward, done, info = env.step(action)
            #state_batch, action_batch, reward_batch, next_state_batch
            memory.append((state,action, reward, state_))
            state  = state_
            print(state)
        age.learn(memory,batch_size = 60)
        age.target_net.load_state_dict(age.act_net.state_dict())
    torch.save(age.target_net,'target_net.pth')
    torch.save(age.act_net,'act_net.pth')
    #print(state, reward, done, info)




####验证
    for episode in range (1):
        state = env.reset()
        
        done = False
        total_reward = 0
        actions = []
        total_rewards = []
        while not done:
            state = torch.tensor(state).reshape(1,1).float()
            index = torch.argmax(age.target_net(state))
            state_, reward, done, info = env.step(index)

            # action_ = age.learned_policy(state_)
            #state, action, reward, new_state, next_action
            # age.SARSAupdate(state,action,reward,state_,action_)
            # state,action = state_,action_
            print(state)
            total_reward += reward
            state = state_
        total_rewards.append(total_reward)
        print(total_reward)
