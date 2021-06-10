from typing import List

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtWidgets import QLabel

import utils
from models.point import Point
from models.segment import Segment
from properties.color import Color


class Canvas(QLabel):
    canvas_clicked = pyqtSignal(Point, Qt.MouseButtons)

    def __init__(self, parent):
        super().__init__(parent)
        self.clear()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.canvas_clicked.emit(Point(ev.pos().x(), ev.pos().y()), ev.buttons())

    def clear(self) -> None:
        self.img = self._new_image()
        self._update_pixmap()

    @staticmethod
    def _new_image() -> QImage:
        img = QImage(utils.W, utils.H, QImage.Format_ARGB32_Premultiplied)
        img.fill(Qt.white)
        return img

    def _update_pixmap(self) -> None:
        self.pixmap = QPixmap().fromImage(self.img)
        self.setPixmap(self.pixmap)

    def draw_segments(self, segments: List[Segment], color: Color, is_result: bool = False) -> None:
        qp = QPainter(self.img)

        qp.setPen(QPen(color.toQColor(), is_result + 1))

        for segment in segments:
            qp.drawLine(segment.to_qline())

        qp.end()
        self._update_pixmap()
