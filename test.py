import cv2
import mss
import numpy as np

from modules.configs.settings import WINDOW_NAME
from modules.cv_and_actions import Window_manager


monitor_manager = Window_manager(window_name=WINDOW_NAME)

with mss.mss() as screenshot:
    while True:
        img = np.asarray(screenshot.grab(monitor_manager.monitor))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hsv_min, hsv_max = (1, 70, 192), (23, 72, 194)

        #Получаем маску
        thresh = cv2.inRange(hsv,hsv_min, hsv_max)
        cv2.imshow('image', thresh)
        cv2.waitKey(1)

