import requests
import cv2
import cv2 as cv
import numpy as np
#url = 'https://docs.google.com/document/d/1q1IScJkOxaG5J_c7VdpHQcs9QbgSpDAqo69yfzezeKk/edit'
#url = 'http://ec2-18-224-21-114.us-east-2.compute.amazonaws.com:8000/add-parking'
#BODY= {"numberOfRows" : 6,"numberOfColumns" : 6,"name" : "Razzberka"}
#x = requests.post(url,headers={"content-type":"application/json"} , data = BODY)
#print(x.text)

#url = 'http://ec2-18-224-21-114.us-east-2.compute.amazonaws.com:8000/add-parking'
#params = {'numberOfRows': 180, 'numberOfColumns': 189, 'name': 'ala'}

#x = requests.post(url,params=params,headers={"Content-Type": "application/json"})

#print(x.text)
#cv2.namedWindow('D')

#D = cv2.imread('1.jpg')



url ='http://ec2-18-224-21-114.us-east-2.compute.amazonaws.com:8000/get-parking-places'
#headers = "Content-Type=multipart/form-data"
#files = {'file': open('1.jpg', 'rb')}
#files = {'file': open('ss4.png', 'rb')}
#requests.post(url, files=files)
params = {'name': 'marcin'}
requests.get(url,params=params)
#cv2.imshow('D', D)
cv2.waitKey()
cv2.destroyAllWindows()