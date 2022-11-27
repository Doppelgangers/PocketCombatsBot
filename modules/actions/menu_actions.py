import time

import numpy as np

from .baseactions import BaseActions
from ..data_classes.data_classes import Object_position
from ..data_classes.templates import *
from ..computer_vision.basefinder import BaseFinder
from .mouse_control import Mouse_control


class MenuActions(BaseActions):

    def __init__(self, monitor_manager, screenshot):
        super().__init__(monitor_manager=monitor_manager, screenshot=screenshot)
        self.SCROLL_AREA = Object_position(x1=202, y1=318, x2=379, y2=642)
        self.SCROLL_AREA.convert_position_to_global(monitor_manager)

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
                Mouse_control.click_random_point_in_the_area(position_btn_attack, monitor_manager=self.monitor_manager)
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
        Mouse_control.scrolling_mouse_for_area(area=self.SCROLL_AREA, scroll_to=scroll_to, speed=0.18)

    def find_fight(self, enemy: Template_Enemy, wait: int) -> bool:
        start_time = time.perf_counter()
        cooldown = False
        while time.perf_counter() - start_time < wait or cooldown:

            img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            atk = self.attack_the_enemy(enemy=enemy, img_gray=img_gray)
            self.take_loot()

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

    def check_attack_button_state(self, pos: Object_position) -> bool:
        img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
        img = self.finder.cut_image_by_obj_pos(img, object_position=pos)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hsv_min = np.array((0, 0, 200))
        hsv_max = np.array((0, 0, 220))

        masc = cv2.inRange(hsv, hsv_min, hsv_max)

        moment = cv2.moments(masc, 1)
        d_area = moment['m00']
        if d_area > 1:
            return True
        return False

    def checking_end_of_scroll(self) -> bool:
        """
        Проверяет появляется волна окончания прокрутки
        :return: True если конец страницы
        """
        img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        min_hsv = np.array((1, 0, 160))
        max_hsv = np.array((179, 30, 255))

        masc = cv2.inRange(hsv, min_hsv, max_hsv)
        moment = cv2.moments(masc, 1)
        d_area = moment['m00']
        if d_area > 10_000:
            return True
        return False

    def __find_first_item_in_loot(self, position_loot_panel: Object_position) -> Object_position | None:
        """
        Ищет первый попавшейся текст ниже координат что переданы , и возвращает позицию текста
        :param position_loot_panel:
        :return: Object_position
        """
        img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
        img = self.finder.cut_image_by_coordinates(img, y1=position_loot_panel.y2)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Получаем маску
        thresh = cv2.inRange(hsv, np.array((0, 0, 0)), np.array((0, 0, 160)))

        # Расширяем области
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
        dilate = cv2.dilate(thresh, kernel, iterations=4)

        "Получаем контуры "
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        if cnts:
            area = cv2.contourArea(cnts[-1])
            if 350 < area < 5000:
                x, y, w, h = cv2.boundingRect(cnts[-1])
                obp = Object_position(x, y+position_loot_panel.y2, x+w, y+h+position_loot_panel.y2)
                obp.convert_position_to_global(self.monitor_manager)
                return obp
            return None

    def take_loot(self):
        img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        pos_loot_panel = self.finder.find_object(template=UI.loot_panel, img_gray=img_gray)

        if pos_loot_panel:

            if pos_close_panel := self.finder.find_in_object(img_gray=img_gray, y1=pos_loot_panel.y1, y2=pos_loot_panel.y2, template=UI.close_panel):
                """
                Если закрыто то открываем вкладку.
                """
                Mouse_control.click_random_point_in_the_area(pos_close_panel, monitor_manager=self.monitor_manager)

            if self.finder.find_in_object(img_gray=img_gray, y1=pos_loot_panel.y1, y2=pos_loot_panel.y2, template=UI.open_panel):
                """
                Ескли вкладка открыта начинаем процесс сбора лута.
                """
                while True:
                    pos_loot = self.__find_first_item_in_loot(position_loot_panel=pos_loot_panel)
                    if pos_loot:
                        Mouse_control.click_random_point_in_the_area(pos_loot, monitor_manager=self.monitor_manager, offset=2, duration_min=60, duration_max=100)

                        time.sleep(0.15)

                        img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
                        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        hsv_min, hsv_max = (1, 70, 192), (23, 72, 194)

                        if pos_pick_up := self.finder.find_object(template=UI.pick_up, img_gray=img_gray):

                            img = self.finder.cut_image(img=img, object_position=pos_pick_up)
                            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                            masc = cv2.inRange(hsv, hsv_min, hsv_max)
                            moment = cv2.moments(masc, 1)
                            d_area = moment['m00']

                            if d_area > 1:
                                return pos_pick_up
                        else:
                            self.scroll_map(scroll_to="down")
                            if not self.finder.find_object(template=UI.pick_up, img_gray=img_gray):
                                break
                    else:
                        break
