import cv2
import matplotlib.pyplot as plt
import numpy as np

def preprocess_image(image):
    bilateral_filter_image = cv2.bilateralFilter(image, 7, 150, 150)
    gray_image = cv2.cvtColor(bilateral_filter_image, cv2.COLOR_BGR2GRAY)
    return gray_image

image = preprocess_image(cv2.imread('abs_diff1.jpg'))
bg = preprocess_image(cv2.imread('abs_diff2.jpg'))

subtracted = cv2.absdiff(image, bg)
plt.imshow(subtracted)
plt.show()

kernel = np.ones((5,5), np.uint8)
close_operated_image = cv2.morphologyEx(subtracted, cv2.MORPH_CLOSE, kernel)
plt.imshow(close_operated_image)
plt.show()

_, thresholded = cv2.threshold(close_operated_image, 50, 255, cv2.THRESH_BINARY)
plt.imshow(thresholded)
plt.show()


median = cv2.medianBlur(thresholded, 5)
plt.imshow(median)
plt.show()


