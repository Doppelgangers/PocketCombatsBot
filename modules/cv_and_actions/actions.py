import time
import random
import pyautogui as pag

from ..data_classes.templates import Template_Enemy
from ..data_classes.data_classes import Object_position
from .finder import Finder


class Actions:

    def __init__(self, monitor_manager):
        self.monitor_manager = monitor_manager

    @staticmethod
    def click_to(x, y):
        pag.moveTo(x, y, 0.05)
        pag.mouseDown()
        time.sleep(random.randrange(31, 109) / 1000)
        pag.mouseUp()

    def find_and_attack(self, enemy: Template_Enemy, img_gray):
        if position_btn_attack := self.__find_a_battle(img_gray=img_gray, enemy=enemy):
            self.__start_a_fight(position_btn_attack)
            return True

    @staticmethod
    def __find_a_battle(img_gray, enemy: Template_Enemy):
        """
        :param img_gray: Чёрно-белый скриншот
        :param enemy: Шаблон врага
        :return: Позицию кнопки атаки
        """
        enemy_position = Finder.find_object(template=enemy, img_gray=img_gray, precision=enemy.precision,
                                            draw_rect_in_gray_img=True)
        if enemy_position:
            attack_position = Finder.find_in_object(template=UI.attack_the_enemy, img_gray=img_gray,
                                                    y1=enemy_position.y1, y2=enemy_position.y2)
            if attack_position:
                return attack_position

    def __start_a_fight(self, attack_position: Object_position):
        """
        Нажимает на кнопку атака в случйном месте
        :param attack_position: координаты поозиция кнопки атаки
        """
        x = random.randint(attack_position.x1, attack_position.x2)
        y = random.randint(attack_position.y1, attack_position.y2)
        self.click_to(self.monitor_manager.monitor.get("left") + x, self.monitor_manager.monitor.get("top") + y)