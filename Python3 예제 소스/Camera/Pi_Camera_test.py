# -*- coding: utf-8 -*-

import cv2, sys
import numpy as np
#from common import clock, draw_str
import platform


def draw_str(dst, target, s):
    x, y = target
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness = 2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)

def clock():
    return cv2.getTickCount() / cv2.getTickFrequency()


print ("-------------------------------------")
print ("(2020-1-15) Camera Frame check")
print ("")
os_version = platform.platform()
print (" ---> OS " + os_version)
python_version = ".".join(map(str, sys.version_info[:3]))
print (" ---> Python " + python_version)
opencv_version = cv2.__version__
print (" ---> OpenCV  " + opencv_version)



W_View_size = 320
H_View_size = int(W_View_size / 1.333)

#W_View_size = 640
#H_View_size = int(W_View_size / 1.777)

'''
W_View_size = 320
H_View_size = 240

W_View_size = 640
H_View_size = 480

W_View_size = 800
H_View_size = 600


W_View_size = 1280
H_View_size = 300
'''

FPS         = 90  #PI CAMERA: 320 x 240 = MAX 90

print (" ---> View Size: " + str(W_View_size) + " x " + str(H_View_size))
print (" ---> FPS: " + str(FPS))
print ("-------------------------------------")


#-------------------------------------

cap = cv2.VideoCapture(0)

cap.set(3, W_View_size)
cap.set(4, H_View_size)
cap.set(5, FPS)  



old_time = clock()
View_select = 1

# loop
while True:
    # ------ read frame buffer from camera
    ret, img = cap.read()
    if not ret:
      break

    #  ------ FPS  ------   
    Frame_time = 1000 / ((clock() - old_time) * 1000.)
    old_time = clock()
    
    #  ------ view select ------ 
    if View_select == 1:
        draw_str(img, (5, 20), str(W_View_size) + " x " + str(H_View_size) + ' = FPS %.1f ' % (Frame_time))
        cv2.imshow('Video Test', img)
    else:
        print(" " + str(W_View_size) + " x " + str(H_View_size) + " = FPS %.1f " % (Frame_time ))

   
    #  ------ keyboad press event  ------ 
    key = 0xFF & cv2.waitKey(1)
    if key == 27:  # ESC  Key
        break
    elif key == ord(' '):  # spacebar Key
        if View_select == 0:
            View_select = 1
        else:
            View_select = 0
