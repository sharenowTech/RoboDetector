import cv2
import numpy as np

stream = cv2.VideoCapture(0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=400.0)

while True:
    ok, frame = stream.read()

    fgmask = bg_subtractor.apply(frame)
    close_operated_image = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    _, thresholded = cv2.threshold(close_operated_image, 75, 255, cv2.THRESH_BINARY)

    median_blurred = cv2.medianBlur(thresholded, 5)

    cv2.imshow('subracted', fgmask)

    if cv2.waitKey(30) & 0xff == 27:
        break

stream.release()
cv2.destroyAllWindows()