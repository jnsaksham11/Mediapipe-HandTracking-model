import cv2 as cv
import time
import mediapipe as mp
import handtrackingmodule as htm
import math
import numpy as np




cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1100)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, 2200)
detector = htm.hand_detector(detectioncon=0.85)

prev_time = 0
curr_time =0

selected_color=(0,0,255)
bc1,bc2,bc3,bc4,bc5=(255,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)
xp,yp=(0,0)
img_canvas= np.zeros((720,1280,3),np.uint8)

while True:
    success, img = cap.read()
    img = cv.flip(img,1)

    #fine hand landmarks
    img = detector.findhands(img)
    
    lmlist = detector.findposition(img)
    if len(lmlist) != 0:
        # print(lmlist)

        #tip of index and midle fingers
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]


        # check which fingers are up
        fingers = detector.fingersup()
        # print(fingers)

        #if selectin mode --> two finger are up
        if fingers[1] and fingers[2]:
            xp,yp=(0,0)

            if y1<180 and y2<180:
                if 170<x1<270 and 170<x2<270:
                    selected_color=(0,0,255)
                    bc1,bc2,bc3,bc4,bc5 = (255,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)
                elif 420<x1<520 and 420<x2<520:
                    selected_color=(255,0,255)
                    bc1,bc2,bc3,bc4,bc5=(0,0,0),(255,0,0),(0,0,0),(0,0,0),(0,0,0)
                elif 670<x1<770 and 670<x2<770:
                    selected_color=(255,255,0)
                    bc1,bc2,bc3,bc4,bc5=(0,0,0),(0,0,0),(255,0,0),(0,0,0),(0,0,0)
                elif 920<x1<1020 and 920<x2<1020:
                    selected_color=(0,255,0)
                    bc1,bc2,bc3,bc4,bc5=(0,0,0),(0,0,0),(0,0,0),(255,0,0),(0,0,0)
                elif 1120<x1<1220 and 1120<x2<1220:
                    selected_color=(0,0,0)
                    bc1,bc2,bc3,bc4,bc5=(0,0,0),(0,0,0),(0,0,0),(0,0,0),(255,0,0)

            cv.rectangle(img,(x1,y1-25),(x2,y2+25),selected_color, cv.FILLED)

        #if drawing mode - index finger is up
        if fingers[1] and fingers[2]==False:
            
            if xp==0 and yp==0:
                xp=x1
                yp=y1
            
            #for erasser
            if selected_color==(0,0,0):
                cv.line(img,(xp,yp),(x1,y1),selected_color,30)
                cv.line(img_canvas,(xp,yp),(x1,y1),selected_color,30)
            else:
                cv.line(img,(xp,yp),(x1,y1),selected_color,10)
                cv.line(img_canvas,(xp,yp),(x1,y1),selected_color,10)

            cv.circle(img,(x1,y1),15,selected_color,cv.FILLED)

            xp,yp = x1,y1
            

    #transform img to gray because threshold take only gray image
    img_gray = cv.cvtColor(img_canvas,cv.COLOR_BGR2GRAY)
    
    #convert gray img to black and white becomes mask in which background is white and all written is black
    _, img_inv = (cv.threshold(img_gray,50,255,cv.THRESH_BINARY_INV))
    
    #convert gray to bgr because bitwise_and takes only bgr image
    img_inv = cv.cvtColor(img_inv,cv.COLOR_GRAY2BGR)
    
    #shows img with black written line on it
    img = cv.bitwise_and(img,img_inv)
    
    #shows img with colorful written line on it
    img = cv.bitwise_or(img,img_canvas)
    



    curr_time = time.time()
    fps = 1/(curr_time-prev_time)
    prev_time = curr_time

    #color rectangle on header
    cv.rectangle(img,(0,0),(1280,180),(0,0,0),cv.FILLED)
    cv.rectangle(img,(170,30),(270,130),(0,0,255),cv.FILLED)
    cv.rectangle(img,(420,30),(520,130),(255,0,255),cv.FILLED)
    cv.rectangle(img,(670,30),(770,130),(255,255,0),cv.FILLED)
    cv.rectangle(img,(920,30),(1020,130),(0,255,0),cv.FILLED)
    cv.rectangle(img,(1120,30),(1220,130),(255,255,255),cv.FILLED)

    #border on selection
    cv.rectangle(img,(170,30),(270,130),bc1,3)
    cv.rectangle(img,(420,30),(520,130),bc2,3)
    cv.rectangle(img,(670,30),(770,130),bc3,3)
    cv.rectangle(img,(920,30),(1020,130),bc4,3)
    cv.rectangle(img,(1120,30),(1220,130),bc5,3)

    cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv.imshow("camera",img)
    # cv.imshow("canvs",img_canvas)
    # cv.imshow("inverse",img_inv)
    if cv.waitKey(1) == ord('d'):
        break

cap.release()
cv.destroyAllWindows()