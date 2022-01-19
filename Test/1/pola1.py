import cv2
import cv2 as cv
import numpy as np
from numpy import*

coordinates = zeros((20,4,2),float)
x1=0
y1=0
z1=0
# mouse callback function
def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global x1
        global y1
        global z1
        #cv2.circle(image1,(x,y),100,(255,0,0),-1)
        coordinates[x1][y1][z1]=x
        coordinates[x1][y1][z1+1]=y
        y1=y1+1
        #y1=0
        if y1==4:
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
            #print(p11)
            #print(coordinates)
            cv.line(image1, (p11,p12),(p21,p22), (255, 0, 0), 1)
            cv.line(image1, (p31,p32),(p21,p22), (255, 0, 0), 1)
            cv.line(image1, (p11,p12),(p41,p42), (255, 0, 0), 1)
            cv.line(image1, (p41,p42),(p31,p32), (255, 0, 0), 1)

# Create a black image, a window and bind the function to window
#img = np.zeros((512,512,3), np.uint8)
image1 = cv2.imread('1.jpg')
cv2.namedWindow('image1')
cv2.setMouseCallback('image1',draw_circle)
f=1
while(f):
    cv2.imshow('image1',image1)
    #if cv2.waitKey(20) & 0xFF == 27:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        f=0
        #break
x1=0
y1=0
z=0



#g1=cv2.imread(cv.samples.findFile("1.jpg"))
g1 = cv2.imread('1.jpg')
g2 = cv2.imread('2.jpg')
#g2=cv2.imread(cv.samples.findFile("2.jpg"))
diff1=cv2.absdiff(g1,g2)

image=diff1
#image = cv2.imread('test1.png')
#image = cv2.imread('2.jpg')
#image = cv2.imread('1.jpg')
blur = cv2.pyrMeanShiftFiltering(image, 11, 21)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.015 * peri, True)
    if len(approx) == 4:
        x,y,w,h = cv2.boundingRect(approx)
        cv2.rectangle(image,(x,y),(x+w,y+h),(36,255,12),2)

r = cv2.imread('2.jpg')
for i in range(1,20):

    y1=y1+1
    if y1==4:
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
            #print(p11)
        print(coordinates)
        kg=0
        kd=0
        kl=0
        kp=0
######################################################
        if p11>=p21:
            kp=p11
        else:
            kp=p21
        if p31>kp:
            kp=p31
        if p41>kp:
            kp=p41
######################################################
        if p11<=p21:
            kl=p11
        else:
            kl=p21
        if p31<kl:
            kl=p31
        if p41<kl:
            kl=p41
######################################################
        if p12>=p22:
            kd=p12
        else:
            kd=p22
        if p32>kd:
            kp=p32
        if p42>kd:
            kd=p42
######################################################
        if p12<=p22:
            kg=p12
        else:
            kg=p22
        if p32<kp:
            kg=p32
        if p42<kp:
            kg=p42
######################################################

        cv.line(r, (p11,p12),(p21,p22), (255, 0, 0), 1)
        cv.line(r, (p31,p32),(p21,p22), (255, 0, 0), 1)
        cv.line(r, (p11,p12),(p41,p42), (255, 0, 0), 1)
        cv.line(r, (p41,p42),(p31,p32), (255, 0, 0), 1)


cv2.imshow('thresh', thresh)
cv2.imshow('r', r)
cv2.imshow('image', image)
cv2.waitKey()
cv2.destroyAllWindows()
