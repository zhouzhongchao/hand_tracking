from time import sleep
import serial
import time
chuankou = serial.Serial('com3',115200,bytesize=8,timeout=0.5)

for i in range(10):
    chuankou.write('01'.encode())
    chuankou.write('s'.encode())
    # time.sleep(1)
    chuankou.write('02'.encode())
    chuankou.write('s'.encode())
    chuankou.write('03'.encode())
    chuankou.write('s'.encode())
    #ut = chuankou.read(20) 
    #print(out)