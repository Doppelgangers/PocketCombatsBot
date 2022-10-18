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
        self.title_window = window_name
        self.monitor = Window_manager.get_monitor(window_name)

    def __dict__(self):
        return self.monitor

    def __str__(self):
        return self.monitor

    def update(self):
        self.monitor = Window_manager.get_monitor(window_name=self.title_window)

    @staticmethod
    def get_position_window(window_name: str) -> tuple:
        ahk = AHK()
        window = ahk.find_window_by_title( bytes(window_name, "utf-8"))
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


def main_loop():

    monitor_manager = Window_manager(window_name=Constants.WINDOW_NAME)

    with mss.mss() as sct:
        while "Screen capturing":

            img = np.array(sct.grab(monitor_manager.monitor))

            cv2.imshow("BOT", img)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    main_loop()

