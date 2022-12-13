import ahk.window
from ahk import AHK
import logging


class Window:
    """
    Обект этого класса содержит информацию о окне
    notebock = Window("Блакнот")
    """
    __window: ahk.window.Window = None
    left: int = 0
    top: int = 0
    width: int = 0
    height: int = 0

    def __init__(self, window_name):
        self.__logger = logging.getLogger(__name__)
        self.__ahk = AHK()
        self.window_name: str = window_name
        self.__get_window_by_name()
        self.window_name = self.__window.title.decode("utf-8")
        self.__window.activate()
        self.update()
        self.__validation_window()
        self.__logger.info(f"""Окно "{self.window_name}" инициализированно.""")

    def __get_window_by_name(self):
        """
        Ищет окно приложения по имени и обновляет self.window
        """
        self.__window = self.__ahk.find_window_by_title(bytes(self.window_name, "utf-8"))
        if not self.__window:
            self.__logger.critical(f"Окно {self.window_name} не найдено!")
            raise Exception(f"Окна с именем '{self.window_name}' не найдено! ")
        self.__logger.debug(f"Окно {self.window_name} найдено.")

    def update(self):
        """
        Обновляет данные объекта
        """
        size = self.__get_position_window()
        self.left = size[0]
        self.top = size[1]
        self.width = size[2]
        self.height = size[3]

        self.__logger.debug(f""" Обновление позиции window.
        Координаты окна '{self.window_name}'  
          left   = {self.left}
          top    = {self.top}
          width  = {self.width}
          height = {self.height}
        """)

    @property
    def monitor(self) -> dict:
        return {"left": self.left, "top": self.top, "width": self.width, "height": self.height}

    def __validation_window(self):
        """
         Проверяет что бы окно было в пределах монитора.
        """
        if self.left < -5000 or self.top < -5000:
            raise Exception("Окно свёрнуто!")

        self.__ahk.mouse_move(self.left, self.top)
        if self.__ahk.get_mouse_position() != (self.left, self.top):
            self.__logger.critical(f"""Окно за пределами монитора!
                                    left = {self.left} 
                                    top = {self.top}
                                    width = {self.width}
                                    top = {self.top}
                                    """)
            raise Exception("Окно за пределами монитора!")

        self.__ahk.mouse_move(self.left + self.width, self.top + self.height)
        if self.__ahk.get_mouse_position() != (self.left + self.width, self.top + self.height):
            self.__logger.critical(f"""Окно за пределами монитора!
                                    left = {self.left} 
                                    top = {self.top}
                                    width = {self.width}
                                    top = {self.top}
                                    """)
            raise Exception("Окно за пределами монитора!")

    def __get_position_window(self) -> tuple:
        return self.__window.rect

    def set_size_window(self, width: int = 424, height: int = 727):
        """Изменяет размеры окна"""
        self.__window.move(width=width, height=height)
        self.update()
        self.__logger.info(f"""Размер окна был изменён\n width = {width}, height = {height}""")
        self.__validation_window()

    def move_window_to(self, x: int = 0, y: int = 0):
        self.__window.move(x=x, y=y)
        self.update()
        self.__logger.info("Окно перемещено программой.")
        self.__validation_window()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bls = Window("Без")
    print(bls.monitor)
