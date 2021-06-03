from typing import List, Optional

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication as QGuiApp
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtWidgets import QLabel, QMessageBox

import utils
from models.cutter import Cutter
from models.point import Point
from models.segment import Segment
from properties.color import ColorListCutter, ColorListSegment, ColorListResult
from properties.mode import Mode, ModeList

ACCURACY = 15

INTO = 0b000
LEFT = 0b0001
RIGHT = 0b0010
BOTTOM = 0b0100
TOP = 0b1000


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

    def handle_vertical_segment(self, point: Point) -> Point:
        if point.y > self._cutter.top:
            return Point(point.x, self._cutter.top)
        elif point.y < self._cutter.bottom:
            return Point(point.x, self._cutter.bottom)
        else:
            return Point(point.x, point.y)

    def handle_segment(self, seg: Segment):
        cutter = self._cutter
        self.set_bits(seg)

        # Полностью видимый
        if seg.start.code == 0 and seg.end.code == 0:
            self.draw_segment(seg, result=True)
            return

        # Полностью невидимый
        if seg.start.code & seg.end.code != 0:
            return

        # Либо обе точки вне отсекателя, либо одна вне, а одна внутри.
        # Если одна из точек лежит внутри, то отрезок пересекает только одну границу отсекателя.

        FIRST = 0
        SECOND = 1
        points: List[Point] = seg.points
        result: List[Point] = []

        curr_index = 1
        if points[FIRST].code == 0:
            result.append(points[FIRST])
        elif points[SECOND].code == 0:
            result.append(points[SECOND])
            points.reverse()
        else:
            curr_index = 0

        while curr_index <= SECOND:

            # Вертикальный отрезок обрабатываем отдельно
            if points[FIRST].x == points[SECOND].x:
                result.append(self.handle_vertical_segment(points[curr_index]))
                curr_index += 1
                continue

            m: float = (points[SECOND].y - points[FIRST].y) / (points[SECOND].x - points[FIRST].x)

            # Если текущая точка лежит слева от отсекателя
            if points[curr_index].code & LEFT:
                y = round(m * (cutter.left - points[curr_index].x) + points[curr_index].y)

                if cutter.bottom <= y <= cutter.top:
                    result.append(Point(cutter.left, y))
                    curr_index += 1
                    continue

            elif points[curr_index].code & RIGHT:
                y = round(m * (cutter.right - points[curr_index].x) + points[curr_index].y)

                if cutter.bottom <= y <= cutter.top:
                    result.append(Point(cutter.right, y))
                    curr_index += 1
                    continue

            # Перед обработкой пересечений с верхней и нижней границей проверяем, что прямая не горизонтальная
            # поскольку в этом случае мы ничего не найдем
            if m == 0:
                curr_index += 1
                continue

            if points[curr_index].code & TOP:
                x = round((cutter.top - points[curr_index].y) / m + points[curr_index].x)

                if cutter.left <= x <= cutter.right:
                    result.append(Point(x, cutter.top))
                    curr_index += 1
                    continue

            if points[curr_index].code & BOTTOM:
                x = round((cutter.bottom - points[curr_index].y) / m + points[curr_index].x)

                if cutter.left <= x <= cutter.right:
                    result.append(Point(x, cutter.bottom))
                    curr_index += 1
                    continue

            curr_index += 1

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
        if abs(pos.x - self._cutter.right) <= ACCURACY:
            pos.x = self._cutter.right
        elif abs(pos.x - self._cutter.left) <= ACCURACY:
            pos.x = self._cutter.left

        if abs(pos.y - self._cutter.top) <= ACCURACY:
            pos.y = self._cutter.top
        elif abs(pos.y - self._cutter.bottom) <= ACCURACY:
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
