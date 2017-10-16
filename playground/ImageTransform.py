import cv2
import numpy as np
import matplotlib.pyplot as plt

input_points = []

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        if len(input_points) < 4:
            input_points.append([x, y])
        else:
            print('enough input points provided')



img = cv2.imread('paper_perspective.JPG')
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', mouse_callback)
output_points = np.float32([[0,0], [1000,0], [1000,1414], [0,1414]])
"""
while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(0) & 0xff
    if k == 27:
        break
    cv2.destroyAllWindows()
"""

gray = cv2.g
cv2.findContours()

# input_points = np.float32(input_points)
input_points = np.float32([[1173, 976], [1896, 984], [1998,1545], [958, 1545]])

M = cv2.getPerspectiveTransform(input_points, output_points)

out_img = cv2.warpPerspective(img, M, (1000, 1414))

plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(out_img),plt.title('Output')
plt.show()

"""
while True:
    cv2.imshow('warped_image', out_img)
    k = cv2.waitKey(0) & 0xff
    if k == 27:
        break
    cv2.destroyAllWindows()

"""

