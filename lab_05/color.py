from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QComboBox


class Color(Enum):
    BG = 0
    RED = 1
    BLUE = 2
    BLACK = 3
    GREEN = 4

    def __str__(self) -> str:
        interp = {
            ColorList.BG: 'Фоновый',
            ColorList.RED: 'Красный',
            ColorList.BLUE: 'Синий',
            ColorList.BLACK: 'Черный',
            ColorList.GREEN: 'Зеленый'
        }
        return interp[self]

    def toQcolor(self) -> QColor:
        interp = {
            Color.BG: Qt.white,
            Color.RED: Qt.red,
            Color.BLUE: Qt.blue,
            Color.BLACK: Qt.black,
            Color.GREEN: Qt.green
        }
        return QColor(interp[self])


class ColorList(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

    def get(self) -> Color:
        return Color(self.currentIndex())
