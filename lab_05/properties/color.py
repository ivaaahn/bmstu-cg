from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QComboBox


class Color(Enum):
    BG = 0
    RED = 1
    BLUE = 2
    GRAY = 3
    YELLOW = 4
    GREEN = 5
    MAGENTA = 6

    FLAG = -1
    POINT = -2

    def __str__(self) -> str:
        interp = {
            Color.BG: 'Фоновый',
            Color.RED: 'Красный',
            Color.BLUE: 'Синий',
            Color.YELLOW: 'Жёлтый',
            Color.GRAY: 'Серый',
            Color.MAGENTA: 'Фиолетовый',
            Color.GREEN: 'Зеленый'
        }
        return interp[self]

    def toQcolor(self) -> QColor:
        interp = {
            Color.BG: Qt.white,
            Color.RED: Qt.red,
            Color.BLUE: Qt.blue,
            Color.YELLOW: Qt.yellow,
            Color.GRAY: Qt.gray,
            Color.MAGENTA: Qt.magenta,
            Color.GREEN: Qt.green,
            Color.POINT: Qt.black,
            Color.FLAG: QColor('#ffa500')
        }
        return QColor(interp[self])


class ColorList(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

    def get(self) -> Color:
        return Color(self.currentIndex())


class ColorListBorder(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

    def get(self) -> Color:
        return Color(self.currentIndex())
