import logging
import time

import mss
import cv2
import numpy as np

from modules.actions.actions import Actions
from modules.computer_vision.base_finder import Finder
from modules.data_classes import Template_Skills, Skills, Object_position, UI, Template
from modules.image.image_actions import Image_actions
from modules.mouse.mouse import Mouse
from modules.window import Window


class Fighter(Actions):

    def __init__(self, monitor_manager: Window, screenshot: mss):
        super(Fighter, self).__init__(monitor_manager=monitor_manager, screenshot=screenshot)
        self.__logger = logging.getLogger(__name__)

    def find_btn_atk(self, wait: float = 1) -> Object_position | None:
        if pos := self.finder.try_find_element(template=Skills.kick, wait=wait):
            self.__logger.debug(f"Кнопка атаки найденна, {pos}")
            return pos
        self.__logger.debug("Кнопка атаки не найденна")
        return None

    def status_move(self, wait: float = 1) -> (bool, Object_position) or (None, None):
        """
        :return: bool стутус хода и его позицию ObjectPosition()
        """

        if position_btn_attack := self.find_btn_atk(wait=wait):
            img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))

            #Получаем фрагмент с изображением кнопки атаки
            img_btn_fight = Image_actions.cut_image_by_obj_pos(img, object_position=position_btn_attack)

            number_true_colors = Image_actions.check_number_of_colors(img_bgr=img_btn_fight, hsv_min=(0, 0, 214), hsv_max=(0, 0, 225))

            if number_true_colors > 1000:
                self.__logger.debug("Ход не доступен")
                return False, position_btn_attack
            else:
                self.__logger.debug("Ход доступен")
                return True, position_btn_attack
        else:
            self.__logger.debug("Не удалось определить статус хода.")
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
                if self.fight_is_end(wait=2):
                    return True

            if move_available is not None:
                if move_available:
                    return pos
        return False

    def fight_is_end(self, wait: float = 4) -> bool:
        if self.find_by_template_and_click_area(template=UI.end_fight, wait=wait):
            self.__logger.info("Нажал кнопку завершить бой.")
            return True
        self.__logger.debug("Кнопка завершения не боя найдено.")
        return False

    def open_skills(self, wait: float = 0.5):
        if self.find_by_template_and_click_area(template=UI.skills_panel, wait=wait, offset=5):
            self.__logger.info("Нажал кнопку с панелью навыков.")
            return True
        self.__logger.info("Кнопки с навыками не найденно найдено.")
        return False


