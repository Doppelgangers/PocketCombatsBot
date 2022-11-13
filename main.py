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

            menu = MenuActions(screenshot=screenshot, monitor_manager=monitor_manager)
            test_fighter = Fighter(screenshot=screenshot, monitor_manager=monitor_manager)
            skill_list = [Skills.kick]

            img = np.asarray(screenshot.grab(monitor_manager.monitor))
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            print(menu.attack_the_enemy(img_gray=img_gray, enemy=Enemies.wolf))

            print(test_fighter.fight_list_skills(skill_list))
            print("END")
            exit()


if __name__ == "__main__":
    main_loop()
    print(Skills.__getattribute__())
