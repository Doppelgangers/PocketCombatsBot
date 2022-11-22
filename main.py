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
        # menu.take_loot()
        #
        if menu.find_fight(Enemies.wolf, 5):
            fighter_men.fight_list_skills([Skills.water_bolt, Skills.ice_vortex, Skills.kick, Skills.mind_power ])

        print("END")

        exit()



if __name__ == "__main__":
        # print(Skills.__getattribute__())
        main_loop()


