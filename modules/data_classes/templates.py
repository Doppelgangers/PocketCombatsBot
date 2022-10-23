import numpy
import cv2


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
