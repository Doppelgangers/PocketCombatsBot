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

    def attack_the_enemy(self, enemy: Template_Enemy, img_gray) -> bool | str:
        """
        Ищет врага на экране и если находит то атакует
        :param enemy: Шаблон врага
        :param img_gray: скриншот
        :return:
        True атаквал врага
        False не атаквал врага
        """
        if position_btn_attack := self.find_the_enemy_and_get_position_btn_attack(img_gray=img_gray, enemy=enemy):
            if self.check_attack_button_state(position_btn_attack):
                self.click_random_point_in_the_area(position_btn_attack, relative=True)
                return True
            else:
                return "cooldown"
        else:
            return False

    @staticmethod
    def find_the_enemy_and_get_position_btn_attack(img_gray, enemy: Template_Enemy):
        """
        :param img_gray: Чёрно-белый скриншот
        :param enemy: Шаблон врага
        :return: Позицию кнопки атаки or None
        """
        enemy_position = BaseFinder.find_object(template=enemy, img_gray=img_gray, draw_rect_in_gray_img=True)

        if enemy_position:
            attack_position = BaseFinder.find_in_object(
                                                        template=UI.attack_the_enemy,
                                                        img_gray=img_gray,
                                                        y1=enemy_position.y1,
                                                        y2=enemy_position.y2,
                                                        draw_rect_in_gray_img=True
                                                        )
            if attack_position:
                return attack_position
        return None

    def scroll_map(self, scroll_to):
        self.scrolling_mouse_for_area(area=self.SCROLL_AREA, scroll_to=scroll_to, speed=0.18)

    def find_fight(self, enemy: Template_Enemy, wait: int) -> bool:
        start_time = time.perf_counter()

        while time.perf_counter() - start_time < wait:

            img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            atk = self.attack_the_enemy(enemy=enemy, img_gray=img_gray)

            print(atk)
            if atk == "cooldown":
                wait += 1
                time.sleep(1)
                print(wait)
            elif atk:
                return True
            else:
                self.scroll_map("down")
        return False

    def check_attack_button_state(self, pos: Object_position) -> bool:
        img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
        img = self.finder.cut_image(img, object_position=pos)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hsv_min = np.array((0, 0, 200))
        hsv_max = np.array((0, 0, 220))

        masc = cv2.inRange(hsv, hsv_min, hsv_max)

        moment = cv2.moments(masc, 1)
        d_area = moment['m00']
        print(d_area)
        if d_area > 1:
            return True
        return False
