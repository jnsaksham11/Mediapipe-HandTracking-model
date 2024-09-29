import cv2
from PIL import Image

from util import get_limits


yellow = [0, 255, 255]  # yellow in BGR colorspace
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=yellow) #get corresponding color range in hsv space

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit) #pixels within the specified HSV range are white (255) and pixels outside the range are black (0)
    cv2.imshow("mask",mask)

    #bounding box detection
    mask_ = Image.fromarray(mask) #for using pil library, It creates a PIL Image object from a NumPy array
    # cv2.imshow("pli",mask_)

    bbox = mask_.getbbox() #bbox contains the bounding box coordinates of the non-zero regions in the mask image. If there are no non-zero regions (i.e., the entire image is zero), bbox will be None.
    # print(bbox)

    if bbox is not None: #make rectangle outside the detected object
        x1, y1, x2, y2 = bbox

        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()