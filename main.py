import mss

from modules.actions.menu_actions import MenuActions
from modules.configs.settings import *
from modules.data_classes.templates import Enemies, Skills
from modules.fighter import Fighter
from modules.window_manager import Window_manager


def main_loop():

    monitor_manager = Window_manager(window_name=WINDOW_NAME)
    if monitor_manager.width != 424 and monitor_manager.height != 727:
        monitor_manager.set_size_window(width=424, height=727)

    with mss.mss() as screenshot:

        menu = MenuActions(screenshot=screenshot, monitor_manager=monitor_manager)
        fighter_men = Fighter(monitor_manager, screenshot)

        if menu.find_fight(Enemies.fire_spider, 5):
            fighter_men.fight_list_skills([Skills.water_bolt, Skills.ice_vortex, Skills.kick, Skills.mind_power ])


if __name__ == "__main__":
        main_loop()


