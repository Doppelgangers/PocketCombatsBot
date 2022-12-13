import cv2
import numpy as np

from modules.data_classes import Object_position


class Image_actions:

    @staticmethod
    def cut_image_by_coordinates(img, x1=None, x2=None, y1=None, y2=None):
        return img[y1:y2, x1:x2]

    @staticmethod
    def cut_image_by_obj_pos(img, object_position: Object_position = None):
        return img[object_position.y1:object_position.y2, object_position.x1:object_position.x2]

    @staticmethod
    def check_number_of_colors(img_bgr, hsv_min: tuple[int, int, int] | np.ndarray, hsv_max: tuple[int, int, int] | np.ndarray):
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        masc = cv2.inRange(hsv, hsv_min, hsv_max)
        moment = cv2.moments(masc, 1)
        return moment['m00']
