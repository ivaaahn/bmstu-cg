from PyQt5 import QtWidgets
from PyQt5.QtCore import QEventLoop

W, H = 1218, 919


def custom_round(num: float) -> int:
    return int(num + (0.5 if num > 0 else -0.5))


def delay():
    QtWidgets.QApplication.processEvents(QEventLoop.AllEvents)
