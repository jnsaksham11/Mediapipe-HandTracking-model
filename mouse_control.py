import cv2 as cv
import time
import mediapipe as mp
import handtrackingmodule1 as htm
import math
import numpy as np
import mouse

cap = cv.VideoCapture(0)
detector = htm.hand_detector(maxhands=1)

prev_time = 0
curr_time =0

wscr = 1270
hscr = 710

smooth = 8
plocx,plocy=0,0
clocx,clocy=0,0


while True:
    success, img = cap.read()
    img = cv.flip(img,1)
    img = detector.findhands(img)
    
    
    lmlist = detector.findposition(img)

    #get tip of middle fingure and index fingure
    if len(lmlist) != 0:
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]
        
        #check which fingers are up
        fingers = detector.fingersup()
        cv.rectangle(img,(100,100),(535,380),(255,0,255),2)

        #only index fingure moving mode
        if fingers[1]==1 and fingers[2]==0:
        
            #convert coordinates
            x3 = np.interp(x1,(100,535),(0,wscr))
            y3 = np.interp(y1,(100,380),(0,hscr))

            #smoothing
            clocx = plocx + (x3-plocx)/ smooth
            clocy = plocy + (y3-plocy)/ smooth

            #move mouse
            mouse.move(clocx,clocy)
            cv.circle(img,(x1,y1),10,(255,0,255),cv.FILLED)
            plocx,plocy=clocx,clocy
        
        #both indes and middle fingers are up:click
        if fingers[1]==1 and fingers[2] ==1:
            cv.line(img,(x1,y1),(x2,y2),(0,0,255),3)
            cv.circle(img,((x1+x2)//2,(y1+y2)//2),10,(0,0,255),cv.FILLED)
            length = math.sqrt((x2-x1)**2 + (y2-y1)**2)
          
            if length<30:
                cv.circle(img,((x1+x2)//2,(y1+y2)//2),10,(0,255,0),cv.FILLED)
                mouse.click()


    curr_time = time.time()
    fps = 1/(curr_time-prev_time)
    prev_time = curr_time
    
    cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv.imshow("camera",img)
    if cv.waitKey(1) == ord('d'):
        break