import time
from mss import mss
from modules.computer_vision.base_finder import Finder
from modules.data_classes import Template
from modules.mouse.mouse import Mouse
from modules.window import Window
import logging


class Actions:

    def __init__(self, monitor_manager: Window, screenshot: mss):
        self.monitor_manager = monitor_manager
        self.screenshot = screenshot
        self.finder = Finder(monitor_manager=monitor_manager, screenshot=screenshot)
        self.__logger = logging.getLogger(__name__)

    def find_by_template_and_click_area(self, template: Template, wait: float = 0.5, offset: int = 2, press_delay: float = 0) -> bool:
        """
        Ищет объект по шаблону и нажимает в случайную точку в его области
        :param press_delay:
        :param offset:
        :param template: шаблон
        :param wait: время поиска объекта
        :return: True or False , нажал на объект или нет.
        """

        if pos := self.finder.try_find_element(template=template, wait=wait):
            time.sleep(press_delay)
            Mouse.click_random_point_in_the_area(pos, monitor_manager=self.monitor_manager, offset=offset)
            self.__logger.debug(f"Делаю клик по найденному области найденного объекта \n Координаты {pos}")
            return True
        self.__logger.debug(f"Объект не найден (find_by_template_and_click_area)")
        return False
