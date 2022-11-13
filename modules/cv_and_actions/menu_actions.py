from .baseactions import BaseActions
from ..data_classes.templates import *
from .basefinder import BaseFinder


class MenuActions(BaseActions):

    def __init__(self, monitor_manager, screenshot):
        super().__init__(monitor_manager=monitor_manager, screenshot=screenshot)

    def attack_the_enemy(self, enemy: Template_Enemy, img_gray) -> bool:
        """
        Ищет врага на экране и если находит то атакует
        :param enemy: Шаблон врага
        :param img_gray: скриншот
        :return:
        True атаквал врага
        False не атаквал врага
        """
        if position_btn_attack := self.__find_the_enemy_and_get_position_btn_attack(img_gray=img_gray, enemy=enemy):
            self.click_random_point_in_the_area(position_btn_attack, relative=True)
            return True
        return False

    @staticmethod
    def __find_the_enemy_and_get_position_btn_attack(img_gray, enemy: Template_Enemy):
        """
        :param img_gray: Чёрно-белый скриншот
        :param enemy: Шаблон врага
        :return: Позицию кнопки атаки or None
        """
        enemy_position = BaseFinder.find_object(template=enemy, img_gray=img_gray, draw_rect_in_gray_img=True)

        if enemy_position:
            attack_position = BaseFinder.find_in_object(template=UI.attack_the_enemy, img_gray=img_gray,
                                                        y1=enemy_position.y1, y2=enemy_position.y2, draw_rect_in_gray_img=True)
            if attack_position:
                return attack_position
        return None
