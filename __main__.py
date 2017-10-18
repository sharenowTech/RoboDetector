import threading
import cv2
import numpy as np
from robodetect.Constants import ESC, RED_BGR
from robodetect.Detection import calculate_perspective_warp
from robodetect.Detection import detect_moving_object_on_raw_image
from robodetect.Detection import warp_image
from robodetect.Detection import get_image_coordinates_of_objects


# globals
stream = cv2.VideoCapture('playground/robo_on_paper.mov')
bg_subtractor = cv2.createBackgroundSubtractorMOG2(
    history=1000, varThreshold=400.0
)
close_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
dst_width = 1000
dst_height = 1414
M = np.ones((3,3))
_4_src_points = []

class GetSrcPoints(threading.Thread):
    # TODO: integrate plt.show
    def __init__(self):
        threading.Thread.__init__(self)
        global _4_src_points
        _4_src_points = []

    # uncomment to provide input points via CL
    """
    def run(self):
        print('Provide 4 points from source image')
        for i in range(4):
            print('Point {}:'.format(i))
            x = input('x ')
            y = input('y ')
            _4_src_points.append([x, y])
    """
    def run(self):
        global _4_src_points
        _4_src_points = [[448,393], [667,389], [731,565], [423,571]]


def main():
    # init
    getSrcPoints = GetSrcPoints()
    getSrcPoints.start()
    # TODO: code for showing frame
    getSrcPoints.join()

    warp_matrix = calculate_perspective_warp(
        _4_src_points,
        [[0,0],[dst_width,0],[dst_width, dst_height],[0,dst_height]]
    )

    ok, frame = stream.read()
    # main loop, reading and processing image from stream
    while stream.isOpened():
        prev_frame = frame
        ok, frame = stream.read()
        if not ok:
            frame = prev_frame

        warped_frame = warp_image(frame, dst_width, dst_height, warp_matrix)

        objects = detect_moving_object_on_raw_image(
            frame, dst_width, dst_height,
            warp_matrix, bg_subtractor, close_kernel,
            area_threshold=17000.0
        )

        object_coordinates = get_image_coordinates_of_objects(objects)

        for position in object_coordinates:
            cv2.drawMarker(warped_frame, position, RED_BGR)
        # cv2.drawContours(warped_frame, objects, -1, RED_BGR, 2)
        # show result
        cv2.imshow('processed', warped_frame)

        if cv2.waitKey(30) & 0xff == ESC:
            break


if __name__ == '__main__':
    main()
    stream.release()
    cv2.destroyAllWindows()