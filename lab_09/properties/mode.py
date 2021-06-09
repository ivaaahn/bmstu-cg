from enum import Enum

from PyQt5.QtWidgets import QComboBox


class Mode(Enum):
    POLY = 0
    CUTTER = 1

    def __str__(self) -> str:
        interp = {
            Mode.POLY: 'Ввод многоугольника',
            Mode.CUTTER: 'Установка отсекателя'
        }
        return interp[self]


class ModeList(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

    def get(self) -> Mode:
        return Mode(self.currentIndex())
