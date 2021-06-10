from typing import List, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication as QGuiApp
from PyQt5.QtWidgets import QMessageBox

from canvas import Canvas
from exceptions import NonConvex, UnableToClose, DegenerateCutter, SelfIntersection
from models.cutter import Cutter
from models.point import Point
from models.segment import Segment
from models.vector import Vector
from properties.color import Color
from properties.mode import Mode


class Controller:
    def __init__(self, canvas: Canvas, mode: Mode, cutter_color: Color, segment_color: Color, res_color: Color) -> None:
        self._canvas = canvas

        self._mouse_mode = mode
        self._cutter_color = cutter_color
        self._segment_color = segment_color
        self._result_color = res_color

        self._segments: List[Segment] = []
        self._cutter = Cutter()

        self._fst_click: Optional[Point] = None

    def clear_all(self) -> None:
        self._canvas.clear()
        self._cutter.reset()
        self._segments.clear()
        self.first_click_reset()

    def add_segment(self, seg: Segment) -> None:
        self._segments.append(seg)
        self._canvas.draw_segments([seg], self._segment_color)

    def along_handler(self, segment: Segment) -> Segment:
        tangents = self.cutter.tangents

        m = segment.tangent

        if m is None and m in tangents:
            return segment
        elif m is None:
            best = max(tangents)
        else:
            diff = [(abs(t - m), t) for t in tangents if t is not None]
            choice = min(diff)
            best = choice[1]

        new_y = best * (segment.p2.x - segment.p1.x) + segment.p1.y

        if best:
            new_x = (segment.p2.y - segment.p1.y) / best + segment.p1.x
        else:
            new_x = segment.p1.x

        if abs(new_x - segment.p2.x) < abs(new_y - segment.p2.y):
            segment.p2.x = new_x
        else:
            segment.p2.y = new_y

        return segment

    def _add_segment_point(self, v: Point) -> None:
        if self.cutter.is_closed():
            if v.dist_to(closest_vertex := self.cutter.get_closest_vertex(v)) <= 10:
                v = closest_vertex
            elif v.dist_to(closest_proj := self.cutter.get_closest_project(v)) <= 10:
                v = closest_proj

        if not self.first_click_was():
            self.first_click = v
        else:
            straight = QGuiApp.keyboardModifiers() & Qt.ShiftModifier
            along = QGuiApp.keyboardModifiers() & Qt.ControlModifier

            segment = Segment.build(self.first_click, v, straight)

            if self.cutter.is_closed() and along:
                self.along_handler(segment)

            self.add_segment(segment)
            self.first_click_reset()

    def add_cutter_vertex(self, v: Point) -> None:
        if self._cutter.is_closed():
            self.reset_cutter()

        if self.cutter.vertices and self.cutter.vertices[-1] == v:
            QMessageBox.critical(self._canvas, "Ошибка", "Необходимо ввести отрезок")
            return

        try:
            edge = self.cutter.add_vertex(v, QGuiApp.keyboardModifiers() & Qt.ShiftModifier)
        except NonConvex as e:
            QMessageBox.critical(self._canvas, "Ошибка", e.message)
            self.reset_cutter()
            return
        except SelfIntersection as e:
            QMessageBox.critical(self._canvas, "Ошибка", e.message)
            return

        if edge is not None:
            self._canvas.draw_segments([edge], self._cutter_color)

    def reset_cutter(self) -> None:
        self._cutter.reset()
        self._canvas.clear()
        self._canvas.draw_segments(self._segments, self._segment_color)
        self.first_click_reset()

    def close_cutter(self) -> None:
        try:
            closing_edge = self.cutter.close()
        except (NonConvex, DegenerateCutter) as e:
            QMessageBox.critical(self._canvas, "Ошибка", e.message)
            self.reset_cutter()
            return
        except UnableToClose as e:
            QMessageBox.critical(self._canvas, "Ошибка", e.message)
            return
        except SelfIntersection as e:
            QMessageBox.critical(self._canvas, "Ошибка", e.message)
            return

        self._canvas.draw_segments([closing_edge], self._cutter_color)

    def click_handler(self, pos: Point, buttons: Qt.MouseButtons) -> None:
        if buttons == Qt.LeftButton:
            if self.mouse_mode is Mode.CUTTER:
                self.add_cutter_vertex(pos)
            else:
                self._add_segment_point(pos)
        elif buttons == Qt.RightButton:
            if self.mouse_mode is Mode.CUTTER:
                self.close_cutter()
            else:
                self.first_click_reset()
        elif self.mouse_mode is Mode.CUTTER:
            self.reset_cutter()

    def cut(self) -> None:
        if not self._cutter.is_closed():
            QMessageBox.critical(self._canvas, "Ошибка", "Для отсечения необходимо задать отсекатель")
            return

        for segment in self._segments:
            result = self.cutter.cut(segment)

            if result is not None:
                self._canvas.draw_segments([result], self.result_color, is_result=True)

    @property
    def mouse_mode(self) -> Mode:
        return self._mouse_mode

    @property
    def cutter_color(self) -> Color:
        return self._cutter_color

    @property
    def segment_color(self) -> Color:
        return self._segment_color

    @property
    def result_color(self) -> Color:
        return self._result_color

    @property
    def cutter(self) -> Cutter:
        return self._cutter

    @cutter.setter
    def cutter(self, value: Cutter) -> None:
        self._cutter = value

    @mouse_mode.setter
    def mouse_mode(self, new_mode: Mode) -> None:
        self._mouse_mode = new_mode
        self.first_click_reset()

    @cutter_color.setter
    def cutter_color(self, new_color: Color) -> None:
        self._cutter_color = new_color

    @segment_color.setter
    def segment_color(self, new_color: Color) -> None:
        self._segment_color = new_color

    @result_color.setter
    def result_color(self, new_color: Color) -> None:
        self._result_color = new_color

    def first_click_was(self) -> bool:
        return self._fst_click is not None

    def first_click_reset(self) -> None:
        self._fst_click = None

    @property
    def first_click(self) -> Optional[Point]:
        return self._fst_click

    @first_click.setter
    def first_click(self, pos: Point) -> None:
        self._fst_click = pos
