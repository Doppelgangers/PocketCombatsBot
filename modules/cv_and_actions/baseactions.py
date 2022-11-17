import time
import random

import numpy as np
import pyautogui as pag

from ..data_classes.data_classes import Object_position
from .basefinder import BaseFinder
from ..data_classes.templates import *
from .window_manager import Window_manager


class BaseActions:

    def __init__(self, monitor_manager: Window_manager, screenshot):
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
    def scrolling_mouse(x1: int, y1: int, x2: int, y2: int, speed: float = 0.16):
        """

        :param x1: Начальная координата по оси x
        :param y1: Начальная координата по оси y
        :param y2: Конечная координата по оси x
        :param x2: Конечная координата по оси y
        :param speed: Скорость прокрутки (в секундаж) >= 0.2 sec
        :return: None
        """
        pag.moveTo(x1, y1)
        pag.mouseDown()
        speed = random.uniform(speed-0.05, speed+0.05)
        pag.moveTo(x2, y2, speed)
        pag.mouseUp()

    @staticmethod
    def scrolling_mouse_for_area(area: Object_position, scroll_to: str = "down", speed: float = 0.16):
        """

        :param area:
        :param speed:
        :param scroll_to: Направление прокрутки up or down
        :return: None
        """

        start_x = random.randint(area.min_x(), area.max_x()-20) #случайная область по координате X
        start_y = random.randint(area.max_y()-20, area.max_y()) # нижняя область с погрешностью 20px вверх

        end_x = start_x # относительно базовой точки прибавляем процентно пикселей вправо
        end_y = random.randint(area.min_y(), area.min_y() + 20)

        match scroll_to:
            case "up":
                start_x, end_x = end_x, start_x
                start_y, end_y = end_y, start_y
            case "down":
                pass
            case _:
                raise KeyError("Аргумент " + scroll_to + " не предусмотрен.")

        BaseActions.scrolling_mouse(x1=start_x, y1=start_y, x2=end_x, y2=end_y, speed=speed)
