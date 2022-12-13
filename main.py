import random

import mss

from modules.fighter.fighter import Fighter
from modules.window import Window
from modules.telegram_bot import TelegramBot
import logging
import settings

logging.basicConfig(level=logging.DEBUG)


def main():

    monitor_manager = Window(window_name="Blue")
    if monitor_manager.width != 424 and monitor_manager.height != 727:
        monitor_manager.set_size_window(width=424, height=727)
    screenshot = mss.mss()

    fighter = Fighter(monitor_manager=monitor_manager, screenshot=screenshot)

    while True:
        fighter.wait_move(10)


if __name__ == "__main__":
    main()
