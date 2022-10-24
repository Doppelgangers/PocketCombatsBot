import mss

from modules.cv_and_actions import *
from modules.cv_and_actions.actions import *
from modules.data_classes.templates import get_enemy
from modules.settings import *




def main_loop():
    Enemies = get_enemy()

    monitor_manager = Window_manager(window_name=WINDOW_NAME)
    with mss.mss() as screenshot:
        while "Screen capturing":
            img = np.asarray(screenshot.grab(monitor_manager.monitor))

            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            actions = Actions(monitor_manager)

            first = actions.find_and_attack(img_gray=img_gray, enemy=Enemies.mini_wolf)

            cv2.imshow("BOT", img_gray)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    main_loop()
