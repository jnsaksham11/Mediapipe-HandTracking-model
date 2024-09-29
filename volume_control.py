import cv2 as cv
import time
import mediapipe as mp
import handtrackingmodule as htm
import math
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# Get the default audio endpoint
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

# Create a volume object
volume = cast(interface, POINTER(IAudioEndpointVolume))
volrange = volume.GetVolumeRange()
minvol = volrange[0]
maxvol = volrange[1]
volbar=400
volper=0
vol = 0


cap = cv.VideoCapture(0)
detector = htm.hand_detector(detectioncon=0.75)

prev_time = 0
curr_time =0

while True:
    success, img = cap.read()
    img = cv.flip(img,1)
    img = detector.findhands(img)
    
    lmlist = detector.findposition(img,draw=False)
    if len(lmlist) != 0:
        # print(lmlist[4],lmlist[8])

        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]
        cx,cy = (x1+x2)//2 , (y1+y2)//2

        cv.circle(img,(x1,y1),10,(255,0,255),cv.FILLED)
        cv.circle(img,(x2,y2),10,(255,0,255),cv.FILLED)
        cv.circle(img,(cx,cy),10,(255,0,255),cv.FILLED)
        cv.line(img,(x1,y1),(x2,y2),(255,0,255),3)

        length = math.hypot(x2-x1,y2-y1)

        vol = np.interp(length,[50,200],[minvol,maxvol])
        volbar = np.interp(length,[50,200],[400,150])
        volper = np.interp(length,[50,200],[0,100])
        volume.SetMasterVolumeLevel(vol,None)

        if length<50:
            cv.circle(img,(cx,cy),10,(0,255,0),cv.FILLED)

    curr_time = time.time()
    fps = 1/(curr_time-prev_time)
    prev_time = curr_time
    
    cv.putText(img,f'FPS: {str(int(fps))}',(40,50),cv.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv.rectangle(img,(50,150),(85,400),(255,0,0),3)
    cv.rectangle(img,(50,int(volbar)),(85,400),(255,0,0),cv.FILLED)
    cv.putText(img,f'{int(volper)}%',(40,450),cv.FONT_HERSHEY_COMPLEX,1,(250,0,0),3)

    cv.imshow("camera",img)
    # cv.waitKey(1)
    if cv.waitKey(1) == ord('d'):
        break