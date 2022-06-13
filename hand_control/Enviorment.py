# import numpy as np
# import hand_tracting as ht
# import cv2
# import serial

# class Enviorment():
#     def __init__(self):
#         super(Enviorment,self).__init__() #set 12 action for agent
#         self.action_space = ['+1+1','-1-1','+1-1','-1+1','0+1','0-1','-1+0','1+0','+0.1+0.1','-0.1-0.1','+0.1-0.1','-0.1+0.1','00']
#         self.n_action = len(self.action_space)
#         self.ser = serial.Serial('com3',115200,bytesize=8,timeout=0.1)
#         # self.state = ht.search_state()
#         self.cap = cv2.VideoCapture(0)
#         self.cap.open(0)
#         self.success, frame = self.cap.read()
#         if self.success == True :
#             frame,self.state = ht.process_frame(frame)#如果能够不开摄像头直接读取状态
#             if self.state > 900:
#                 self.state = self.reset()

#     def step(self,action):
#         self.action = self.action_space[action]
#         if self.action == '+1+1':
#             self.ser.write('+1+1'.encode())
#             print('+1+1')
#         if self.action == '-1-1':
#             self.ser.write('-1-1'.encode())
#             print('-1-1')
#         if self.action == '+1-1':
#             self.ser.write('+1-1'.encode())
#             print('+1-1')
#         if self.action == '-1+1':
#             self.ser.write('-1+1'.encode())
#             print('-1+1')
#         if self.action == '0+1':
#             self.ser.write('0+1'.encode())
#             print('0+1')
#         if self.action == '0-1':
#             self.ser.write('0-1'.encode())
#             print('0-1')
#         if self.action == '-1+0':
#             self.ser.write('-1+0'.encode())
#             print('-1+0')
#         if self.action == '1+0':
#             self.ser.write('1+0'.encode())
#             print('1+0')
#         if self.action == '+0.1+0.1':
#             self.ser.write('+0.1+0.1'.encode)
#             print('+1-1')
#         if self.action == '-0.1-0.1':
#             self.ser.write('-0.1-0.1'.encode())
#             print('-0.1-0.1')
#         if self.action == '+0.1-0.1':
#             self.ser.write('+0.1-0.1'.encode())
#             print('+0.1-0.1')
#         if self.action == '-0.1+0.1':
#             self.ser.write('-0.1+0.1'.encode())
#             print('-0.1+0.1')
#         if self.action == '00':
#             self.ser.write('00'.encode())
#             print('00')
#         self.success, frame = self.cap.read()
#         if self.success == True :
#             _,self.state = ht.process_frame(frame)#这里怎么读取一个状态？
#         else : self.reset()
#         # print(self.state)
#         # print(self.state.type)
#         done =  (int(self.state) <= 50 ) or (int(self.state) >=180)
#         done = bool(done)

#         if not done:
#             reward = -1
#         else:
#             if int(self.state) <= 50:
#                 reward = 100
#             else: reward = -100

#         return self.state, reward,done,{}
    
#     def reset(self):
#         self.cap.release()
#         self.cap.open(0)
#         self.success, frame = self.cap.read()
#         if self.success == True :
#             _,self.state = ht.process_frame(frame)#如果能够不开摄像头直接读取状态
#             if self.state > 900:
#                 self.state = self.reset()
#         return self.state
    
#     def close(self):
#         self.cap.release()



# # if __name__ == '__main__':

# #     env = Enviorment()
# # for i in range(100):
# #     total_action = np.arange(12)
# #     total_action = 1
# #     print(total_action)
# #     state, reward, done,_ = env.step(total_action)
# #     print(state,reward,done)
# #     #print(env.state)

