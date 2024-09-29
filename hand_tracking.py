import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0)

prev_time = 0
curr_time =0

mphands = mp.solutions.hands #imports the hands module from MediaPipe's solutions
hands = mphands.Hands() #creates an instance of the Hands class from the hands module. with four default parameter
mpdraw = mp.solutions.drawing_utils #imports the drawing_utils module from MediaPipe's solutions.

while True:
    success, img = cap.read()
    img = cv.flip(img,1)
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(img_rgb) #process is a method processes the input image to detect and track hand landmarks
    #returns an object containing the detection results.

    if results.multi_hand_landmarks: #attribute of the results object contains a list of hand landmarks for each detected hand. If no hands are detected, this attribute will be None.
        
        for handlms in results.multi_hand_landmarks: #handlms represent object landmark which has 3 attributes x,y,z in normalized form

            for id, lm in enumerate(handlms.landmark): #lm shows all attributes of handlms.landmark object and id no. of landmark in one hand
                
                h, w, c= img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                
                mpdraw.draw_landmarks(img,handlms,mphands.HAND_CONNECTIONS) #function of drawing module which drwa connection btw landmarks
                
                #for id check which id represent which landmark
                if id ==13:
                    cv.circle(img,(cx,cy),25,(255,0,255),cv.FILLED)


    curr_time = time.time()
    fps = 1/(curr_time-prev_time)
    prev_time = curr_time

    cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv.imshow("camera",img)
    if cv.waitKey(1) == ord('d'):
        break

