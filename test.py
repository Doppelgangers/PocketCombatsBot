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
        # thresh = cv2.inRange(hsv, np.array((1,0,0)), np.array((255,255,255)))
        thresh = cv2.inRange(hsv, np.array((1,0,160)), np.array((179,30,255)))
        cv2.imshow('image', thresh)
        cv2.waitKey(1)

