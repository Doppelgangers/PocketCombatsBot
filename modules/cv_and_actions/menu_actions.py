import time

import numpy as np

from .baseactions import BaseActions
from ..data_classes.data_classes import Object_position
from ..data_classes.templates import *
from .basefinder import BaseFinder


class MenuActions(BaseActions):

    def __init__(self, monitor_manager, screenshot):
        super().__init__(monitor_manager=monitor_manager, screenshot=screenshot)
        self.SCROLL_AREA = Object_position(x1=202, y1=318, x2=379, y2=642)
        self.SCROLL_AREA.convert_position_local_to_global(monitor_manager)

    def attack_the_enemy(self, enemy: Template_Enemy, img_gray) -> bool:
        """
        Ищет врага на экране и если находит то атакует
        :param enemy: Шаблон врага
        :param img_gray: скриншот
        :return:
        True атаквал врага
        False не атаквал врага
        """
        if position_btn_attack := self.__find_the_enemy_and_get_position_btn_attack(img_gray=img_gray, enemy=enemy):
            self.click_random_point_in_the_area(position_btn_attack, relative=True)
            return True
        return False

    @staticmethod
    def __find_the_enemy_and_get_position_btn_attack(img_gray, enemy: Template_Enemy):
        """
        :param img_gray: Чёрно-белый скриншот
        :param enemy: Шаблон врага
        :return: Позицию кнопки атаки or None
        """
        enemy_position = BaseFinder.find_object(template=enemy, img_gray=img_gray, draw_rect_in_gray_img=True)

        if enemy_position:
            attack_position = BaseFinder.find_in_object(template=UI.attack_the_enemy, img_gray=img_gray,
                                                        y1=enemy_position.y1, y2=enemy_position.y2, draw_rect_in_gray_img=True)
            if attack_position:
                return attack_position
        return None

    def scroll_map(self, scroll_to):
        self.scrolling_mouse_for_area(area=self.SCROLL_AREA, scroll_to=scroll_to, speed=0.18)

    def find_fight(self, enemy: Template_Enemy, wait: int)-> bool:

        start_time = time.perf_counter()
        while time.perf_counter() - start_time < wait:
            img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            if self.attack_the_enemy(enemy=enemy, img_gray=img_gray):
                return True

            self.scroll_map("down")
        return False
