import random
import time

import numpy
import pyautogui as pag
import numpy as np
import cv2
import mss
from ahk import AHK
import requests


class TelegramBot:
    api_token = ""
    chat_id = ""
    name = ""

    def say(self, msg):
        requests.get(f'https://api.telegram.org/bot{self.api_token}/sendMessage', params=dict(
            chat_id=self.chat_id,
            text=f""" {self.name}, {msg} """
        ))


class Constants:
    WINDOW_NAME = "BlueStacks"
    TELEGRAM_API_KEY = '1219818658:AAERsK7cI_NPgqPz8naLk1EuS8822FtyudM'
    TELEGRAM_CHAT_ID = '-1001240340647'


class Window_manager:

    def __init__(self, window_name):
        self.title_window: str = window_name
        self.monitor: dict = Window_manager.get_monitor(window_name)

    def update(self):
        self.monitor = Window_manager.get_monitor(window_name=self.title_window)

    @staticmethod
    def get_position_window(window_name: str) -> tuple:
        ahk = AHK()
        window = ahk.find_window_by_title(bytes(window_name, "utf-8"))
        "(1684, 0, 1366, 728) == (x1, y1, x2, y2) лево верх и ширина и высота "
        return window.rect if window else ()

    @staticmethod
    def convert_pos_windows_to_monitor(position: tuple) -> dict:
        mon = {"left": position[0], "top": position[1], "width": position[2], "height": position[3]}
        return mon

    @staticmethod
    def get_monitor(window_name: str) -> dict:
        # monitor = {"top": 100, "left": 100, "width": 200, "height": 200}
        return Window_manager.convert_pos_windows_to_monitor(Window_manager.get_position_window(window_name))


class Template:

    def __init__(self, path_image_template):
        self.img: numpy.ndarray = cv2.imread(path_image_template, cv2.IMREAD_GRAYSCALE)


class Template_Enemy(Template):

    def __init__(self, name, path_image_template):
        super().__init__(path_image_template)
        self.name: str = name


class Template_Skill(Template):

    def __init__(self, path_image_template):
        super().__init__(path_image_template)


class Template_UI(Template):

    def __init__(self, path_image_template):
        super().__init__(path_image_template)


class UI:
    attack_the_enemy = Template_UI("assets/Templates/UI/attack_the_enemy.png")


class Enemies:
    noob = Template_Enemy("Попрашайка", "assets/Templates/Enemies/noob.png")
    evil_wood = Template_Enemy("Злобный древень", "assets/Templates/Enemies/evil_wood.png")
    forest_wolf = Template_Enemy("Молодой волк", "assets/Templates/Enemies/forest_wolf.png")


class Finder:

    @staticmethod
    def find_object(template, img_gray, precision: float = 0.6, method=cv2.TM_CCOEFF_NORMED,
                    draw_rect_in_gray_img: bool = False):

        position_find_object = {}
        width_template, height_template = template.shape[::-1]

        result = cv2.matchTemplate(img_gray, template, method)
        location_of_matches = np.where(result >= precision)

        for pt in zip(*location_of_matches[::-1]):

            if draw_rect_in_gray_img:
                cv2.rectangle(img_gray, pt, (pt[0] + width_template, pt[1] + height_template), (0, 0, 255), 1)

            # Координаты найденного обекта, относительно обасти видимости opencv (monitor)
            position_find_object = {
                "lt_X": pt[0],  # Лево вверх, координаты X
                "lt_Y": pt[1],  # Лево вверх, координаты Y
                "rb_X": pt[0] + width_template,  # Право низ, координаты X
                "rb_Y": pt[1] + height_template  # Право низ, координаты Y
            }
            break

        return position_find_object

    @staticmethod
    def find_in_object(template, img_gray, y1, y2, precision: float = 0.6, draw_rect_in_gray_img: bool = False):
        cut_img_gray = img_gray[y1:y2]

        local_position = Finder.find_object(template=template, img_gray=cut_img_gray, precision=precision, draw_rect_in_gray_img=draw_rect_in_gray_img)
        if local_position:
            local_position["lt_Y"] += y1
            local_position["rb_Y"] += y1
            return local_position


class Actions_Character:

    def __init__(self, monitor_manager):
        self.monitor_manager = monitor_manager

    @staticmethod
    def click_to(x, y):
        pag.moveTo(x, y, 0.05)
        pag.mouseDown()
        time.sleep(random.randrange(31, 109) / 1000)
        pag.mouseUp()

    def find_fight(self, img_gray, enemy):
        enemy_position = Finder.find_object(template=enemy.img, img_gray=img_gray, precision=0.8,
                                            draw_rect_in_gray_img=True)
        if enemy_position:
            attack_position = Finder.find_in_object(UI.attack_the_enemy.img, img_gray, enemy_position["lt_Y"], enemy_position["rb_Y"])
            if attack_position:
                self.start_a_fight(attack_position)
        return True


    def start_a_fight(self, attack_position: dict):
        x = random.randint(attack_position.get("lt_X"), attack_position.get("rb_X"))
        y = random.randint(attack_position.get("lt_Y"), attack_position.get("rb_Y"))
        Actions_Character.click_to(self.monitor_manager.monitor.get("left") + x, self.monitor_manager.monitor.get("top") + y)


def main_loop():
    monitor_manager = Window_manager(window_name=Constants.WINDOW_NAME)

    with mss.mss() as screenshot:
        while "Screen capturing":
            img = np.asarray(screenshot.grab(monitor_manager.monitor))
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            actions = Actions_Character(monitor_manager)

            first = actions.find_fight(enemy=Enemies.forest_wolf, img_gray=img_gray)
            second = actions.find_fight(enemy=Enemies.evil_wood, img_gray=img_gray)

            cv2.imshow("BOT", img_gray)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    main_loop()
