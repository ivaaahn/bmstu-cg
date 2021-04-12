from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from point import Point


class Canvas(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.surf = QPixmap(3, 3)
        self.surf.fill(Qt.white)

        self.init_sizes: bool = False

    def calc_sizes(self) -> None:
        self.x_min = self.x()
        self.y_min = self.y()

        self.x_max = self.width() + self.x_min
        self.y_max = self.height() + self.y_min

        self.xc = (self.x_min + self.x_max) // 2
        self.yc = (self.y_min + self.y_max) // 2

    @property
    def center_point(self) -> Point:
        return Point(self.xc, self.yc)
