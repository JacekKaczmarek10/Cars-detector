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
#color=0
r1=640
r2=480

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
    x1=0
    y1=0
    z1=0
    d1=1
    l=0
    if l==0:
        #src2=frame.array
        pusty=frame.array
        scr10=frame.array
        print("pierwsza pętla")
    src2=frame.array
    
    
    n_plik='1.jpg'
    cv2.imwrite(n_plik,pusty)
    key = cv2.waitKey(1) & 0xFF
    raw_capture.truncate(0)