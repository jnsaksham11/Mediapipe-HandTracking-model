import cv2 as cv
import time
import mediapipe as mp
import handtrackingmodule as htm

cap = cv.VideoCapture(0)
detector = htm.hand_detector()

prev_time = 0
curr_time =0

while True:
    success, img = cap.read()
    img = cv.flip(img,1)
    img = detector.findhands(img)
    
    lmlist = detector.findposition(img,draw=False)
    if len(lmlist) != 0:
        print(lmlist[4])

    curr_time = time.time()
    fps = 1/(curr_time-prev_time)
    prev_time = curr_time
    
    cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv.imshow("camera",img)
    cv.waitKey(1)
    # if cv.waitKey(1) == ord('d'):
    #     break