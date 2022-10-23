import json
import os
import sys
from settings import ENEMIES_DIR , TEMPLATES_DIR
from modules.data_classes.templates import *

sys.path[0] = f"{os.sep}".join(os.path.dirname(os.path.abspath(__file__)).split(os.sep)[:-2])


# UIs = type("UIs", (), {})
# Enemies = type("Enemies", (), {})

list_enemies = {}
for enemy in os.listdir(ENEMIES_DIR):
    files = os.listdir(PATH_THIS_ENEMY := os.path.join(ENEMIES_DIR, enemy))

    if 'data.json' not in files and 'image.png' not in files:
        break

    with open(os.path.join(PATH_THIS_ENEMY, "data.json", ), encoding='utf-8') as f:
        data = json.load(f)
    list_enemies[data["varname"]] = {"name": data["name"], "precision": data["precision"], "img": os.path.join(PATH_THIS_ENEMY, 'image.png')}

Enemies = type("Enemies", (), list_enemies)




#
# class UI:
#     attack_the_enemy = Template_UI("assets/Templates/UI/attack_the_enemy.png")
#
#
# class Enemies:
#     noob = Template_Enemy("Попрашайка", 0.8, "assets/Templates/Enemies/noob.png")
#     evil_wood = Template_Enemy("Злобный древень", 0.8, "assets/Templates/Enemies/evil_wood.png")
#     forest_wolf = Template_Enemy("Молодой волк", 0.8, "assets/Templates/Enemies/forest_wolf.png")