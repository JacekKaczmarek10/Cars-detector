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
r1=640
r2=480
p=29
h=p*(-1000)
print(h)
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


l=0
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    #src = frame.array

    src2=frame.array
        

        
    key = cv2.waitKey(1) & 0xFF
    #cv.imshow("src", src)
    name='xd'
    miejsca_wysyłka=zeros((2),int)
    BODY= {"parkingPlaces[]":miejsca_wysyłka,"name": name}
    cv.imshow("wyj", src2)
    #cv.waitKey(0)
    raw_capture.truncate(0)

    
        
    


