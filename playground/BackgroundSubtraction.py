import numpy as np
import cv2


cap = cv2.VideoCapture('2_balls.mov')

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))

fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    _, fgmask = cv2.threshold(fgmask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    fgmask = cv2.medianBlur(fgmask, 5)
    _, contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE,
                                      cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (100, 0, 255), 2)
    cv2.fill

    cv2.imshow('frame', frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
