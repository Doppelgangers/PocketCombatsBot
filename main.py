import time

import cv2
import mss

from modules.cv_and_actions import *
from modules.cv_and_actions import Actions
from modules.cv_and_actions.actions import *
from modules.configs.settings import *
from modules.cv_and_actions.fighter import *


def main_loop():

    monitor_manager = Window_manager(window_name=WINDOW_NAME)
    if monitor_manager.width != 424 and monitor_manager.height != 727:
        monitor_manager.set_size_window()
        monitor_manager.update()

    with mss.mss() as screenshot:
        while "BOT WORK":

            test_fighter = Fighter(screenshot=screenshot, monitor_manager=monitor_manager)


            skill_list = [
                Skills.water_bolt,
                Skills.ice_vortex,
                Skills.mind_power,
                Skills.kick
                        ]

            test_fighter.fight_list_skills(skill_list)
            print("END")
            exit()


if __name__ == "__main__":
    main_loop()
    print(Skills.__getattribute__())
