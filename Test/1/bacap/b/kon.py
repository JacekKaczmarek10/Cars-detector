import cv2
import cv2 as cv
import numpy as np
from numpy import*


lczbamc=0
lczbamw=0 
coordinates = zeros((20,4,2),float)
miejsca = zeros((20,2),int)
x1=0
y1=0
z1=0

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
            lczbamc=lczbamc+1
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

pusty = cv2.imread('1.jpg')
cv2.namedWindow('pusty')
cv2.setMouseCallback('pusty',draw_P)
f=1
while(f):
    cv2.imshow('pusty',pusty)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        f=0

print('liczy...')

def thresh_callback(val):
    threshold = val
    # Detect edges using Canny
    canny_output = cv.Canny(src_gray, threshold, threshold * 2)
    # Find contours
    contours, hierarchy = cv.findContours(canny_output, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    # Draw contours
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    
    
    for i in range(len(contours)):
        color = (255)
        cv.drawContours(drawing, contours, i, color, 2, cv.LINE_8, hierarchy, 0)
    # Show in a window
    print('XD')
    print(len(contours[0][0][0]))
    print(len(contours[0][0]))
    print(len(contours[23]))
    print(len(contours))
    print('XD')
    print(contours[100][22][0][1])
    #print(hierarchy)
    cv.imshow('Contours', drawing)
    return drawing

#g1=cv2.imread(cv.samples.findFile("1.jpg"))
Pusty_v2 = cv2.imread('1.jpg')
zajety= cv2.imread('2.jpg')
#g3 = cv2.imread('3.jpg')
#g2=cv2.imread(cv.samples.findFile("2.jpg"))
#diff1=cv2.absdiff(g1,g2)
diff=cv2.absdiff(Pusty_v2,zajety)
image=diff
#image = cv2.imread('test1.png')
#image = cv2.imread('2.jpg')
#image = cv2.imread('1.jpg')
blur = cv2.pyrMeanShiftFiltering(image, 11, 21)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

threshold = 200
src_gray=gray
#thresh1=thresh_callback(thresh)
#print(thresh)
#src_gray=thresh
thresh_callback(threshold)
#cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#for c in cnts:
#    peri = cv2.arcLength(c, True)
#    approx = cv2.approxPolyDP(c, 0.015 * peri, True)
#    if len(approx) == 4:
#        x,y,w,h = cv2.boundingRect(approx)
#        cv2.rectangle(image,(x,y),(x+w,y+h),(36,255,12),2)
#print(thresh[244])
#print(coordinates)
#cv2.imshow('thresh', thresh)
#r = cv2.imread('2.jpg')
wyj=zajety
x1=0
y1=0
z=0
for i in range(1,80):
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
        #print(p12)
        #print(p21)
        #print(p22)
        #print(coordinates)
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
            kd=p32
        if p42>kd:
            kd=p42
######################################################
        if p12<=p22:
            kg=p12
        else:
            kg=p22
        if p32<kg:
            kg=p32
        if p42<kg:
            kg=p42
######################################################
        color=(0, 255, 0)
        a=0
        #print(kd)
        #print(kg)
        #print(kl)
        #print(kp)
        #print(x1)
        b=kg-kd
        c=kp-kl
        d=0
        e=0
        for n in range(1,700):
            #print(kd)
            for m in range(1,700):
                #print(kd)
                #print(kg)
                #print(kl)
                #print(kp)

                #print(d)
                #print(e)
                if d>kg:
                    if d<kd:
                        if e>kl:
                            if e<kp:
                                #print(thresh[e][d])
                                if thresh[d][e]==[0]:
                                    a=1
                            
                d=d+1
                if d== 700:
                    d=0
                    #print(e)
                    e=e+1
        if a==0:
            color=(0, 255, 0)
            
        else:
            
            color=(0, 0, 255)
            lczbamw=lczbamw+1
        #print(a)
######################################################
        cv.line(wyj, (p11,p12),(p21,p22), color, 1)
        cv.line(wyj, (p31,p32),(p21,p22), color, 1)
        cv.line(wyj, (p11,p12),(p41,p42), color, 1)
        cv.line(wyj, (p41,p42),(p31,p32), color, 1)
lczbamw=lczbamc-lczbamw
print(lczbamc)
print(lczbamw)
#cv2.imshow('thresh1', thresh1)
#wyświetlanie obrazu z zaznaczonymi miejscami (zajęte, nie zajęte)
cv2.imshow('wyj', wyj)
cv2.imshow('image', image)
cv2.waitKey()
cv2.destroyAllWindows()

