import random
import time

import ahk
import cv2
import mss


from modules.cv_and_actions import MenuActions
from modules.configs.settings import *
from modules.cv_and_actions.fighter import *
from modules.data_classes.templates import Enemies


def main_loop():

    monitor_manager = Window_manager(window_name=WINDOW_NAME)
    if monitor_manager.width != 424 and monitor_manager.height != 727:
        monitor_manager.set_size_window(width=424, height=727)

    with mss.mss() as screenshot:
        menu = MenuActions(screenshot=screenshot, monitor_manager=monitor_manager)
        fighter_men = Fighter(monitor_manager, screenshot)
        for i in range(3):

            if menu.find_fight(Enemies.wolf, 5):
                fighter_men.fight_list_skills([Skills.kick])

            print("END")



if __name__ == "__main__":

        main_loop()


