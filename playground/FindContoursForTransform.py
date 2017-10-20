import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import List

# TODO: cv2.Canny is propably what is needed

def find_largest_square(contours: List):
    squares = [square for square in filter(lambda l: len(l) == 4, contours)]
    areas = [area_square(square) for square in squares]
    return max(zip(squares,areas), key=lambda z: z[1])[0]

# TODO: there is something like cv2.contourArea
def area_square(square):
    e = (square[0]-square[1])[0]
    f = (square[2]-square[3])[0]
    return 0.5 * np.sqrt(np.dot(e,e)*np.dot(f,f)-np.dot(e,f)**2)

# TODO: implement largest_square
# then we should be able to get input points
# automatically

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))

video = cv2.VideoCapture('robo_on_paper.mov')

_, frame = video.read()

gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
close_operated_frame = cv2.morphologyEx(gray_frame, cv2.MORPH_CLOSE, kernel)
_, thresholded = cv2.threshold(gray_frame, 200, 255, cv2.THRESH_BINARY)

_, contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest = find_largest_square(contours)
cv2.drawContours(thresholded, contours, -1, (255, 0, 255), 10)

plt.subplot(221); plt.imshow(frame)
plt.subplot(222); plt.imshow(gray_frame)
plt.subplot(223); plt.imshow(close_operated_frame)
plt.subplot(224); plt.imshow(thresholded)

plt.show()