from __future__ import print_function
from math import sqrt 
from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import sys
import cv2 as cv
import numpy as np
import argparse
import random as rng
import cv2 # OpenCV library

def thresh_callback(val):
    threshold = val

    canny_output = cv.Canny(src_gray, threshold, threshold * 2)

    contours, hierarchy = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    #contours, hierarchy = cv.findContours(canny_output, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
  
    m=len(contours)

    Poz=0
    if m!=0:
        w = [0,0]
        w[0] = contours[0][0][0][0]
        w[1] = contours[0][0][0][1]
        
        contours.reverse()
        
        n = [0,0]
        n[0] = contours[0][0][0][0]
        n[1] = contours[0][0][0][1]
        
        #print(w)
        #print(n)
        
        Poz=(w[1]+n[1])/2
        print(w[1])
        print(n[1])
        print(Poz)
    #print(contours)
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        color = (55, 255, 255)
        cv.drawContours(drawing, contours, i, color, 2, cv.LINE_8, hierarchy, 0)
    
    #cv.imshow('XD', drawing)
    cv.imwrite("XD1.png",drawing)
    return Poz

g1=cv2.imread(cv.samples.findFile("1.jpg"))
g2=cv2.imread(cv.samples.findFile("2.jpg"))
diff1=cv2.absdiff(g1,g2)
#print(diff1)
  
#for i in range

   # diff1.reverse()
        
   
#cv.imshow("diff", diff1)
cv.imwrite("XD.png",diff1)
src_gray = cv.cvtColor(diff1, cv.COLOR_BGR2GRAY)
src_gray = cv.blur(src_gray, (3,3))
    

    
thresh = 60

thresh_callback(thresh)

