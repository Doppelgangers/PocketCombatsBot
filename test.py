import cv2
import mss
import numpy as np

from modules.configs.settings import WINDOW_NAME
from modules.cv_and_actions import Window_manager

cv2.imread("")
monitor_manager = Window_manager(window_name=WINDOW_NAME)

with mss.mss() as screenshot:
    while True:
        img = np.asarray(screenshot.grab(monitor_manager.monitor))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )

        #Получаем маску
        thresh = cv2.inRange(hsv, np.array((0,0,0)), np.array((0,0,160)))

        #Расширяем области
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
        dilate = cv2.dilate(thresh, kernel, iterations=4)

        "Получаем контуры "
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]


        for c in cnts:
            area = cv2.contourArea(c)
            if 350 < area < 5000:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 3)

        cv2.imshow('thresh', thresh)
        cv2.imshow('dilate', dilate)
        cv2.imshow('image', img)
        cv2.waitKey(1)

