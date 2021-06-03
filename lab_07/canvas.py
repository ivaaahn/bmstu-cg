from typing import List, Optional

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication as QGuiApp
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtWidgets import QLabel, QMessageBox

import utils
from algorithms import Algorithms
from models.cutter import Cutter
from models.point import Point
from models.segment import Segment
from properties.color import ColorListCutter, ColorListSegment, ColorListResult
from properties.mode import Mode, ModeList

INTO = 0b0000
LEFT = 0b0001
RIGHT = 0b0010
BOTTOM = 0b0100
TOP = 0b1000


class Canvas(QLabel):
    def __init__(self, parent):
        self._accuracy = 15
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
        self._modes.currentTextChanged.connect(self.mode_changed)
        self._cutter_colors = cutter_colors
        self._segment_colors = segment_colors
        self._result_colors = result_colors

    def add_segment(self, segment: Segment) -> None:
        self._segments.append(segment)
        self.draw_segment(segment)

    def mode_changed(self, value):
        self._fst_click = None

    def set_cutter(self, cutter: Cutter) -> None:
        if self._cutter is not None:
            self.clear_canvas()
            self.redraw_segments()

        self._cutter = cutter
        self.draw_cutter(cutter)

    def set_bits(self, segment: Segment):
        cutter = self._cutter

        for point in segment.points:
            code = 0b0000
            if point.x < cutter.left:
                code |= LEFT
            elif point.x > cutter.right:
                code |= RIGHT

            if point.y < cutter.bottom:
                code |= BOTTOM
            elif point.y > cutter.top:
                code |= TOP

            point.code = code

    def handle_segment(self, seg: Segment):
        cutter = self._cutter
        self.set_bits(seg)

        # Полностью видимый
        if not(seg.p1.code | seg.p2.code):
            self.draw_segment(seg, result=True)
            return

        # Полностью невидимый
        if seg.p1.code & seg.p2.code != 0:
            return

        points_to_handle: List[Point] = []
        result: List[Point] = []

        if seg.p1.code == 0:
            result.append(seg.p1)
            points_to_handle.append(seg.p2)
        elif seg.p2.code == 0:
            result.append(seg.p2)
            points_to_handle.append(seg.p1)
        else:
            points_to_handle.extend(seg.points)

        for point in points_to_handle:
            if seg.is_vertical():
                if point.y > self._cutter.top:
                    result.append(Point(point.x, self._cutter.top))
                else:
                    result.append(Point(point.x, self._cutter.bottom))
                continue

            m: float = seg.tangent

            if point.code & LEFT:
                y = round(m * (cutter.left - point.x) + point.y)
                if cutter.bottom <= y <= cutter.top:
                    result.append(Point(cutter.left, y))
                    continue

            elif point.code & RIGHT:
                y = round(m * (cutter.right - point.x) + point.y)
                if cutter.bottom <= y <= cutter.top:
                    result.append(Point(cutter.right, y))
                    continue

            # Заметим, что в случае горизонтальной прямой сюда мы не попадем
            # горизонтальная прямая либо обработается в самом начале подпрограммы, либо выше
            if point.code & TOP:
                x = round((cutter.top - point.y) / m + point.x)
                if cutter.left <= x <= cutter.right:
                    result.append(Point(x, cutter.top))
                    continue

            elif point.code & BOTTOM:
                x = round((cutter.bottom - point.y) / m + point.x)
                if cutter.left <= x <= cutter.right:
                    result.append(Point(x, cutter.bottom))
                    continue

        # Рассматриваемый отрезок мог быть полностью невидимым
        if result:
            self.draw_segment(Segment(result[0], result[1]), result=True)

    def cut(self) -> None:
        if self._cutter is None:
            QMessageBox.critical(self, "Ошибка", "Необходимо установить отсекатель")
            return

        for segment in self._segments:
            self.handle_segment(segment)

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
        if abs(pos.x - self._cutter.right) <= self._accuracy:
            pos.x = self._cutter.right
        elif abs(pos.x - self._cutter.left) <= self._accuracy:
            pos.x = self._cutter.left

        if abs(pos.y - self._cutter.top) <= self._accuracy:
            pos.y = self._cutter.top
        elif abs(pos.y - self._cutter.bottom) <= self._accuracy:
            pos.y = self._cutter.bottom

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        position = Point(ev.pos().x(), ev.pos().y() - 10)

        if ev.buttons() == Qt.LeftButton:
            if self._cutter is not None and self._modes.get() == Mode.SEGMENTS:
                self.cutter_is_nearly(position)

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

    def draw_segment(self, segment: Segment, result: bool = False) -> None:
        qp = QPainter(self.img)
        if result:
            width = 2
            color = self._result_colors.get().toQColor()
        else:
            width = 1
            color = self._segment_colors.get().toQColor()

        qp.setPen(QPen(color, width))
        # Algorithms.dda(qp, segment.p1, segment.p2)
        qp.drawLine(segment.to_qline())
        qp.end()
        self.update_pixmap()

    def draw_cutter(self, cutter: Cutter) -> None:
        qp = QPainter(self.img)
        qp.setPen(QPen(self._cutter_colors.get().toQColor(), 1))
        for segment in cutter.get_lines():
            qp.drawLine(segment.to_qline())
        qp.end()
        self.update_pixmap()

    def redraw_segments(self) -> None:
        qp = QPainter(self.img)
        qp.setPen(QPen(self._segment_colors.get().toQColor(), 1))
        for segment in self._segments:
            qp.drawLine(segment.to_qline())
        qp.end()
        self.update_pixmap()
