import cv2
import time
import numpy as np

from modules.actions import Mouse_control
from modules.data_classes import Object_position
from modules.data_classes.templates import UI
from modules.image_controller.image_controller import Image_controller


def find_first_item_in_loot(self, position_loot_panel: Object_position) -> Object_position | None:
    """
    Ищет первый попавшейся текст ниже координат что переданы , и возвращает позицию текста
    :param position_loot_panel:
    :return: Object_position
    """
    img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
    img = Image_controller.cut_image_by_coordinates(img, y1=position_loot_panel.y2)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Получаем маску
    thresh = cv2.inRange(hsv, np.array((0, 0, 0)), np.array((0, 0, 160)))

    # Расширяем области
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    "Получаем контуры "
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    if cnts:
        area = cv2.contourArea(cnts[-1])
        if 350 < area < 5000:
            x, y, w, h = cv2.boundingRect(cnts[-1])
            obp = Object_position(x, y + position_loot_panel.y2, x + w, y + h + position_loot_panel.y2)
            obp.convert_position_to_global(self.monitor_manager)
            return obp
        return None


def take_loot(self):
    img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    pos_loot_panel = self.finder.find_object(template=UI.loot_panel, img_gray=img_gray)

    if pos_loot_panel:

        if pos_close_panel := self.finder.find_in_object(img_gray=img_gray, y1=pos_loot_panel.y1, y2=pos_loot_panel.y2,
                                                         template=UI.close_panel):
            """
            Если закрыто то открываем вкладку.
            """
            Mouse_control.click_random_point_in_the_area(pos_close_panel, monitor_manager=self.monitor_manager)

        if self.finder.find_in_object(img_gray=img_gray, y1=pos_loot_panel.y1, y2=pos_loot_panel.y2,
                                      template=UI.open_panel):
            """
            Ескли вкладка открыта начинаем процесс сбора лута.
            """
            while True:
                pos_loot = self.find_first_item_in_loot(position_loot_panel=pos_loot_panel)
                if pos_loot:
                    Mouse_control.click_random_point_in_the_area(pos_loot, monitor_manager=self.monitor_manager,
                                                                 offset=2, duration_min=60, duration_max=100)

                    time.sleep(0.15)

                    img = np.asarray(self.screenshot.grab(self.monitor_manager.monitor))
                    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    hsv_min, hsv_max = (1, 70, 192), (23, 72, 194)

                    if pos_pick_up := self.finder.find_object(template=UI.pick_up, img_gray=img_gray):

                        img = self.finder.cut_image(img=img, object_position=pos_pick_up)

                        number_true_colors = Image_controller.check_number_of_colors(img, hsv_min, hsv_max)

                        if number_true_colors > 1:
                            return pos_pick_up
                    else:
                        self.scroll_map(scroll_to="down")
                        if not self.finder.find_object(template=UI.pick_up, img_gray=img_gray):
                            break
                else:
                    break
