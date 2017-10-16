import cv2
import numpy as np
from matplotlib import pyplot as plt

filename = 'robo1.JPG'
img = cv2.imread(filename)
gray = np.float32(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

dst = cv2.cornerHarris(gray, 10, 3, 0.04)

dst = cv2.dilate(dst, None)

img[dst > 0.01*dst.max()] = [0, 0, 255]

"""
cv2.imshow('dst', img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
"""

corners = np.int_(cv2.goodFeaturesToTrack(gray, 25, 0.01, 10))

for i in corners:
    x, y = i.ravel()
    cv2.circle(img, (x,y), 3, 255, -1)

plt.imshow(img)
plt.show()
