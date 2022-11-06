import time
import random

import numpy as np
import pyautogui as pag

from ..data_classes.data_classes import Object_position
from .finder import Finder
from ..data_classes.templates import *


class Actions:

    def __init__(self, monitor_manager):
        self.monitor_manager = monitor_manager

    def click_to(self, x, y, click: bool = True, relative_your_screen: bool = False):

        if relative_your_screen:
            x += self.monitor_manager.monitor.get("left")
            y += self.monitor_manager.monitor.get("top")

        pag.moveTo(x, y)

        if click:
            pag.mouseDown()
            time.sleep(random.randrange(31, 109) / 1000)
            pag.mouseUp()

    def attack_the_enemy(self, enemy: Template_Enemy, img_gray):
        """
        Ищет врага на экране и если находит то атакует
        :param enemy:
        :param img_gray:
        :return:
        """
        if position_btn_attack := self.find_the_enemy_and_get_position_btn_attack(img_gray=img_gray, enemy=enemy):
            self.click_random_point_in_the_area(position_btn_attack)
            return True

    @staticmethod
    def find_the_enemy_and_get_position_btn_attack(img_gray, enemy: Template_Enemy):
        """
        :param img_gray: Чёрно-белый скриншот
        :param enemy: Шаблон врага
        :return: Позицию кнопки атаки or None
        """
        enemy_position = Finder.find_object(template=enemy, img_gray=img_gray, draw_rect_in_gray_img=True)

        if enemy_position:
            attack_position = Finder.find_in_object(template=UI.attack_the_enemy, img_gray=img_gray,
                                                    y1=enemy_position.y1, y2=enemy_position.y2, draw_rect_in_gray_img=True)
            if attack_position:
                return attack_position

    def get_a_position_relative_to_the_screen(self, position: Object_position):
        left = self.monitor_manager.monitor.get("left")
        top = self.monitor_manager.monitor.get("top")
        position.y1 += top
        position.y2 += top
        position.x1 += left
        position.x2 += left
        return position

    def click_random_point_in_the_area(self, attack_position: Object_position):
        """
        Нажимает на кнопку атака в случйном месте
        :param relative:
        :param attack_position: координаты поозиция кнопки атаки
        """

        attack_position_rel = self.get_a_position_relative_to_the_screen(attack_position)

        x = random.randint(int(attack_position.x1), int(attack_position.x2))
        y = random.randint(int(attack_position.y1), int(attack_position.y2))
        self.click_to(x=x, y=y)


