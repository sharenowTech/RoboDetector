import cv2
import numpy as np
import threading
import matplotlib.pyplot as plt
from typing import List, Optional


stream = cv2.VideoCapture(0)
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=3600,
                                                   varThreshold=400.0)
dst_width= 1000
dst_height = 1414

class GetSrcPoints(threading.Thread):
    # TODO: integrate plt.show
    def __init__(self):
        threading.Thread.__init__(self)
        self._4_src_points = []

    def run(self):
        print('Provide 4 points from source image')
        for i in range(4):
            print('Point {}:'.format(i))
            x = input('x ')
            y = input('y ')
            self._4_src_points.append([x, y])


def calculate_perspective_warp(_4_src_points: Optional[List[List], np.ndarray],
                               _4_dst_points: Optional[List[List], np.ndarray]):
    M = cv2.getPerspectiveTransform(np.float32(_4_src_points),
                                    np.float32(_4_dst_points))
    return M

def main():

    # init
    M = calculate_perspective_warp()
    getSrcPoints = GetSrcPoints()

    ok, frame = stream.read()


    # main loop, reading and processing image from stream
    while True:
        prev_frame = frame
        ok, frame = stream.read()
        if not ok:
            frame = prev_frame

        warped_frame = cv2.warpPerspective(frame, M, (dst_width, dst_height))
        fg_frame = bg_subtractor.apply(warped_frame)






if __name__ == '__main__':
    main()