from typing import List, Optional, Tuple

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QObject, QRect
from PyQt5.QtGui import QGuiApplication as QGuiApp
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage, QColor
from PyQt5.QtWidgets import QLabel

import utils
from models.cutter import Cutter
from models.point import Point
from models.segment import Segment
from properties.color import ColorListCutter, ColorListSegment, ColorListResult
from properties.mode import Mode, ModeList


ACCURACY = 15

class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.img = self._new_image()
        self.update_pixmap()
        self._fst_click: Optional[Point] = None
        self._segments: List[Segment] = []
        self._cutter: Optional[Cutter] = None

    def set_objects(self, modes_list: ModeList,
                    cutter_colors: ColorListCutter,
                    segment_colors: ColorListSegment,
                    result_colors: ColorListResult):
        self._modes = modes_list
        self._cutter_colors = cutter_colors
        self._segment_colors = segment_colors
        self._result_colors = result_colors

    def add_segment(self, segment: Segment) -> None:
        self._segments.append(segment)
        self.draw_segment(segment)

    def set_cutter(self, cutter: Cutter) -> None:
        if self._cutter is not None:
            self.clear_canvas()
            self.redraw_segments()

        self._cutter = cutter
        self.draw_cutter(cutter)

    def cut(self) -> None:
        pass

    def clear_all(self) -> None:
        self.clear_canvas()
        self.clear_data()

    def clear_canvas(self) -> None:
        self.img = self._new_image()
        self.update_pixmap()

    def clear_data(self) -> None:
        self._segments.clear()
        self._fst_click = None
        self._cutter = None

    @staticmethod
    def build_segment(start: Point, end: Point, exactly: bool = False) -> Segment:
        if exactly:
            if abs(end.x - start.x) < abs(end.y - start.y):
                end.x = start.x
            else:
                end.y = start.y

        return Segment(start, end)

    @staticmethod
    def build_cutter(p1: Point, p2: Point) -> Cutter:
        return Cutter(Point(min(p1.x, p2.x), max(p1.y, p2.y)), Point(max(p1.x, p2.x), min(p1.y, p2.y)))

    def cutter_is_nearly(self, pos: Point) -> None:
        if abs(pos.x - self._cutter.right) <= ACCURACY:
            pos.x = self._cutter.right
        elif abs(pos.x - self._cutter.left) <= ACCURACY:
            pos.x = self._cutter.left

        if abs(pos.y - self._cutter.top) <= ACCURACY:
            pos.y = self._cutter.top
        elif abs(pos.y - self._cutter.bottom) <= ACCURACY:
            pos.y = self._cutter.bottom

        # return pos

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        position = Point(ev.pos().x(), ev.pos().y()-10)

        if ev.buttons() == Qt.LeftButton:
            if self._cutter is not None and self._modes.get() == Mode.SEGMENTS:
                print(self._cutter.ltop, self._cutter.rbottom)
                print("before", position)
                self.cutter_is_nearly(position)
                print("after", position)

            if self._fst_click is not None:
                if self._modes.get() == Mode.SEGMENTS:
                    exactly = QGuiApp.keyboardModifiers() & Qt.ShiftModifier
                    self.add_segment(self.build_segment(self._fst_click, position, exactly))
                else:
                    self.set_cutter(self.build_cutter(self._fst_click, position))
                self._fst_click = None
            else:
                self._fst_click = position
        elif ev.buttons() == Qt.RightButton and self._fst_click is not None:
            self._fst_click = None

    @staticmethod
    def _new_image() -> QImage:
        img = QImage(utils.W, utils.H, QImage.Format_ARGB32_Premultiplied)
        img.fill(Qt.white)
        return img

    def update_pixmap(self):
        self.pixmap = QPixmap().fromImage(self.img)
        self.setPixmap(self.pixmap)

    def draw_segment(self, segment: Segment) -> None:
        qp = QPainter(self.img)
        qp.setPen(QPen(self._segment_colors.get().toQColor(), 1))  # TODO толщинааа
        print(segment.to_qline())
        qp.drawLine(segment.to_qline())
        qp.end()

        self.update_pixmap()

    def draw_cutter(self, cutter: Cutter) -> None:
        qp = QPainter(self.img)
        qp.setPen(QPen(self._cutter_colors.get().toQColor(), 1))  # TODO толщинааа
        for segment in cutter.get_lines():
            qp.drawLine(segment.to_qline())
        qp.end()
        self.update_pixmap()

    def redraw_segments(self) -> None:
        qp = QPainter(self.img)
        qp.setPen(QPen(self._segment_colors.get().toQColor(), 1))  # TODO толщинааа
        for segment in self._segments:
            qp.drawLine(segment.to_qline())
        qp.end()
        self.update_pixmap()
