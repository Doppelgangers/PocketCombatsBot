import time

import mss
import cv2
import numpy as np

from ..window_manager import Window_manager
from ..computer_vision import BaseFinder
from ..data_classes.templates import Skills, UI, Template_Skills, Template_UI, Template_Enemy, Template
from ..actions import BaseActions
from ..data_classes.data_classes import Object_position
from ..actions import Mouse_control


class Fighter:

    def __init__(self, monitor_manager: Window_manager, screenshot: mss):
        self.monitor_manager = monitor_manager
        self.screenshot = screenshot

        self.finder = BaseFinder()

        self.actions = BaseActions(monitor_manager=monitor_manager, screenshot=screenshot)

    def fight_list_skills(self, skills: list[Template_Skills]) -> str:
        """
        Сражение с чередаванием заранее определённых скилов
        :param skills: Список объектов с умениями
        :param is_open_skills: Нужно ли открывать панель с навыками
        :return:
        fight_is_not_found - бой не был найден, возможно его не начали
        fight_is_end вы завершили сражение порожением или победой
        """
        # TODO: Если во время атаки кнопка по какой то причине не прожаласть будет прожат моментально следующий навык
        if not self.actions.try_find_element(template=Skills.kick, wait=1):
            print("fight_is_not_found")
            return "fight_is_not_found"

        self.open_skills(wait=1)

        while "FIGHT!":

            for skill in skills:
                wait_move = self.wait_move(20)

                if type(wait_move) == bool:
                    if wait_move:
                        return "fight_is_end"
                    else:
                        raise Exception("Бой прерван")

                if type(wait_move) == Object_position:
                    time.sleep(0.2)
                    if self.find_by_template_and_click_area(template=skill, wait=1):
                        print(f"Использую {skill.name}")
                    time.sleep(0.3)

    def find_btn_attack(self, wait: float = 1) -> Object_position | None:
        return self.actions.try_find_element(template=Skills.kick, wait=wait)

    def status_move(self, wait: float = 1) -> (bool, Object_position) or (None, None):
        """
        :return: bool стутус хода и его позицию ObjectPosition()
        """

        if position_btn_attack := self.find_btn_attack(wait=wait):

            img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))

            #Получаем фрагмент с изображением кнопки атаки
            img_btn_fight = self.finder.cut_image_by_obj_pos(img, object_position=position_btn_attack)

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
        return self.find_by_template_and_click_area(template=UI.skills_panel, wait=wait, offset=5)

    def find_by_template_and_click_area(self, template: Template, wait: float = 0.5, offset: int = 2) -> bool:
        """
        Ищет объект по шаблону и нажимает в случайную точку в его области
        :param offset:
        :param template: шаблон
        :param wait: время поиска объекта
        :return: True or False , нажал на объект или нет.
        """
        if pos := self.actions.try_find_element(template=template, wait=wait):
            print(pos)
            Mouse_control.click_random_point_in_the_area(pos, monitor_manager=self.monitor_manager, offset=offset)
            return True
        return False
