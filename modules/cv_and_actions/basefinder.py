import time

import cv2
import numpy as np
from ..data_classes.templates import *
from ..data_classes.data_classes import Object_position


class BaseFinder:

    @staticmethod
    def find_object(template: Template, img_gray, method=cv2.TM_CCOEFF_NORMED, draw_rect_in_gray_img: bool = False):
        """
        Ищет на скиншоте объект по шаблону
        :param template: Шаблон по которому будем искать
        :param img_gray: чёрно-белый скриншот
        :param method: метод cv2 для поиска по шаблону
        :param draw_rect_in_gray_img: Рисовать квадрат вокруг объекта?
        :return: координаты обекта или ничего
        """

        position_find_object = {}
        width_template, height_template = template.img.shape[::-1]

        result = cv2.matchTemplate(img_gray, template.img, method)
        location_of_matches = np.where(result >= template.precision)

        for pt in zip(*location_of_matches[::-1]):

            if draw_rect_in_gray_img:
                cv2.rectangle(img_gray, pt, (pt[0] + width_template, pt[1] + height_template), (0, 0, 255), 1)

            # Координаты найденного обекта, относительно обасти видимости opencv (monitor)
            position_find_object = Object_position(
                x1=pt[0],
                y1=pt[1],
                x2=pt[0] + width_template,
                y2=pt[1] + height_template
            )
            break

        return position_find_object

    @staticmethod
    def cut_image(img_gray, x1=None, x2=None, y1=None, y2=None, object_position: Object_position = None):
        if x1 or x2 or y1 or y1:
            return img_gray[y1:y2, x1:x2]
        if object_position:
            return img_gray[object_position.y1:object_position.y2, object_position.x1:object_position.x2]

    @staticmethod
    def find_in_object(template, img_gray, x1=None, x2=None, y1=None, y2=None, draw_rect_in_gray_img: bool = False):

        cut_img_gray = BaseFinder.cut_image(img_gray=img_gray, x1=x1, x2=x2, y1=y1, y2=y2)

        local_position = BaseFinder.find_object(template=template, img_gray=cut_img_gray,
                                                draw_rect_in_gray_img=draw_rect_in_gray_img)

        #TODO: Кажется тут могут быть ошибки с вычислениями если обрезать не только по координуте y,
        # в плене координаты будут считаться не правильно
        if local_position:
            if y1:
                local_position.y1 += y1
            if y2:
                local_position.y2 += y1
            if x1:
                local_position.x1 += x1
            if x2:
                local_position.x2 += x1
            return local_position

    @staticmethod
    def find_and_cut_object(template: Template, img_gray, method=cv2.TM_CCOEFF_NORMED, draw_rect_in_gray_img: bool = False):
        if position := BaseFinder.find_object(template=template, img_gray=img_gray, method=method):
            return BaseFinder.cut_image(img_gray=img_gray, x1=position.x1, x2=position.x2, y1=position.y1, y2=position.y2)
