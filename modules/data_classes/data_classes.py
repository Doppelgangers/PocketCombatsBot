from dataclasses import dataclass


@dataclass
class Object_position:
    x1: float  # Лево вверх, координаты X
    y1: float  # Лево вверх, координаты Y
    x2: float  # Право низ, координаты X
    y2: float  # Право низ, координаты Y

    def top(self):
        return self.y2 - self.y1

    def left(self):
        return self.x2 - self.x1
