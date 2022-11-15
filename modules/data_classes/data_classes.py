from dataclasses import dataclass


@dataclass
class Object_position:
    x1: int  # Лево вверх, координаты X
    y1: int  # Лево вверх, координаты Y
    x2: int  # Право низ, координаты X
    y2: int  # Право низ, координаты Y

    def height(self):
        return self.y2 - self.y1

    def wight(self):
        return self.x2 - self.x1

    def max_x(self):
        return self.x1 if self.x1 > self.x2 else self.x2

    def max_y(self):
        return self.y1 if self.y1 > self.y2 else self.y2

    def min_x(self):
        return self.x1 if self.x1 < self.x2 else self.x2

    def min_y(self):
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
