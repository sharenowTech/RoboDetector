import cv2
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread

class GetInput(Thread):
    def run(self):
        print('Provide input points')
        for i in range(4):
            print('Point {}:'.format(i))
            x = input('x ')
            y = input('y ')
            input_points.append([x, y])




video = cv2.VideoCapture('robo_on_paper.mov')
_, frame = video.read()

output_points = np.float32([[0,0], [1000, 0], [1000, 1410], [0, 1410]])
input_points = []
# input points for robo_on_paper.mov
input_points = [[448,393], [667,389], [731,565], [423,571]]

input_points = np.float32(input_points)

if not len(input_points):
    getInput = GetInput()
    getInput.start()
    plt.imshow(frame)
    plt.title('first frame')
    plt.show()
    getInput.join()

M = cv2.getPerspectiveTransform(input_points, output_points)
warped = cv2.warpPerspective(frame, M, (1000,1410))

tracker = cv2.MultiTracker_create()
bbox1 = cv2.selectROI('tracking', warped)
bbox2 = cv2.selectROI('tracking', warped)

tracker.add(cv2.TrackerMedianFlow_create(), warped, bbox1)
tracker.add(cv2.TrackerMedianFlow_create(), warped, bbox2)

while True:
    ok, frame = video.read()
    if not ok:
        break

    warped = cv2.warpPerspective(frame, M, (1000, 1410))
    _, boxes = tracker.update(warped)

    for box in boxes:
        p1 = int(box[0]), int(box[1])
        p2 = int(box[0] + box[2]), int(box[1] + box[3])
        cv2.rectangle(warped, p1, p2, (0, 0, 200))
    cv2.imshow('tracking', warped)

    k = cv2.waitKey(1) & 0xff
    if k == 27: break

video.release()
cv2.destroyAllWindows()


