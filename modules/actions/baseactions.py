import time
import numpy as np


from ..data_classes.data_classes import Object_position
from ..computer_vision import BaseFinder
from ..data_classes.templates import *
from ..window_manager import Window_manager


class BaseActions:

    def __init__(self, monitor_manager: Window_manager, screenshot):
        self.monitor_manager = monitor_manager
        self.screenshot = screenshot
        self.finder = BaseFinder()

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



