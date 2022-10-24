import json
import os

import numpy
import cv2

from modules.settings import ENEMIES_DIR


class Template:

    def __init__(self, path_image_template):
        self.img: numpy.ndarray = cv2.imread(path_image_template, cv2.IMREAD_GRAYSCALE)


class Template_Enemy(Template):

    def __init__(self, name: str, precision: float, path_image_template):
        super().__init__(path_image_template)
        self.name: str = name
        self.precision: float = precision


class Template_Skill(Template):

    def __init__(self, path_image_template):
        super().__init__(path_image_template)


class Template_UI(Template):

    def __init__(self, path_image_template):
        super().__init__(path_image_template)


# UIs = type("UIs", (), {})
# Enemies = type("Enemies", (), {})


def get_enemy():
    list_enemies = {}
    for enemy in os.listdir(ENEMIES_DIR):
        files = os.listdir(PATH_THIS_ENEMY := os.path.join(ENEMIES_DIR, enemy))

        if 'data.json' not in files and 'image.png' not in files:
            break

        with open(os.path.join(PATH_THIS_ENEMY, "data.json", ), encoding='utf-8') as f:
            data = json.load(f)

        list_enemies[data["varname"]] = Template_Enemy(name=data["name"], precision=data["precision"], path_image_template=os.path.join(PATH_THIS_ENEMY, 'image.png'))
    return type("Enemies", (), list_enemies)

