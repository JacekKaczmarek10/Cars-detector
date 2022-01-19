#from __future__ import print_function
#from math import sqrt 
#from picamera.array import PiRGBArray # Generates a 3D RGB array
#from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import sys
import cv2 as cv
import numpy as np
import argparse
import random as rng
import cv2 # OpenCV library
import requests
# Initialize the camera
#camera = PiCamera()
 
# Set the camera resolution
#camera.resolution = (640, 480)

# Set the number of frames per second
#camera.framerate = 60

# Generates a 3D RGB array and stores it in rawCapture
#raw_capture = PiRGBArray(camera, size=(640, 480))

# Wait a certain number of seconds to allow the camera time to warmup
#time.sleep(0.1)
#i=0
#op=0

for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    
    src = frame.array
    
    key = cv2.waitKey(1) & 0xFF
    
    if i<1:
        src1 = src
        i+=1
    diff=cv2.absdiff(src,src1)
 
    src1=src
    
    src_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    src_gray = cv.blur(src_gray, (3,3))
    
    op+=1
    
   # print(op)
   # x=time.perf_counter()

   # print("Czas:",x)
    thresh = 100 
    ff=thresh_callback(thresh)
    if op<2:
        x=time.perf_counter()
    if op==62:
        y=time.perf_counter()
        z=y-x
        print("Czas:",z)
    #print("Pozycjia kaplsa:",ff)
    #cv.waitKey(0)
    raw_capture.truncate(0)
    

