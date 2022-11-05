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
    with mss.mss() as screenshot:
        while "BOT WORK":

            actions_hero = Actions(monitor_manager=monitor_manager)
            finder = Finder()
            fight = Fighter(monitor_manager=monitor_manager, screenshot=screenshot)

            fight.status_move()
            # break


        # finder.find_and_cut_object(Enemies)
        # actions_hero.attack_the_enemy(img_gray=img_gray, enemy=Enemies.wolf)
        # finder.find_object(Skills.kick, img_gray, draw_rect_in_gray_img=True)
        # first = actions_hero.find_and_attack(img_gray=img_gray, enemy=Enemies.wolf)
        # if finder.find_object(Skills.kick, img_gray, draw_rect_in_gray_img=True):
        #     print("good")
        #
        #
        #     img = np.asarray(screenshot.grab(monitor_manager.monitor))
        #     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("BOT", img_gray)
        # if cv2.waitKey(25) & 0xFF == ord("q"):
        #     cv2.destroyAllWindows()
        #     break


if __name__ == "__main__":
    main_loop()

