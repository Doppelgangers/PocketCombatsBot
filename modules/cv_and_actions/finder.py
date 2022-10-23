import cv2
import numpy as np
from ..data_classes.templates import *
from ..data_classes.data_classes import *


class Finder:

    @staticmethod
    def find_object(template: Template, img_gray, precision: float = 0.6, method=cv2.TM_CCOEFF_NORMED, draw_rect_in_gray_img: bool = False):
        """
        Ищет на скиншоте объект по шаблону
        :param template: Шаблон по которому будем искать
        :param img_gray: чёрно-белый скриншот
        :param precision: точность поиска
        :param method: метод cv2 для поиска по шаблону
        :param draw_rect_in_gray_img: Рисовать квадрат вокруг объекта?
        :return: координаты обекта или ничего
        """

        position_find_object = {}
        width_template, height_template = template.img.shape[::-1]

        result = cv2.matchTemplate(img_gray, template.img, method)
        location_of_matches = np.where(result >= precision)

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
    def find_in_object(template, img_gray, y1, y2, precision: float = 0.6, draw_rect_in_gray_img: bool = False):
        cut_img_gray = img_gray[y1:y2]

        local_position = Finder.find_object(template=template, img_gray=cut_img_gray, precision=precision,
                                            draw_rect_in_gray_img=draw_rect_in_gray_img)
        if local_position:
            local_position.y1 += y1
            local_position.y2 += y1
            return local_position
