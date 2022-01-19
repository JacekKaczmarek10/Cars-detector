import requests
import cv2
import cv2 as cv
import numpy as np
from numpy import*
import json
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
#url ='http://ec2-18-224-21-114.us-east-2.compute.amazonaws.com:8000/get-parking-places'
#headers = "Content-Type=multipart/form-data"
#files = {'file': open('1.jpg', 'rb')}
#files = {'file': open('ss4.png', 'rb')}
#requests.post(url, files=files)
#params = {'name': 'marcin'}
#requests.get(url,params=params)
#cv2.imshow('D', D)

url ='http://ec2-18-224-21-114.us-east-2.compute.amazonaws.com:8000/get-parking-places'
params = {'name': 'black'} 
x=requests.get(url,params=params)
print(x.content)
json_data=json.loads(x.text)



print(json_data['name'])
x1=json_data['parkingPlaceResponseList'][0]['x_1']
print(x1)
coordinates = zeros((5,4,2),float)
if json_data['name']=='black':
    f=0
    g=1
    
    while(g):
        
        if json_data['parkingPlaceResponseList'][f]['id']==f+1:
            print('XDDDDDDDDD')
            coordinates[f][0][0]=json_data['parkingPlaceResponseList'][f]['x_1']
            coordinates[f][0][1]=json_data['parkingPlaceResponseList'][f]['y_1']
            
            coordinates[f][1][0]=json_data['parkingPlaceResponseList'][f]['x_2']
            coordinates[f][1][1]=json_data['parkingPlaceResponseList'][f]['y_2']
            
            coordinates[f][2][0]=json_data['parkingPlaceResponseList'][f]['x_3']
            coordinates[f][2][1]=json_data['parkingPlaceResponseList'][f]['y_3']
            
            coordinates[f][3][0]=json_data['parkingPlaceResponseList'][f]['x_4']
            coordinates[f][3][1]=json_data['parkingPlaceResponseList'][f]['y_4']
            f+=1
        if json_data['parkingPlaceResponseList'][f]['id']!=f+1:
            break
print(coordinates)
#print(c1)
cv2.waitKey()
cv2.destroyAllWindows()