import cv2
import numpy as np
import matplotlib.pyplot as plt

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
cv2.drawContours(thresholded, contours, -1, (100, 0, 255), 2)

plt.subplot(321); plt.imshow(frame)
plt.subplot(322); plt.imshow(gray_frame)
plt.subplot(323); plt.imshow(close_operated_frame)
plt.subplot(324); plt.imshow(thresholded)
plt.subplot(325);
plt.subplot(326);
plt.show()