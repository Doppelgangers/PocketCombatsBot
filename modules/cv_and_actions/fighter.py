import time

import mss
import cv2
import numpy as np

from .window_manager import Window_manager
from .finder import Finder
from ..data_classes.templates import Skills, UI, Template_Skills, Template_UI, Template_Enemy, Template
from .actions import Actions
from ..data_classes.data_classes import Object_position


class Fighter:

    def __init__(self, monitor_manager: Window_manager, screenshot: mss):
        self.monitor_manager = monitor_manager
        self.screenshot = screenshot

        self.finder = Finder()

        self.actions = Actions(monitor_manager=monitor_manager, screenshot=screenshot)

    def fight_list_skills(self, skills: list[Template_Skills]):
        time.sleep(1)
        self.open_skills(wait=1)
        fight = True
        while fight:

            for skill in skills:
                wait_move = self.wait_move(20)

                if type(wait_move) == bool:
                    if wait_move:
                        fight = False
                        break
                    else:
                        raise Exception("Бой прерван")

                if type(wait_move) == Object_position:
                    time.sleep(0.2)
                    if self.find_by_template_and_click_area(template=skill, wait=1):
                        print(f"Использую {skill.name}")
                    time.sleep(0.3)

    def find_btn_attack(self, wait: float = 1) -> Object_position | None:
        return self.try_find_element(template=Skills.kick, wait=wait)

    def status_move(self, wait: float = 1) -> (bool, Object_position) or (None, None):
        """
        :return: bool стутус хода и его позицию ObjectPosition()
        """

        if position_btn_attack := self.find_btn_attack(wait=wait):

            img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))

            #Получаем фрагмент с изображением кнопки атаки
            img_btn_fight = self.finder.cut_image(img, object_position=position_btn_attack)

            hsv = cv2.cvtColor(img_btn_fight, cv2.COLOR_BGR2HSV)

            hsv_min = np.array((0, 0, 214))
            hsv_max = np.array((0, 0, 225))
            masc = cv2.inRange(hsv, hsv_min, hsv_max)
            moment = cv2.moments(masc, 1)
            d_area = moment['m00']
            if d_area > 1000:
                print("Ход не доступен")
                return False, position_btn_attack
            else:
                print("Ход доступен")
                return True, position_btn_attack
        else:
            return None, None

    def wait_move(self, wait: float) -> bool | Object_position:
        """
        :param wait: Время ожидания конца хода
        :return:    {
                    True - сражение завершенно
                    False - за время wait ход не стал доступен
                    Object_position - координаты кнопки атаки
                    }
        """

        start_time = time.perf_counter()
        while time.perf_counter() - start_time < wait:
            move_available, pos = self.status_move(wait=0.9)

            if move_available is None:
                if self.fight_is_end():
                    return True

            if move_available is not None:
                if move_available:
                    return pos

        return False

    def fight_is_end(self, wait: float = 4) -> bool:
        return self.find_by_template_and_click_area(template=UI.end_fight, wait=wait)

    def open_skills(self, wait: float = 0.5):
        return self.find_by_template_and_click_area(template=UI.skills_panel, wait=wait)

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

    def find_by_template_and_click_area(self, template: Template, wait: float = 0.5) -> bool:
        """
        Ищет объект по шаблону и нажимает в случайную точку в его области
        :param template: шаблон
        :param wait: время поиска объекта
        :return: True or False , нажал на объект или нет.
        """
        if pos := self.try_find_element(template=template, wait=wait):
            print(pos)
            self.actions.click_random_point_in_the_area(pos, relative=True, offset=2)
            return True
        return False
