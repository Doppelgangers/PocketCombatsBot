import json
import os
import cv2
import numpy

from modules.configs.settings import TEMPLATES_DIR


class Template:

    path_folder = ''

    def __init__(self, img, precision: float = 0.8):
        self.img: numpy.ndarray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        self.precision = precision


class Template_Enemy(Template):

    path_folder = os.path.join(TEMPLATES_DIR, "Enemies")

    def __init__(self, img, name: str, precision: float = 0.8, **kwargs):
        super(Template_Enemy, self).__init__(img=img, precision=precision)
        self.name = name


class Template_UI(Template):

    path_folder = os.path.join(TEMPLATES_DIR, "UI")

    def __init__(self, img, precision: float = 0.8, **kwargs):
        super(Template_UI, self).__init__(img=img, precision=precision)


@classmethod
def get_atributes(cls):
    class_atr = cls.__dict__.keys()
    list_atributes = []
    for atr in class_atr:
        if atr[0] == "_":
            break
        list_atributes.append(atr)
    return list_atributes


def get_templates(use_class) -> type:
    list_templates = {}
    for enemy in os.listdir(use_class.path_folder):
        path_this_enemy = os.path.join(use_class.path_folder, enemy)
        json_file = ''
        png_file = ''

        for file in os.listdir(path_this_enemy):
            if "json" in file.split("."):
                json_file = file
            if "png" in file.split("."):
                png_file = file

        if not json_file and png_file:
            raise Exception(f"В папке {path_this_enemy} должен быть png шаблон, и json конфигурация!")

        with open(os.path.join(path_this_enemy, json_file), "r", encoding="utf-8") as f:
            info_enemy = json.load(f)

        info_enemy['img'] = os.path.join(path_this_enemy, png_file)

        list_templates[enemy] = use_class(**info_enemy)
    list_templates["__getattribute__"] = get_atributes
    return type(use_class.__name__, (), list_templates)


Enemies = get_templates(Template_Enemy)
UI = get_templates(Template_UI)
