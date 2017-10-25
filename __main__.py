import threading
import cv2
import matplotlib.pyplot as plt
import numpy as np

from robodetect.Constants import ESC, RED_BGR
from robodetect.Constants import DST_WIDTH, DST_HEIGHT, AREA_THRESH
from robodetect.Detection import calculate_perspective_warp
from robodetect.Detection import detect_moving_object_on_raw_image
from robodetect.Detection import get_image_coordinates_of_objects
from robodetect.Detection import warp_image

# globals
# reads from camera stream
stream = cv2.VideoCapture(0)
bg_subtractor = cv2.createBackgroundSubtractorMOG2(
    history=500, varThreshold=400.0
)
close_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
M = np.ones((3,3))
four_src_points = []


class InputPoints(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global four_src_points
        four_src_points = []

    def run(self):
        print('Provide 4 points from the source image. '
              'Those are used to calculate the perspective warp matrix')

        for point in range(4):
            print('Point {}:'.format(point))
            x = input('x ')
            y = input('y ')
            four_src_points.append([x, y])

def input_points_and_show_image(image: np.ndarray):
    # we need to create a child thread, because plt.show() blocks program
    # execution until the window is closed, but we want to be able to specify
    # points from the image while having the window opened.
    input_points = InputPoints()
    input_points.start()
    plt.imshow(image)
    plt.show()
    input_points.join()

def main():
    ok, frame = stream.read()

    # init
    input_points_and_show_image(frame)
    warp_matrix = calculate_perspective_warp(
        four_src_points,
        [[0,0], [DST_WIDTH, 0], [DST_WIDTH, DST_HEIGHT], [0, DST_HEIGHT]]
    )

    # main loop, reading and processing image from stream
    while stream.isOpened():
        prev_frame = frame
        ok, frame = stream.read()
        if not ok:
            frame = prev_frame

        warped_frame = warp_image(frame, DST_WIDTH, DST_HEIGHT, warp_matrix)

        objects = detect_moving_object_on_raw_image(
            frame, DST_WIDTH, DST_HEIGHT,
            warp_matrix, bg_subtractor, close_kernel,
            area_threshold=AREA_THRESH
        )

        object_coordinates = get_image_coordinates_of_objects(objects)

        for position in object_coordinates:
            cv2.drawMarker(warped_frame, position, RED_BGR)

        # uncomment to show the detected object contours
        # cv2.drawContours(warped_frame, objects, -1, RED_BGR, 2)
        # show result
        cv2.imshow('processed', warped_frame)

        # break loop when ESC is pressed
        if cv2.waitKey(30) & 0xff == ESC:
            break


if __name__ == '__main__':
    main()
    stream.release()
    cv2.destroyAllWindows()