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
time.sleep(1)

lczbamc=0
lczbamw=0 
#coordinates = zeros((20,4,2),float)
#BL = zeros((20,2),float)
#miejsca=zeros((14),int)


#funkcjia zczytujaca miejca parkingowe na podstawie kliknięć urzytkowinika
def draw_P(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global x1
        global y1
        global z1
        global lczbamc
        global d1
        if y1<5 and d1==1:
            coordinates[x1][y1][z1]=x
            coordinates[x1][y1][z1+1]=y
            y1=y1+1
            
            print("dodąłeś puntk:",y1)
        #if d1==0:
            #BL[x1-1][0]=x
            #BL[x1-1][1]=y
            #d1=1
            #print("miejce dodane")
        if y1==4 and d1==1:
            d1=1
            #print("4 pkt dodaje jeszcze 1")
            print("miejce dodane")
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
            
            #cv.line(pusty, (p11,p12),(p21,p22), (255, 0, 0), 1)
            #cv.line(pusty, (p31,p32),(p21,p22), (255, 0, 0), 1)
            #cv.line(pusty, (p11,p12),(p41,p42), (255, 0, 0), 1)
            #cv.line(pusty, (p41,p42),(p31,p32), (255, 0, 0), 1)

def thresh_callback(val):
    threshold = val

    canny_output = cv.Canny(src_gray, threshold, threshold * 2)

    contours, hierarchy = cv.findContours(canny_output, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    
    
    for i in range(len(contours)):
        color = (255)
        cv.drawContours(drawing, contours, i, color, 2, cv.LINE_8, hierarchy, 0)
    
    cv.imshow('Contours', drawing)
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
u=0
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    #src = frame.array
    x1=0
    y1=0
    z1=0
    d1=1
    if l==0:
        #src2=frame.array
        pusty=frame.array
        scr10=frame.array
        print("pierwsza pętla")
        n_plik='1.jpg'
        cv2.imwrite(n_plik,pusty)
    src2=frame.array
    
    
   
    #@dodawanie nowego parkingu
    if l==0:
        name="Parking1"
        url = 'http://ec2-18-224-21-114.us-east-2.compute.amazonaws.com:8000/add-parking'
        BODY= {"name" :name ,"numberOfPlaces" : 10,"city" : "Poznań","postalCode":"60-461","street":"saturn",
               "number":5,"isGuarded":"true","email":"test15@test.pl","phoneNumber":"153555789"}
        x = requests.post(url, data = BODY)
        print("utworzyłem parking:",name)
        #@wysyłąnie zdiecia
        url='http://ec2-18-224-21-114.us-east-2.compute.amazonaws.com:8000/add-parking-image'
        files = {'file': open('1.jpg', 'rb')}
        params = {'name': name}
        requests.post(url, files=files,params=params)
        #@dostawanie punktów
        url ='http://ec2-18-224-21-114.us-east-2.compute.amazonaws.com:8000/get-parking-places'
        params = {'name': name}
        u=1
        while(u):
            print("czekam")
            x=requests.get(url,params=params)
            json_data=json.loads(x.text)
            if json_data['name']==name:
                if json_data['placesNumber']>0:
                    p=json_data['placesNumber']
                    coordinates = zeros((p,4,2),float)
                    miejsca=zeros((p),int)
                    miejsca_wysyłka=zeros((p),int)
                    #g=json_data['parkingPlaceResponseList']
                    for f in range(len(miejsca)):
                        coordinates[f][0][0]=json_data['parkingPlaceResponseList'][f]['x_1']
                        coordinates[f][0][1]=json_data['parkingPlaceResponseList'][f]['y_1']
                        coordinates[f][1][0]=json_data['parkingPlaceResponseList'][f]['x_2']
                        coordinates[f][1][1]=json_data['parkingPlaceResponseList'][f]['y_2']
                        coordinates[f][2][0]=json_data['parkingPlaceResponseList'][f]['x_3']
                        coordinates[f][2][1]=json_data['parkingPlaceResponseList'][f]['y_3']
                        coordinates[f][3][0]=json_data['parkingPlaceResponseList'][f]['x_4']
                        coordinates[f][3][1]=json_data['parkingPlaceResponseList'][f]['y_4']
                    break
            time.sleep(5)
        
        
    #if l==1:
        #src1=src2
        #src2=frame.array
    
    key = cv2.waitKey(1) & 0xFF
    
    #cv.imshow("scr10", scr10)
    #pusty=src1
    #print(u)
    #u+=1
    print("--------------------------------")
    l=1
    if l==5:
        l=1
        f=1
        cv2.namedWindow('pusty')
        cv2.setMouseCallback('pusty',draw_P)
        while(f):
            cv2.imshow('pusty',pusty)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
                
        print("liczy...")
    

    #cv.imshow("scr10", scr10)
    #cv.imshow("src2", src2)
    #znalezienie różnic
    img1=cv2.imread('1.jpg')
    diff=cv2.absdiff(img1,src2)
    #diff=cv2.absdiff(scr10,src2)
    image=diff
    #cv.imshow("diff", diff)
    
    #przygotowanie obrazu
    blur = cv2.pyrMeanShiftFiltering(image, 11, 21)
    src_gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    #wyszukanie krawędzi w obrazie rużnic 
    threshold = 200
    kra=thresh_callback(threshold)
    
#pętla sppawdzajaca czy dane mijece jest zjęte
    g=0
    for j in range(len(miejsca)):
        if miejsca[g]==0:
            #print("sprawdza co i jak")
            x1=g+1
            y1=0
            z1=0
            g+=1
#spisywanie pkt z tablicy dla ułatwienia operacji na nich 
            p11=coordinates[x1-1][y1][z1]
            p12=coordinates[x1-1][y1][z1+1]
            p21=coordinates[x1-1][y1+1][z1]
            p22=coordinates[x1-1][y1+1][z1+1]
            p31=coordinates[x1-1][y1+2][z1]
            p32=coordinates[x1-1][y1+2][z1+1]
            p41=coordinates[x1-1][y1+3][z1]
            p42=coordinates[x1-1][y1+3][z1+1]
#rzutowanie aby umożliwić funkcji rysowanie pkt 
            p11=int(p11)
            p12=int(p12)
            p22=int(p22)
            p21=int(p21)    
            p31=int(p31)
            p32=int(p32)
            p41=int(p41)
            p42=int(p42)
            s=0
            a=0
            b=0
#wylicznie wzorów prostych
            a1,b1=W_F(p11,p12,p21,p22)
            a2,b2=W_F(p21,p22,p31,p32)
            a3,b3=W_F(p31,p32,p41,p42)
            a4,b4=W_F(p41,p42,p11,p12)
#spawdzanie po której stronie znajduje sie 4 pkt miejca parkingowego 
            Oriet1=W_Sp(a1,b1,a2,b2,p41,p42)
            Oriet2=W_Sp(a2,b2,a3,b3,p11,p12)
            Oriet3=W_Sp(a3,b3,a4,b4,p21,p22)
            Oriet4=W_Sp(a4,b4,a1,b1,p31,p32)
#spawdzanie czy jakaś krewędz znajduję sie w zanzanczonym opszarze
            while s<=len(kra)-1:
                k1=kra[s][0][0][0]
                k2=kra[s][0][0][1]
                spr1=W_Sp(a1,b1,a2,b2,k1,k2)
                if spr1==Oriet1:
                    #print("1 argument tak")
                    spr2=W_Sp(a2,b2,a3,b3,k1,k2)
                    if spr2==Oriet2:
                        spr3=W_Sp(a3,b3,a4,b4,k1,k2)
                        #print("2 argument tak")
                        if spr3==Oriet3:
                            spr4=W_Sp(a4,b4,a1,b1,k1,k2)
                            #print("3 argument tak")
                            if spr4==Oriet4:
                                miejsca[g-1]=2
                                #print("4 argument tak")
                                s=len(kra)                                      
                s+=1
                
            if miejsca[g-1]==0:
                miejsca[g-1]=1
            #miejsca_wysyłka[g-1]=miejsca[g-1]    
    #pętla rysjujaca miejce
    #wyj=src2
    g=0
    for i in range(len(miejsca)):
        x1=g+1
        y1=0
        z1=0
#spisywanie pkt z tablicy dla ułatwienia operacji na nich 
        p11=coordinates[x1-1][y1][z1]
        p12=coordinates[x1-1][y1][z1+1]
        p21=coordinates[x1-1][y1+1][z1]
        p22=coordinates[x1-1][y1+1][z1+1]
        p31=coordinates[x1-1][y1+2][z1]
        p32=coordinates[x1-1][y1+2][z1+1]
        p41=coordinates[x1-1][y1+3][z1]
        p42=coordinates[x1-1][y1+3][z1+1]
#rzutowanie aby umożliwić funkcji rysowanie pkt 
        p11=int(p11)
        p12=int(p12)
        p22=int(p22)
        p21=int(p21)    
        p31=int(p31)
        p32=int(p32)
        p41=int(p41)
        p42=int(p42)
#sprawdzanie danego miejsca
        
        if miejsca[g]==2:
            color=color=(0, 0, 255)
            miejsca_wysyłka[g]=0
            #print ("zajęte miejce ",g)
        if miejsca[g]==1:
            color=color=(0, 255, 0)
            miejsca_wysyłka[g]=1
            
            #print ("wolne miejce ",g)
        
#rysowanie miejsc
        
        if miejsca[g]==2 or miejsca[g]==1:
            #print("rysuje linie")
            cv.line(src2, (p11,p12),(p21,p22), color, 1)
            cv.line(src2, (p31,p32),(p21,p22), color, 1)
            cv.line(src2, (p11,p12),(p41,p42), color, 1)
            cv.line(src2, (p41,p42),(p31,p32), color, 1)
            miejsca[g]=0
        g+=1
    lczbamc=len(miejsca)
    lczbamw=0
    for h in range(len(miejsca)):
        if miejsca_wysyłka[h]==1:
            lczbamw+=1
    print("liczba miejc wolnych",lczbamw)
    print("liczba miejc całkowitych",lczbamc)
    cv.imshow("src2", src2)
    
    w_plik='2.jpg'
    cv2.imwrite(w_plik,src2)
    url='http://ec2-18-224-21-114.us-east-2.compute.amazonaws.com:8000/add-parking-image'
    files = {'file': open('2.jpg', 'rb')}
    #files = src2
    params = {'name': name}
    requests.post(url, files=files,params=params)
    
    #name="trzy"
    url = 'http://ec2-18-224-21-114.us-east-2.compute.amazonaws.com:8000/change-parking-place'
    BODY= {"parkingPlaces":miejsca_wysyłka,"name": name}
    x = requests.post(url, data = BODY)
    
    print("wysłałem  parking:",name)

    #cv.waitKey(0)
    raw_capture.truncate(0)

    
        
    


