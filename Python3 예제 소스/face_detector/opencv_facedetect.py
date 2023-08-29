#!/usr/bin/env python



# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2

from common import clock, draw_str
import imutils

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.35, minNeighbors=4, minSize=(30, 30),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

if __name__ == '__main__':
    import sys, getopt
    #print(__doc__)
    
    W_View_size = 320
    #H_View_size = int(W_View_size / 1.777)
    H_View_size = int(W_View_size / 1.333)


    cap = cv2.VideoCapture(0)
    cap.set(3, W_View_size)
    cap.set(4, H_View_size)
    

    face_cascade = cv2.CascadeClassifier( './frontalface_1.xml')


    t = clock()
    dt = clock() - t
    
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        vis = img.copy()

        for (x, y, w, h) in faces:
            cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 255, 0), 1)

            
        
        draw_str(vis, (5, 15), 'Time: %.1f ms' % (dt * 1000))
        draw_str(vis, (5, H_View_size-5), 'Exit = ESC Key')
        
        
        dt = clock() - t
        t = clock()
        cv2.imshow('OpenCV Facedetect', vis)
        
        
        if 0xFF & cv2.waitKey(1) == 27:  # ESC  Key
            break
    cv2.destroyAllWindows()
