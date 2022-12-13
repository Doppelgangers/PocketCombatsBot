import cv2
import time
import numpy as np

from .attack_the_enemy import Attack_the_enemy
from .baseactions import BaseActions
from ..data_classes.data_classes import Object_position
from .mouse_control import Mouse_control
from ..data_classes.templates import *
from ..image_controller.image_controller import Image_controller


class MenuActions(BaseActions):

    def __init__(self, monitor_manager, screenshot):
        super().__init__(monitor_manager=monitor_manager, screenshot=screenshot)
        self.SCROLL_AREA = Object_position(x1=202, y1=318, x2=379, y2=642)
        self.SCROLL_AREA.convert_position_to_global(monitor_manager)

    def scroll_map(self, scroll_to):
        Mouse_control.scrolling_mouse_for_area(area=self.SCROLL_AREA, scroll_to=scroll_to, speed=0.18)

    def find_fight(self, enemy: Template_Enemy, wait: int) -> bool:
        start_time = time.perf_counter()
        cooldown = False
        while time.perf_counter() - start_time < wait or cooldown:

            img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            attker = Attack_the_enemy(monitor_manager=self.monitor_manager, screenshot=self.screenshot)
            atk = attker.attack_the_enemy(enemy=enemy, img_gray=img_gray)

            if atk == "cooldown":
                cooldown = True
            elif atk:
                return True
            else:
                cooldown = False
                self.scroll_map("down")
                if self.checking_end_of_scroll():
                    break
        return False

    def checking_end_of_scroll(self) -> bool:
        """
        Проверяет появляется волна окончания прокрутки
        :return: True если конец страницы
        """
        img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))

        min_hsv = np.array((1, 0, 160))
        max_hsv = np.array((179, 30, 255))

        number_true_colors = Image_controller.check_number_of_colors(img, min_hsv, max_hsv)
        if number_true_colors > 10_000:
            return True
        return False

