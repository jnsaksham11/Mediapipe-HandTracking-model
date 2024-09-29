import cv2 as cv
import time
import mediapipe as mp
import handtrackingmodule as htm

cap = cv.VideoCapture(0)
detector = htm.hand_detector(detectioncon=0.75)

prev_time = 0
curr_time =0

tipids = [4, 8, 12, 16, 20]
fingers=[]
lmlist1=[]

while True:
    success, img = cap.read()
    img = cv.flip(img,1)
    img = detector.findhands(img)
    
    lmlist = detector.findposition(img,draw=False,handno=0)
    
    if detector.results.multi_hand_landmarks:
        if(len(detector.results.multi_hand_landmarks) == 2):
            lmlist1 = detector.findposition(img,draw=False,handno=1)

    if len(lmlist) != 0 or len(lmlist1) != 0:
        fingers = []

        if len(lmlist) !=0:
            #for right and left thumb
            if(lmlist[tipids[0]][1] < lmlist[tipids[0]-1][1] and lmlist[5][1]< lmlist[18][1]):
                fingers.append(1)
            elif(lmlist[tipids[0]][1] > lmlist[tipids[0]-1][1]  and lmlist[5][1]> lmlist[18][1]):
                fingers.append(1)
            else:
                fingers.append(0)

            #for four fingers
            for id in range(1,5):
                if(lmlist[tipids[id]][2] < lmlist[tipids[id]-2][2]):
                    fingers.append(1)
                else:
                    fingers.append(0)
        
        if (detector.results.multi_hand_landmarks != None):
            if(len(detector.results.multi_hand_landmarks) == 2):
                #for right and left thumb
                if(lmlist1[tipids[0]][1] < lmlist1[tipids[0]-1][1] and lmlist1[5][1]< lmlist1[18][1]):
                    fingers.append(1)
                elif(lmlist1[tipids[0]][1] > lmlist1[tipids[0]-1][1]  and lmlist1[5][1]> lmlist1[18][1]):
                    fingers.append(1)
                else:
                    fingers.append(0)

                #for four fingers
                for id in range(1,5):
                    if(lmlist1[tipids[id]][2] < lmlist1[tipids[id]-2][2]):
                        fingers.append(1)
                    else:
                        fingers.append(0)

    else:
         #no hand is seen
         lmlist1=[]
         lmlist=[]
         fingers=[]


    curr_time = time.time()
    fps = 1/(curr_time-prev_time)
    prev_time = curr_time

    
    cv.putText(img,f'FPS: {str(int(fps))}',(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv.putText(img,str(fingers.count(1)),(10,120),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv.imshow("camera",img)
    # cv.waitKey(1)
    if cv.waitKey(1) == ord('d'):
        break