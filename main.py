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

            for i in range(100):
                pos = Object_position(x1=275, y1=357, x2=858, y2=748)
                action = Actions(monitor_manager)
                action.click_random_point_in_the_area(pos)
            break
            # fight = Fighter(monitor_manager=monitor_manager, screenshot=screenshot)
            #
            # still_move = fight.fight([Skills.water_bolt, Skills.ice_vortex, Skills.mind_power, Skills.kick])
            # print("Враг убит за ", still_move, "ход")
            # time.sleep(1000)


if __name__ == "__main__":
    main_loop()

