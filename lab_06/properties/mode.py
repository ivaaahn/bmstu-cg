from enum import Enum

from PyQt5.QtWidgets import QComboBox


class Mode(Enum):
    NO_DELAY = 0
    DELAY = 1
    TESTING = -1

    def __str__(self) -> str:
        interp = {
            Mode.NO_DELAY: 'Без задержки',
            Mode.DELAY: 'С задержкой',
            Mode.TESTING: 'Тестирование'
        }
        return interp[self]


class ModeList(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

    def get(self) -> Mode:
        return Mode(self.currentIndex())
