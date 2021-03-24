from PyQt5.QtWidgets import QMainWindow, QWidget, QTableWidgetItem, QLineEdit, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QBrush, QPen, QPolygon, QPixmap
from loguru import logger

from design.task_popup import Ui_TaskPopup
from design.b_change_popup import Ui_b_change_popup
from errors import ErrorInput
from point import Point


class TaskPopup(QWidget, Ui_TaskPopup):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.okBtn.clicked.connect(self.close)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.close()


class BChangePopup(QWidget, Ui_b_change_popup):
    def __init__(self, astroid: Astroid, lbl_value, repaint_func):
        super().__init__()
        self.setupUi(self)
        self.change_btn.clicked.connect(self.change_coef)
        self.do_repaint = repaint_func
        self.astroid = astroid
        self._lbl_value = lbl_value

    def change_coef(self):
        coef = self._get_coef()
        if coef:
            self.astroid.b = coef
            self._lbl_value.setText(str(coef))
            self.do_repaint()
            self.close()

    def _get_coef(self) -> float or None:
        try:
            data = float(self.box.text())
        except ValueError:
            err = ErrorInput("Коэффициент - вещественное число")
            if err.clickedButton() is QMessageBox.Cancel:
                return None
        else:
            self.box.clear()
            return data

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Enter) or (event.key() == Qt.Key_Return):
            self.change_coef()
