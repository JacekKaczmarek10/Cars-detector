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


miejsca_wysyłka=zeros((3),int)
miejsca_wysyłka[1]=0
miejsca_wysyłka[2]=1
miejsca_wysyłka[0]=1
name="trzy"
url = 'http://ec2-18-224-21-114.us-east-2.compute.amazonaws.com:8000/change-parking-place'
BODY= {"parkingPlaces":miejsca_wysyłka,"name": name}
x = requests.post(url, data = BODY)
    
print("wysłałem  parking:",name)


    
        
    


