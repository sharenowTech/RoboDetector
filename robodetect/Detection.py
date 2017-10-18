import cv2
import numpy as np

def calculate_perspective_warp(_4_src_points,
                               _4_dst_points):
    return cv2.getPerspectiveTransform(
        np.float32(_4_src_points),
        np.float32(_4_dst_points)
    )

def warp_image(image, dst_width, dst_height, warp_matrix):
    return cv2.warpPerspective(
        image, warp_matrix, (dst_width, dst_height)
    )

def preprocess_image_for_detection(
        image, dst_width, dst_height,
        warp_matrix, bg_subtractor,
        close_kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
):
    # preprocessing before detection and tracking
    warped_frame = cv2.warpPerspective(
        image, warp_matrix, (dst_width, dst_height)
    )
    gray_frame = cv2.cvtColor(warped_frame, cv2.COLOR_BGR2GRAY)
    inv_gray_frame = cv2.bitwise_not(gray_frame)
    median_blurred_frame = cv2.medianBlur(inv_gray_frame, 11)
    fg_frame = bg_subtractor.apply(median_blurred_frame)
    close_operated_frame = cv2.morphologyEx(
        fg_frame, cv2.MORPH_CLOSE, close_kernel
    )

    return close_operated_frame


def get_convex_hulls_of_moving_objects(preprocessed_image):
    _, contours, _ = cv2.findContours(
        preprocessed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    return [cv2.convexHull(points) for points in contours]


def detect_moving_objects(convex_hulls, area_threshold=100.0):
    return [convex_hull
            for convex_hull in convex_hulls
            if cv2.contourArea(convex_hull) >= area_threshold]


def detect_moving_object_on_raw_image(
        raw_image, dst_width, dst_height, warp_matrix, bg_subtractor,
        close_kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)),
        area_threshold=100.0
):
    # TODO: this should give coordinates to the backtransformed image resp.!!!
    preprocessed_image = preprocess_image_for_detection(
        raw_image, dst_width, dst_height,
        warp_matrix, bg_subtractor, close_kernel
    )

    hulls = get_convex_hulls_of_moving_objects(preprocessed_image)
    return detect_moving_objects(hulls, area_threshold)


def get_image_coordinates_of_objects(objects):
    moments = [cv2.moments(points) for points in objects]

    centroids = [(int(M['m10']/M['m00']), int(M['m01']/M['m00']))
                 for M in moments]
    return centroids
