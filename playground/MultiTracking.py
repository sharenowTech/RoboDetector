import numpy as np
import cv2
import sys

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
fgbg = cv2.createBackgroundSubtractorMOG2()
cv2.namedWindow('tracking')
video = cv2.VideoCapture('2_balls.mov')

tracker = cv2.MultiTracker_create()

ok, image = video.read()

def draw_contours_of_moving_objects(_image):
    image = _image.copy()
    fgmask = fgbg.apply(image)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    _, fgmask = cv2.threshold(fgmask, 0, 255,
                              cv2.THRESH_BINARY) # + cv2.THRESH_OTSU)

    fgmask = cv2.medianBlur(fgmask, 5)
    _, contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE,
                                      cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (100, 0, 255), 2)

    return image


if not ok:
    print('Failed to read video!')
    exit(-1)

bbox1 = cv2.selectROI('tracking', image)
bbox2 = cv2.selectROI('tracking', image)

tracker.add(cv2.TrackerMedianFlow_create(), image, bbox1)
tracker.add(cv2.TrackerMedianFlow_create(), image, bbox2)



while video.isOpened():
    ok, image = video.read()
    if not ok:
        print('no frame to read')
        break

    # optimized_image = draw_contours_of_moving_objects(image)
    optimized_image = image
    ok, boxes = tracker.update(optimized_image)

    for box in boxes:
        p1 = int(box[0]), int(box[1])
        p2 = int(box[0] + box[2]), int(box[1] + box[3])
        cv2.rectangle(image, p1, p2, (0, 0, 200))

    cv2.imshow('tracking', image)
    k = cv2.waitKey(30)
    if k == 27: break # esc pressed
