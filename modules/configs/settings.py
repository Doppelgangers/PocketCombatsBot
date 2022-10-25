import os
import pathlib

"""PATHS"""
BASE_DIR = pathlib.WindowsPath(os.path.dirname(os.path.abspath(__file__))).parents[1]
TEMPLATES_DIR = os.path.join(BASE_DIR, "assets", "Templates")


"""WINDOW"""
WINDOW_NAME = "BlueStacks"

"""TELEGRAM"""
TELEGRAM_API_KEY = '1219818658:AAERsK7cI_NPgqPz8naLk1EuS8822FtyudM'
TELEGRAM_CHAT_ID = '-1001240340647'


