import cv2 as cv
import mediapipe as mp
import time

class hand_detector():
    def __init__(self, mode = False,maxhands =2, detectioncon= 0.5,trackcon = 0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.detectioncon = detectioncon
        self.trackcon = trackcon

        
        self.mphands = mp.solutions.hands
        # self.hands = self.mphands.Hands(self.mode,self.maxhands,self.detectioncon,self.trackcon)
        self.hands = self.mphands.Hands()
        self.mpdraw = mp.solutions.drawing_utils

        self.tipids = [4, 8, 12, 16, 20]

    def findhands(self,img,draw = True):
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)


        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img,handlms,self.mphands.HAND_CONNECTIONS)
        
        return img
    
    def findposition(self, img, handno=0,draw= True):
        self.lmlist = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):
                # print(id,lm)
                h, w, c= img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(results.multi_hand_landmarks)
                # print(id,cx,cy)
                self.lmlist.append([id,cx,cy])
                if draw:
                    cv.circle(img,(cx,cy),7,(255,0,2),cv.FILLED)

        return self.lmlist
    
    def fingersup(self):
        fingers = []

        
        #for right and left thumb
        if(self.lmlist[self.tipids[0]][1] < self.lmlist[self.tipids[0]-1][1] and self.lmlist[5][1]< self.lmlist[18][1]):
            fingers.append(1)
        elif(self.lmlist[self.tipids[0]][1] > self.lmlist[self.tipids[0]-1][1]  and self.lmlist[5][1]> self.lmlist[18][1]):
            fingers.append(1)
        else:
            fingers.append(0)

        #for four fingers
        for id in range(1,5):
            if(self.lmlist[self.tipids[id]][2] < self.lmlist[self.tipids[id]-2][2]):
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers

def main():
    cap = cv.VideoCapture(0)
    detector = hand_detector()

    prev_time = 0
    curr_time =0

    while True:
        success, img = cap.read()
        img = cv.flip(img,1)
        img = detector.findhands(img)
        
        lmlist = detector.findposition(img)
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

if __name__ == "__main__":
    main()