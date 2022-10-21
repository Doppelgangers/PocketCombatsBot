import random
import time

import numpy
import pyautogui as pag
import numpy as np
import cv2
import mss
from ahk import AHK
import requests

import mouse

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

    def __init__(self, name, path_image_template):
        name: str = ""
        img: numpy.ndarray = cv2.imread(path_image_template, cv2.IMREAD_GRAYSCALE)


class Templates_Enemies(Template):

    fire_wood = cv2.imread('assets/Templates/Enemies/fire_wood.png', cv2.IMREAD_GRAYSCALE)
    fire_spider = cv2.imread('assets/Templates/Enemies/fire_spider.png', cv2.IMREAD_GRAYSCALE)
    sceleton = cv2.imread('assets/Templates/Enemies/sceleton.png', cv2.IMREAD_GRAYSCALE)
    mini_snake = cv2.imread('assets/Templates/Enemies/mini_snake.png', cv2.IMREAD_GRAYSCALE)
    hydra = cv2.imread('assets/Templates/Enemies/hydra.png', cv2.IMREAD_GRAYSCALE)
    witch = cv2.imread('assets/Templates/Enemies/witch.png', cv2.IMREAD_GRAYSCALE)
    mumu = cv2.imread('assets/Templates/Enemies/mumu.png', cv2.IMREAD_GRAYSCALE)
    sand_man = cv2.imread('assets/Templates/Enemies/sand_man.png', cv2.IMREAD_GRAYSCALE)
    skorpion = cv2.imread('assets/Templates/Enemies/skorpion.png', cv2.IMREAD_GRAYSCALE)
    noob = cv2.imread("assets/Templates/Enemies/noob.png", cv2.IMREAD_GRAYSCALE)
    evil_wood = cv2.imread("assets/Templates/Enemies/evil_wood.png", cv2.IMREAD_GRAYSCALE)
    forest_wolf = cv2.imread("assets/Templates/Enemies/forest_wolf.png", cv2.IMREAD_GRAYSCALE)

class Templates_Skills:
    pass


class Templates_UI:
    attack_the_enemy = cv2.imread("assets/Templates/UI/attack_the_enemy.png", cv2.IMREAD_GRAYSCALE)


class Finder:

    @staticmethod
    def find_object(template, img_gray, precision: float = 0.6, method=cv2.TM_CCOEFF_NORMED, draw_rect_in_gray_img: bool = False):

        position_find_object = {}
        width_template, height_template = template.shape[::-1]
        
        result = cv2.matchTemplate(img_gray, template, method)
        location_of_matches = np.where(result >= precision)
        
        for pt in zip(*location_of_matches[::-1]):

            if draw_rect_in_gray_img:
                cv2.rectangle(img_gray, pt, (pt[0] + width_template, pt[1] + height_template), (0, 0, 255), 1)

            # Координаты найденного обекта, относительно обасти видимости opencv (monitor)
            position_find_object = {
                "lt_X": pt[0],                      # Лево вверх, координаты X
                "lt_Y": pt[1],                      # Лево вверх, координаты Y
                "rb_X": pt[0] + width_template,     # Право низ, координаты X
                "rb_Y": pt[1] + height_template     # Право низ, координаты Y
            }
            break

        return position_find_object


class Actions_Character:

    @staticmethod
    def click_to(position):
        if position:
            pag.moveTo("""""")
            pag.mouseDown()
            time.sleep( random.randrange(31, 109) / 1000 )
            pag.mouseUp()
            return True

    @staticmethod
    def find_fight(img_gray, enemy):
        enemy_position = Finder.find_object(template=enemy, img_gray=img_gray, precision=0.8, draw_rect_in_gray_img=True)
        if enemy_position:
            enemy_area = img_gray[enemy_position["lt_Y"]:enemy_position["rb_Y"]]
            attack_position = Finder.find_object(template=Templates_UI.attack_the_enemy, img_gray=enemy_area, precision=0.7, draw_rect_in_gray_img=True)
            print("Напал", attack_position)
            return attack_position


def main_loop():
    monitor_manager = Window_manager(window_name=Constants.WINDOW_NAME)

    with mss.mss() as screenshot:
        while "Screen capturing":
            img = np.asarray(screenshot.grab(monitor_manager.monitor))
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            first = Actions_Character.find_fight(enemy=Templates_Enemies.evil_wood, img_gray=img_gray)
            second = Actions_Character.find_fight(enemy=Templates_Enemies.forest_wolf, img_gray=img_gray)




            cv2.imshow("BOT", img_gray)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    main_loop()
