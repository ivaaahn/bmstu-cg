from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QComboBox


class Color(Enum):
    BG = 0
    RED = 1
    BLUE = 2
    BLACK = 3
    YELLOW = 4
    ORANGE = 5
    GRAY = 6
    MAGENTA = 7
    GREEN = 8

    def __str__(self) -> str:
        interp = {
            Color.BG: 'Фоновый',
            Color.RED: 'Красный',
            Color.BLUE: 'Синий',
            Color.BLACK: 'Черный',
            Color.YELLOW: 'Жёлтый',
            Color.ORANGE: 'Оранжевый',
            Color.GRAY: 'Серый',
            Color.MAGENTA: 'Фиолетовый',
            Color.GREEN: 'Зеленый'
        }
        return interp[self]

    def toQColor(self) -> QColor:
        interp = {
            Color.BG: Qt.white,
            Color.RED: Qt.red,
            Color.BLUE: Qt.blue,
            Color.BLACK: Qt.black,
            Color.YELLOW: Qt.yellow,
            Color.ORANGE: QColor('#ffa500'),
            Color.GRAY: Qt.gray,
            Color.MAGENTA: Qt.magenta,
            Color.GREEN: Qt.green
        }
        return QColor(interp[self])


class ColorListPoly(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

    def get(self) -> Color:
        return Color(self.currentIndex())


class ColorListResult(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

    def get(self) -> Color:
        return Color(self.currentIndex())


class ColorListCutter(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

    def get(self) -> Color:
        return Color(self.currentIndex())
