import time

import mss
import cv2
import numpy as np

from .window_manager import Window_manager
from .finder import Finder
from ..data_classes.templates import Skills, UI, Template_Skills
from .actions import Actions


class Fighter:

    def __init__(self, monitor_manager: Window_manager, screenshot: mss):
        self.monitor_manager = monitor_manager
        self.screenshot = screenshot

        self.finder = Finder()

        self.actions = Actions(monitor_manager=monitor_manager)

    def fight(self, skills_list: list = []):
        move = 0
        self.open_skills()
        while True:

            for skill in skills_list:

                trys = 20
                while trys:
                    if self.status_move(2):
                        self.use_skill(skill_template=skill)
                        move += 1
                    trys -= 1

                if self.fight_is_end():
                    return move

    def find_btn_attack(self, trys: int = 5):
        """
        Ищет позицию кнопки атаки
        :param trys: количество попыток поиска
        :return: координаты кнопки атаки или None
        """
        while trys:
            print("Попытка", trys)
            img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            if pos := self.finder.find_object(template=Skills.kick, img_gray=img_gray):
                print("Кнопка найдена", pos)
                return pos

            trys -= 1
            time.sleep(0.9)
        else:
            print("Не найдена кнопка атаки ")
            return None

    def status_move(self, trys_find_atk: int = 5):
        """
        Если найдена кнопка возвращает её состояние , если кнопки нету тогда возвращает None
        :return: bool стутус хода и его позицию ObjectPosition()
        """

        if position_btn_attack := self.find_btn_attack(trys=trys_find_atk):

            img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            img_btn_fight = self.finder.cut_image(img, object_position=position_btn_attack)

            hsv = cv2.cvtColor(img_btn_fight, cv2.COLOR_BGR2HSV)

            hsv_min = np.array((0, 0, 214))
            hsv_max = np.array((0, 0, 225))
            masc = cv2.inRange(hsv, hsv_min, hsv_max)
            moment = cv2.moments(masc, 1)
            dArea = moment['m00']
            if dArea > 1000:
                print("Ход не доступен")
                return False, position_btn_attack
            else:
                print("Ход доступен")
                return True, position_btn_attack
        else:
            return None, None

    def fight_is_end(self, trys: int = 5):
        pos = self.try_find_element(template=UI.end_fight, trys=trys)
        if pos:
            self.actions.click_random_point_in_the_area(pos)
            return True
        return False

    def open_skills(self, trys: int = 5):
        if pos := self.try_find_element(template=UI.skills_panel, trys=trys):
            self.actions.click_random_point_in_the_area(pos)
            return True
        return False

    def try_find_element(self, template, trys: int = 5):

        while trys:
            print("Ищю ")
            img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            if pos := self.finder.find_object(template=template, img_gray=img_gray):
                return pos

            trys -= 1
            time.sleep(0.9)
        else:
            return None

    def use_skill(self, skill_template: Template_Skills, trys: int = 3):
        if pos := self.try_find_element(skill_template, trys=trys):
            self.actions.click_random_point_in_the_area(pos)
            return True
        return False



