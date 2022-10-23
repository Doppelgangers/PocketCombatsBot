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
        self.window_name: str = window_name
        self.update()

    def update(self):
        size = self.__get_position_window(self.window_name)
        self.left = size[0]
        self.top = size[1]
        self.width = size[2]
        self.height = size[3]
        self.monitor: dict = {"left": size[0], "top": size[1], "width": size[2], "height": size[3]}

        if self.left < 0 or self.top < 0:
            raise Exception("Окно находится за пределами монитора!")

    @staticmethod
    def __get_position_window(window_name: str) -> tuple:
        ahk = AHK()
        window = ahk.find_window_by_title(bytes(window_name, "utf-8"))
        "(1684, 0, 1366, 728) == (x1, y1, x2, y2) лево верх и ширина и высота "
        if not window:
            raise Exception(f"Окна с именем '{window_name}' не найдено! ")
        return window.rect
