import time
import random

import numpy as np
import pyautogui as pag

from ..data_classes.data_classes import Object_position
from .basefinder import BaseFinder
from ..data_classes.templates import *


class BaseActions:

    def __init__(self, monitor_manager, screenshot):
        self.monitor_manager = monitor_manager
        self.screenshot = screenshot
        self.finder = BaseFinder()

    def click_to(self, x, y, click: bool = True, relative_your_screen: bool = False):

        if relative_your_screen:
            x += self.monitor_manager.monitor.get("left")
            y += self.monitor_manager.monitor.get("top")

        pag.moveTo(x, y)

        if click:
            pag.mouseDown()
            time.sleep(random.randrange(31, 83) / 1000)
            pag.mouseUp()

    def get_a_position_relative_to_the_screen(self, position: Object_position):
        """
        Приимсает Object_position модифицирует его и возвращает
        координаты относитиельо монитора для дальнейшего использования
        например для клика по элементу
        :param position: Объект класса Object_position
        :return: модифицированный объект с координатами относительно монитора
        """
        left = self.monitor_manager.monitor.get("left")
        top = self.monitor_manager.monitor.get("top")
        position.y1 += top
        position.y2 += top
        position.x1 += left
        position.x2 += left
        return position

    def click_random_point_in_the_area(self, position: Object_position, relative: bool = True, offset: int = 1):
        """
        Нажимает на кнопку атака в случйном месте
        :param relative: Преобразует коордтинаты окна в координаты монитора
        :param offset: отступ в px во внутрь области
        :param position: координаты элемента
        """
        x = random.randint(position.x1+offset, position.x2-offset)
        y = random.randint(position.y1+offset, position.y2-offset)
        self.click_to(x=x, y=y, relative_your_screen=relative)

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

            if pos := self.finder.find_object(template=template, img_gray=img_gray):
                return pos
        else:
            return None

    @staticmethod
    def scrolling_mouse(distance: int, scrolling_area: Object_position, speed: float = 0.2, distance_is_percent: bool = False):
        """

        :param distance: Растояник прокрутки в px
        :param speed: Скорость прокрутки (в секундаж)
        :param scrolling_area: Область прокрутки
        :param distance_is_percent: Растояник прокрутки будет в процентах относительно размеров scrolling_area
        :return: None
        """
        pag.moveTo(scrolling_area.x1, scrolling_area.y2)
        pag.mouseDown()
        speed = random.uniform(speed-0.05, speed+0.05)
        print(speed)
        pag.moveTo(scrolling_area.x1, scrolling_area.y1, speed)
        pag.mouseUp()

