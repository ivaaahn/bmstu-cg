from enum import Enum
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


class Color(Enum):
    BACK = 0
    RED = 1
    BLUE = 2
    BLACK = 3
    GREEN = 4

    def __str__(self) -> str:
        interp = {
            Color.BACK: 'Фоновый',
            Color.RED: 'Красный',
            Color.BLUE: 'Синий',
            Color.BLACK: 'Черный',
            Color.GREEN: 'Зеленый'
        }
        return interp[self]

    def to_qt(self) -> QColor:
        interp = {
            Color.BACK: Qt.white,
            Color.RED: Qt.red,
            Color.BLUE: Qt.blue,
            Color.BLACK: Qt.black,
            Color.GREEN: Qt.green
        }
        return QColor(interp[self])
