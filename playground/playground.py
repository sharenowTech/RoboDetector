import numpy as np
import cv2

img = cv2.imread('screenshot.png')
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
