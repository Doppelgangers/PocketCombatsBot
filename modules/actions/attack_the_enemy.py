import numpy as np

from .mouse_control import Mouse_control
from ..computer_vision import BaseFinder
from ..data_classes import Object_position
from ..data_classes.templates import *
from ..image_controller.image_controller import Image_controller
from ..window_manager import Window_manager


class Attack_the_enemy:

    def __init__(self, monitor_manager: Window_manager, screenshot):
        self.monitor_manager = monitor_manager
        self.screenshot = screenshot

    def attack_the_enemy(self, enemy: Template_Enemy, img_gray) -> bool | str:
        """
        Ищет врага на экране и если находит то атакует
        :param monitor_manager:
        :param enemy: Шаблон врага
        :param img_gray: скриншот
        :return:
        True атаквал врага
        False не атаквал врага
        """
        if position_btn_attack := self.find_the_enemy_and_get_position_btn_attack(img_gray=img_gray, enemy=enemy):
            if self.check_attack_button_state(position_btn_attack):
                Mouse_control.click_random_point_in_the_area(position=position_btn_attack, monitor_manager=self.monitor_manager)
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

    def check_attack_button_state(self, pos: Object_position) -> bool:
        img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
        img = Image_controller.cut_image_by_obj_pos(img, object_position=pos)

        number_true_colors = Image_controller.check_number_of_colors(img, (0, 0, 200), (0, 0, 220))
        if number_true_colors > 1:
            return True
        return False
