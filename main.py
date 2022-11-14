import time

import cv2
import mss


from modules.cv_and_actions import MenuActions
from modules.configs.settings import *
from modules.cv_and_actions.fighter import *
from modules.data_classes.templates import Enemies


def main_loop():

    monitor_manager = Window_manager(window_name=WINDOW_NAME)
    if monitor_manager.width != 424 and monitor_manager.height != 727:
        monitor_manager.set_size_window()
        monitor_manager.update()

    with mss.mss() as screenshot:
        while "BOT WORK":

            obp = Object_position(x1=1171, y1=281, x2=1511, y2=720)

            menu = MenuActions(screenshot=screenshot, monitor_manager=monitor_manager)
            menu.scrolling_mouse(distance=40, speed=0.16, scrolling_area=obp)


            print("END")
            exit()


if __name__ == "__main__":
    main_loop()

