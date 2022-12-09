from dataclasses import dataclass
from modules.window import Window

from modules.window import Window


@dataclass
class Base_object_position:
    x1: int  # Лево вверх, координаты X
    y1: int  # Лево вверх, координаты Y
    x2: int  # Право низ, координаты X
    y2: int  # Право низ, координаты Y

    def height(self) -> int:
        return self.y2 - self.y1

    def wight(self) -> int:
        return self.x2 - self.x1

    def max_x(self) -> int:
        return self.x1 if self.x1 > self.x2 else self.x2

    def max_y(self) -> int:
        return self.y1 if self.y1 > self.y2 else self.y2

    def min_x(self) -> int:
        return self.x1 if self.x1 < self.x2 else self.x2

    def min_y(self) -> int:
        return self.y1 if self.y1 < self.y2 else self.y2

    def get_angle_coordinates(self, corner: str = "lt") -> list[int, int]:
        """
        Получить координаты угла
        :param corner: Название угла.
        lt = left top - левый вверхний угол.
        rt = right top - парвый вверхний угол.
        lb = left bottom - левый нижний угол.
        rb = right bottom - парвый нижний угол.
        :return: 
        [x, y]
        """""
        match corner:
            case "lt":
                x = self.x1 if self.x1 < self.x2 else self.x2
                y = self.y1 if self.y1 > self.y2 else self.y2
            case "rt":
                x = self.x1 if self.x1 > self.x2 else self.x2
                y = self.y1 if self.y1 > self.y2 else self.y2
            case "lb":
                x = self.x1 if self.x1 < self.x2 else self.x2
                y = self.y1 if self.y1 < self.y2 else self.y2
            case "rb":
                x = self.x1 if self.x1 > self.x2 else self.x2
                y = self.y1 if self.y1 < self.y2 else self.y2
            case _:
                raise KeyError("Аргумент " + corner + " не предусмотрен.")
        return [x, y]


@dataclass
class Object_position(Base_object_position):
    is_global_position: bool = False

    def convert_position_to_global(self, window: Window):
        """
        Приимсает Object_position модифицирует его и возвращает
        координаты относитиельо монитора для дальнейшего использования
        например для клика по элементу
        """
        if not self.is_global_position:
            self.is_global_position = True
            left = window.left
            top = window.top
            self.y1 += top
            self.y2 += top
            self.x1 += left
            self.x2 += left
        return self

    def convert_position_to_local(self, window: Window):
        """
        Приимсает Object_position модифицирует его и возвращает
        координаты относитиельо монитора для дальнейшего использования
        например для клика по элементу
        """
        if self.is_global_position:
            self.is_global_position = False
            left = window.left
            top = window.top
            self.y1 -= top
            self.y2 -= top
            self.x1 -= left
            self.x2 -= left
        return self

    def switch_position_global_or_local(self, window: Window):
        if self.is_global_position:
            return self.convert_position_to_local(window)
        else:
            return self.convert_position_to_global(window)
