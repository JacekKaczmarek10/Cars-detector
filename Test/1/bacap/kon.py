import cv2
import cv2 as cv
import numpy as np
from numpy import*

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
#wgrywanie obrazu
pusty = cv2.imread('1.jpg')
cv2.namedWindow('pusty')
cv2.setMouseCallback('pusty',draw_P)
#pętla do zczytywania punktów wieszchołkowych danego miejca parkingowego
f=1
while(f):
    cv2.imshow('pusty',pusty)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print('liczy...')
#funkcjia obliczająca i rysująca krawędzie
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
#wczytanie obrazów
Pusty_v2 = cv2.imread('1.jpg')
zajety= cv2.imread('2.jpg')
#znalezienie różnic
diff=cv2.absdiff(Pusty_v2,zajety)
image=diff
#przygotowanie obrazu
blur = cv2.pyrMeanShiftFiltering(image, 11, 21)
src_gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
#wyszukanie krawędzi w obrazie rużnic 
threshold = 60
kra=thresh_callback(threshold)
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
#pętla sppawdzajaca czy dane mijece jest zjęte
g=0
for i in range(len(miejsca)):
    if miejsca[g]==1:
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
                spr2=W_Sp(a2,b2,a3,b3,k1,k2)
                if spr2==Oriet2:
                    spr3=W_Sp(a3,b3,a4,b4,k1,k2)
                    if spr3==Oriet3:
                        spr4=W_Sp(a4,b4,a1,b1,k1,k2)
                        if spr4==Oriet4:
                            miejsca[g-1]=2
                            s=len(kra)                                      
            s+=1
#pętla rysjujaca miejce
wyj=zajety
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
    if miejsca[g]==1:
        color=color=(0, 255, 0)
        
    if miejsca[g]==2:
        color=color=(0, 0, 255)
        lczbamw+=1
    g+=1
#rysowanie miejsc
    cv.line(wyj, (p11,p12),(p21,p22), color, 1)
    cv.line(wyj, (p31,p32),(p21,p22), color, 1)
    cv.line(wyj, (p11,p12),(p41,p42), color, 1)
    cv.line(wyj, (p41,p42),(p31,p32), color, 1)
#podawanie ilości wolnych miejc 
lczbamw=lczbamc-lczbamw
print(lczbamc)
print(lczbamw)
#wyświetlanie obrazu z zaznaczonymi miejscami (zajęte, nie zajęte)
cv2.imshow('wyj', wyj)
cv2.imshow('image', image)
cv2.waitKey()
cv2.destroyAllWindows()

