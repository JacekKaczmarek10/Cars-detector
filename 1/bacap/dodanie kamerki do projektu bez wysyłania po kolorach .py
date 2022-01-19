from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library
import sys
import cv2 as cv
import numpy as np
import argparse
import random as rng
import requests
from numpy import*
import json

r1=1280
r2=720
# Initialize the camera
camera = PiCamera()
 
# Set the camera resolution
camera.resolution = (r1, r2)

# Set the number of frames per second
camera.framerate = 30
 
# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(r1, r2))
 
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.5)

lczbamc=0
lczbamw=0 
coordinates = zeros((20,4,2),float)
miejsca=zeros((14),int)
x1=0
y1=0
z1=0

#funkcjia zczytujaca miejca parkingowe na podstawie kliknięć urzytkowinika
def draw_P(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global x1
        global y1
        global z1
        global lczbamc
        
        coordinates[x1][y1][z1]=x
        coordinates[x1][y1][z1+1]=y
        y1=y1+1
        
        if y1==4:
            miejsca[x1]=1
            lczbamc+=1
            x1=x1+1
            y1=0
            p11=coordinates[x1-1][y1][z1]
            p12=coordinates[x1-1][y1][z1+1]
            p21=coordinates[x1-1][y1+1][z1]
            p22=coordinates[x1-1][y1+1][z1+1]
            p31=coordinates[x1-1][y1+2][z1]
            p32=coordinates[x1-1][y1+2][z1+1]
            p41=coordinates[x1-1][y1+3][z1]
            p42=coordinates[x1-1][y1+3][z1+1]
            p11=int(p11)
            p12=int(p12)
            p22=int(p22)
            p21=int(p21)
            
            p31=int(p31)
            p32=int(p32)
            p41=int(p41)
            p42=int(p42)
            
            cv.line(pusty, (p11,p12),(p21,p22), (255, 0, 0), 1)
            cv.line(pusty, (p31,p32),(p21,p22), (255, 0, 0), 1)
            cv.line(pusty, (p11,p12),(p41,p42), (255, 0, 0), 1)
            cv.line(pusty, (p41,p42),(p31,p32), (255, 0, 0), 1)

def thresh_callback(val):
    threshold = val

    canny_output = cv.Canny(src_gray, threshold, threshold * 2)

    contours, hierarchy = cv.findContours(canny_output, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    
    
    for i in range(len(contours)):
        color = (255)
        cv.drawContours(drawing, contours, i, color, 2, cv.LINE_8, hierarchy, 0)
        
    #cv.imshow('Contours', drawing)
    return contours

#funkcjia obliczajaca wzór na podstawie 2 pkt 
def W_F(x1,y1,x2,y2):
    if x1==x2:
        a=10000
        b=x1*10000
        return a,b
    a=(y1-y2)/(x1-x2)
    b=y1-a*x1
    return a,b
#funkcjia sprawdzajaca po której stronie znajdzuję się punkt 
def W_Sp(a1,b1,a2,b2,cx,cy):
    if cy>=a1*cx+b1:
        if cy>=a2*cx+b2:
            return 0 
    if cy>a1*cx+b1:
        if cy<a2*cx+b2:
            return 1
    if cy<a1*cx+b1:
        if cy>a2*cx+b2:
            return 2
    if cy<=a1*cx+b1:
        if cy<=a2*cx+b2:
            return 3 

l=0
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    #src = frame.array
    if l==0:
        src1=frame.array
        src2=frame.array
        
    if l==1:
        src1=src2
        src2=frame.array
        
    key = cv2.waitKey(1) & 0xFF
    #cv.imshow("src", src)
    pusty=src1
    print(1)
    if l==0:
        l=1
        f=1
        cv2.namedWindow('pusty')
        cv2.setMouseCallback('pusty',draw_P)
        while(f):
            cv2.imshow('pusty',pusty)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    print("liczy...")
    
    
    
    #znalezienie różnic
    diff=cv2.absdiff(src1,src2)
    image=diff
    cv.imshow("diff", diff)
    
    #przygotowanie obrazu
    blur = cv2.pyrMeanShiftFiltering(image, 11, 21)
    src_gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    #wyszukanie krawędzi w obrazie rużnic 
    threshold = 60
    kra=thresh_callback(threshold)
    
    
    
    
    #cv.waitKey(0)
    raw_capture.truncate(0)

    
        
    


