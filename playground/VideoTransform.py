import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt

video = cv2.VideoCapture('2_balls.mov')

_, frame = video.read()

output_points = np.float32([[0,0], [1000, 0], [1000, 1000], [0, 1000]])

input_points = []
print('Provide input points')

plt.imshow(frame)
plt.title('first frame')
plt.show()

for _ in range(4):
    x = input('x')
    y = input('y')
    input_points.append([x,y])

input_points = np.float32(input_points)

M = cv2.getPerspectiveTransform(input_points, output_points)

while True:
    ok, frame = video.read()
    if not ok:
        break

    warped = cv2.warpPerspective(frame, M, (1000,1000))

    cv2.imshow('warped', warped)

    k = cv2.waitKey(1) & 0xff
    if k == 27: break


