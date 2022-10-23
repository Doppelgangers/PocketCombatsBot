import numpy
import numpy as np
import cv2
import mss

from modules.cv_and_actions import Window_manager
from modules.cv_and_actions import *
from modules.telegtam_bot import TelegramBot
from modules.cv_and_actions.actions import *


def main_loop():
    monitor_manager = Window_manager(window_name=Constants.WINDOW_NAME)
    with mss.mss() as screenshot:
        while "Screen capturing":
            img = np.asarray(screenshot.grab(monitor_manager.monitor))

            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            actions = Actions(monitor_manager)

            first = actions.find_and_attack(img_gray=img_gray, enemy=Enemies.forest_wolf)

            cv2.imshow("BOT", img_gray)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    main_loop()
