import time

import mss
import cv2
import numpy as np

from .window_manager import Window_manager
from .finder import Finder
from ..data_classes.templates import Skills


class Fighter:

    def __init__(self, monitor_manager: Window_manager, screenshot: mss):
        self.monitor_manager = monitor_manager
        self.screenshot = screenshot

        self.finder = Finder()

    def find_btn_attack(self, trys: int = 5):
        """
        Ищет позицию кнопки атаки
        :param trys: количество попыток поиска
        :return: координаты кнопки атаки
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

    def status_move(self):
        """
        Если найдена кнопка возвращает её состояние , если кнопки нету тогда возвращает None
        :return: bool стутус хода
        """
        if position_btn_attack := self.find_btn_attack():

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
                return False
                print("Ход не доступен")
            else:
                return True
                print("Ход доступен")
        else:
            return None
