import time

import cv2
import numpy as np
from modules.window import Window
from modules.data_classes import Object_position, Template
from modules.image.image_actions import Image_actions


class Base_finder:

    @staticmethod
    def find_object(img_gray: np.ndarray, template: Template, method=cv2.TM_CCOEFF_NORMED,
                    draw_rect_in_gray_img: bool = False) -> Object_position | None:
        """
        Ищет на скиншоте объект по шаблону
        :param template: Шаблон по которому будем искать
        :param img_gray: чёрно-белый скриншот
        :param method: метод cv2 для поиска по шаблону
        :param draw_rect_in_gray_img: Рисовать квадрат вокруг объекта?
        :return: координаты обекта или ничего
        """

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
            return position_find_object
        else:
            return None

    @classmethod
    def find_in_object(cls, img_gray: np.ndarray, template: Template, x1=None, x2=None, y1=None, y2=None,
                       draw_rect_in_gray_img: bool = False) -> Object_position:
        """
        Ищет обект в указанных дипаозонах.
        :param template: Изображение шаблон.
        :param img_gray: Изображение в котором будем искать шаблон.
        :param x1:
        :param x2:
        :param y1:
        :param y2:
        :param draw_rect_in_gray_img: Рисовать квадрат вокруг этого объекта.
        :return: Координаты найденного объекта
        """
        # Обрезаем огбласть видемости
        cut_img_gray = Image_actions.cut_image_by_coordinates(img=img_gray, x1=x1, x2=x2, y1=y1, y2=y2)
        # Ищем в этой области изображение
        local_position = cls.find_object(template=template, img_gray=cut_img_gray,
                                                 draw_rect_in_gray_img=draw_rect_in_gray_img)
        # Добавляем координаты которые забрали обратно
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

    @classmethod
    def find_and_cut_object(cls, template: Template, img_gray, method=cv2.TM_CCOEFF_NORMED) -> np.ndarray:
        """
        Ищит изображение по шаблону и возвращает его.

        :param template: Изображение шаблон
        :param img_gray: Изображение на котором бужем искать шаблон
        :param method: Способ сравнения изображений
        :return: Возвращает найденное изображение
        """
        if position := cls.find_object(template=template, img_gray=img_gray, method=method):
            return Image_actions.cut_image_by_obj_pos(img=img_gray, object_position=position)


class Iteration_finder(Base_finder):

    def __init__(self, monitor_manager: Window, screenshot):
        self.monitor_manager = monitor_manager
        self.screenshot = screenshot

    def try_find_element(self, template, wait: float = 1) -> Object_position | None:
        """
        Попытка найти объект
        :param wait: количество секунд поиска
        :param template: Шаблон искомого объкта
        :return: позиция объекта или None
        """
        start_time = time.perf_counter()

        while time.perf_counter()-start_time < wait:
            img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            if pos := self.find_object(template=template, img_gray=img_gray):
                return pos
        else:
            return None
