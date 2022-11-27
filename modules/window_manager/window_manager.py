from ahk import AHK


class Window_manager:
    """
    Обект этого класса содержит информацию о расположении и размерах искомого окна
    monitor = Window_manager("Блакнот")

    Если нужно обновить данные положения монитора используйте функцию update. Она обновит данные объекта.
    """

    left: int = 0
    top: int = 0
    width: int = 0
    height: int = 0
    monitor: dict = {"left": 0, "top": 0, "width": 0, "height": 0}

    def __init__(self, window_name):
        self.ahk = AHK()
        self.window_name: str = window_name

        self.window = None
        self.__get_window_by_name()
        self.window.activate()
        self.update()

    def __get_window_by_name(self):
        self.window = self.ahk.find_window_by_title(bytes(self.window_name, "utf-8"))

        if not self.window:
            raise Exception(f"Окна с именем '{self.window_name}' не найдено! ")

    def update(self):
        size = self.__get_position_window()
        self.left = size[0]
        self.top = size[1]
        self.width = size[2]
        self.height = size[3]
        self.monitor: dict = {"left": size[0], "top": size[1], "width": size[2], "height": size[3]}

        if self.left < -10000 or self.top < -10000:
            raise Exception("Окно свёрнуто!")

        self.ahk.mouse_move(self.left, self.top)
        if self.ahk.get_mouse_position() != (self.left, self.top):
            raise Exception("Окно за пределами монитора!")

        self.ahk.mouse_move(self.left+self.width, self.top+self.height)
        if self.ahk.get_mouse_position() != (self.left+self.width, self.top+self.height):
            raise Exception("Окно за пределами монитора!")

    def __get_position_window(self) -> tuple:
        return self.window.rect

    def set_size_window(self, width: int = 424, height: int = 727):
        self.window.move(width=width, height=height)
        self.update()

    def move_window_to(self, x: int = 0, y: int = 0):
        window = self.ahk.find_window_by_title(bytes(self.window_name, "utf-8"))
        window.move(x=x, y=y)
        self.update()



