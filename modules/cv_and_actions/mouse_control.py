import pyautogui as pag
import time
import random

from modules.data_classes.data_classes import Object_position
from modules.cv_and_actions.window_manager import Window_manager


class Mouse_control:

    @staticmethod
    def click_to(x, y, click: bool = True, relative_your_screen: bool = False, duration_min: int = 38, duration_max: int = 93):
        pag.moveTo(x, y)

        if click:
            pag.mouseDown()
            time.sleep(random.randrange(duration_min, duration_max) / 1000)
            pag.mouseUp()

    @staticmethod
    def click_random_point_in_the_area(position: Object_position, monitor_manager: Window_manager, offset: int = 1, duration_min: int = 31, duration_max: int = 83):
        """
        Нажимает на кнопку атака в случйном месте объекта
        :param monitor_manager:
        :param offset: отступ в px во внутрь области
        :param position: координаты элемента
        :param duration_max:
        :param duration_min:
        """
        position.convert_position_to_global(monitor_manager=monitor_manager)
        x = random.randint(position.x1+offset, position.x2-offset)
        y = random.randint(position.y1+offset, position.y2-offset)
        Mouse_control.click_to(x=x, y=y, duration_min=duration_min, duration_max=duration_max)

    @staticmethod
    def scrolling_mouse(x1: int, y1: int, x2: int, y2: int, speed: float = 0.16):
        """

        :param x1: Начальная координата по оси x
        :param y1: Начальная координата по оси y
        :param y2: Конечная координата по оси x
        :param x2: Конечная координата по оси y
        :param speed: Скорость прокрутки (в секундаж) >= 0.2 sec
        :return: None
        """
        pag.moveTo(x1, y1)
        pag.mouseDown()
        speed = random.uniform(speed-0.05, speed+0.05)
        pag.moveTo(x2, y2, speed)
        pag.mouseUp()

    @staticmethod
    def scrolling_mouse_for_area(area: Object_position, scroll_to: str = "down", speed: float = 0.16):
        """

        :param area: облать по которой будем скорллить
        :param speed: скорость скролла
        :param scroll_to: Направление прокрутки "up" or "down"
        """
        #TODO Координаты выбираются весьма странно , переделать!
        start_x = random.randint(area.min_x(), area.max_x()-20) #случайная область по координате X
        start_y = random.randint(area.max_y()-20, area.max_y()) # нижняя область с погрешностью 20px вверх

        end_x = start_x
        end_y = random.randint(area.min_y(), area.min_y() + 20)

        match scroll_to:
            case "up":
                start_x, end_x = end_x, start_x
                start_y, end_y = end_y, start_y
            case "down":
                pass
            case _:
                raise KeyError("Аргумент " + scroll_to + " не предусмотрен.")
        Mouse_control.scrolling_mouse(x1=start_x, y1=start_y, x2=end_x, y2=end_y, speed=speed)
