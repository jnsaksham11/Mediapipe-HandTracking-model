import cv2 as cv
import mediapipe as mp
import time
import math
import handtrackingmodule1 as htm

cap = cv.VideoCapture(0)
detector = htm.hand_detector()

prev_time = 0
curr_time =0
index2 = 8
index1 = 8

while True:
    success, img = cap.read()
    img = cv.flip(img,1)
    img = detector.findhands(img)
    
    lmlist1 = detector.findposition(img,handno=0)
    if detector.results.multi_hand_landmarks:
        if len(detector.results.multi_hand_landmarks) == 2:
            lmlist2 = detector.findposition(img,handno=1)
            x1,y1 = lmlist1[index1][1],lmlist1[index1][2]
            x2,y2 = lmlist2[index2][1],lmlist2[index2][2]
            if math.sqrt((lmlist2[4][1]-lmlist2[8][1])**2 + (lmlist2[4][2]-lmlist2[8][2])**2) <20:
                if index2 ==8:
                    index2=4
                else:
                    index2=8
            if math.sqrt((lmlist1[4][1]-lmlist1[8][1])**2 + (lmlist1[4][2]-lmlist1[8][2])**2) <20:
                if index1 ==8:
                    index1=4
                else:
                    index1=8
                
            cv.line(img,(x1,y1),(x2,y2),(255,255,0),3)
            cv.circle(img,(x1,y1),10,(255,255,0),-1)
            cv.circle(img,(x2,y2),10,(255,255,0),-1)
            cv.circle(img,((x1+x2)//2,(y1+y2)//2),10,(255,255,0),-1)

    curr_time = time.time()
    fps = 1/(curr_time-prev_time)
    prev_time = curr_time
    
    cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv.imshow("camera",img)
    
    if cv.waitKey(1) == ord('d'):
        break
