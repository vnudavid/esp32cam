#usr/bin/python3
# -*- coding: utf-8 -*-
import serial
import numpy as np
import cv2
from time import sleep
path = 'param.txt'
f = open(path, 'r')
lines = f.readlines()
def recv(serial2):
  while 1:
    data=serial2.read(4096)
    if data=='':
      continue
    else:
      break
    sleep(0.02)
  return data
ser=serial.Serial(lines[0][:-1],int(lines[1]),timeout=0.02)
img = b'' #字節連接，定義全局字節變量以備使用
recev = 0 #接收標誌位
ser.write(b'1')
while 1:
  data = recv(ser)
  if data:
     if (b'\xff\xd8' in data) or (recev):
         recev = 1
         img += data
         print('開始接收圖片:',len(img))
         #sleep(0.02)
     if b'\xff\xd9' in data:
       print('接收圖片完成：',len(img))
       nparr = np.frombuffer(img, np.uint8)
       print(nparr.shape[0])
       if nparr.shape[0]>=5000:
           try:
             img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
             cv2.imshow('test',img_np)
             cv2.waitKey(1)
           except:
             pass
       img = b''
       recev = 0
       ser.flushInput()
  else:
    print("timeout")
    img = b''
    recev = 0
    ser.flushInput()
    ser.write(b'1')  