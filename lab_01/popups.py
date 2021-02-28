from PyQt5.QtWidgets import QMainWindow, QWidget, QTableWidgetItem, QLineEdit, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QBrush, QPen, QPolygon, QPixmap

import design.add_popup as addUI
import design.edit_popup as editUI
import design.task_popup as taskUI
import design.answer_popup as ansUI

from errors import ErrorInput
from points import Points
from point import Point


class TaskPopup(QWidget, taskUI.Ui_TaskPopup):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.okBtn.clicked.connect(self.close)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.close()


class AnsPopup(QWidget, ansUI.Ui_AnsPopup):
    def __init__(self, text: str):
        super().__init__()
        self.setupUi(self)
        self.okBtn.clicked.connect(self.close)
        self.textPad.setText(text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.close()


class AddPointPopup(QWidget, addUI.Ui_AddPopup):
    def __init__(self, points_table, repaint_func):
        super().__init__()
        self.setupUi(self)
        self.points_table = points_table
        self.addBtn_ok.clicked.connect(self.addPoint)
        self.do_repaint = repaint_func

    def getPointWrapper(self) -> tuple:
        boxes = (self.tbox_x, self.tbox_y)

        try:
            data = (float(boxes[0].text()), float(boxes[1].text()))
        except ValueError:
            err = ErrorInput("Координаты точки - вещественные числа")
            if err.clickedButton() is QMessageBox.Cancel:
                return None
        else:
            self.tbox_x.clear()
            self.tbox_y.clear()
            return data

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Enter) or (event.key() == Qt.Key_Return):
            self.addPoint()

    def addPoint(self):
        data = self.getPointWrapper()
        if data:
            self.points_table.add(Point(point=data))
            self.do_repaint()


class EditPointPopup(QWidget, editUI.Ui_EditPopup):
    def __init__(self, points_table, repaint):
        super().__init__()
        self.setupUi(self)
        self.editBtn_ok.clicked.connect(self.editPoint)

        self._do_repaint = repaint
        self.points_table = points_table
        self._fill_from_old_point()

    def _fill_from_old_point(self):
        row_index = self.points_table.currentRow()
        point_txt = self.points_table.item(row_index, 0).text()

        self.old_point = Point(text=point_txt)

        self.tbox_x.setText(repr(self.old_point.x))
        self.tbox_y.setText(repr(self.old_point.y))

    def getPointWrapper(self) -> tuple:
        boxes_txt = (self.tbox_x.text(), self.tbox_y.text())
        try:
            data = tuple(map(float, boxes_txt))
        except ValueError:
            err = ErrorInput("Координаты точки - вещественные числа")

            if err.clickedButton() is QMessageBox.Cancel:
                return None
        else:
            self.tbox_x.clear()
            self.tbox_y.clear()
            return data

    def editPoint(self):
        data = self.getPointWrapper()
        if data:
            new_point = Point(point=data, label=self.old_point.label)
            self.points_table.editPoint(new_point)
            self._do_repaint()
            self.close()

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Enter) or (event.key() == Qt.Key_Return):
            self.editPoint()
