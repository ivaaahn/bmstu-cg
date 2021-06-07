from typing import List, Optional

from PyQt5.QtCore import Qt

from PyQt5.QtGui import QGuiApplication as QGuiApp
from PyQt5.QtWidgets import QMessageBox

from canvas import Canvas
from models.cutter import Cutter
from models.point import Point
from models.segment import Segment
from properties.color import Color
from properties.mode import Mode


class Controller:
    def __init__(self, canvas: Canvas, mode: Mode, cutter_color: Color, segment_color: Color, res_color: Color):
        self._canvas = canvas

        self._mouse_mode = mode
        self._cutter_color = cutter_color
        self._segment_color = segment_color
        self._result_color = res_color

        self._segments: List[Segment] = []
        self._cutter = Cutter()

        self._fst_click: Optional[Point] = None

    def cut(self) -> None:
        print("def cut(self) -> None:")

    def clear_all(self) -> None:
        self._canvas.clear()
        self.cutter = Cutter()
        self._fst_click = None
        self._segments.clear()

    def add_segment(self, seg: Segment) -> None:
        self._segments.append(seg)
        self._canvas.draw_segments([seg], self._segment_color, is_result=False)

    def _add_segment_point(self, p: Point) -> None:
        if self._fst_click is not None:
            straight = QGuiApp.keyboardModifiers() & Qt.ShiftModifier
            along = QGuiApp.keyboardModifiers() & Qt.ControlModifier

            segment = Segment.build(self._fst_click, p, straight=straight, along=along)
            self.add_segment(segment)
            self._fst_click = None
        else:
            self._fst_click = p

    def _add_cutter_edge(self, p1: Point, p2: Point):
        edge = Segment(p1, p2)
        self.cutter.add_edge(edge)
        self._canvas.draw_segments([edge], self.cutter_color)

    def reset_cutter(self) -> None:
        self._cutter = Cutter()
        self._canvas.clear()
        self._canvas.draw_segments(self._segments, self._segment_color)
        self._fst_click = None

    def add_cutter_point(self, p: Point) -> None:
        if self._cutter.is_closed():
            self.reset_cutter()

        if self._fst_click is not None:
            try:
                self._add_cutter_edge(self._fst_click, p)
            except:
                QMessageBox.critical(self._canvas, "Ошибка", "Невыпуклый отсекатель")
                self.reset_cutter()
                return

        self._fst_click = p

    def close_cutter(self) -> None:
        if self.cutter.ready_to_close():
            try:
                closing_edge = self.cutter.close()
            except:
                QMessageBox.critical(self._canvas, "Ошибка", "Невыпуклый отсекатель")
                self.reset_cutter()
                return
            self._canvas.draw_segments([closing_edge], self._cutter_color)

    def click_handler(self, pos: Point, buttons: Qt.MouseButtons):
        if buttons == Qt.LeftButton:

            if self.mouse_mode is Mode.CUTTER:
                self.add_cutter_point(pos)

            else:
                self._add_segment_point(pos)

        elif buttons == Qt.RightButton:
            if self.mouse_mode is Mode.CUTTER:
                self.close_cutter()

            self._fst_click = None

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
    def cutter(self, value: Cutter):
        self._cutter = value

    @mouse_mode.setter
    def mouse_mode(self, new_mode: Mode) -> None:
        self._mouse_mode = new_mode

    @cutter_color.setter
    def cutter_color(self, new_color: Color) -> None:
        self._cutter_color = new_color

    @segment_color.setter
    def segment_color(self, new_color: Color) -> None:
        self._segment_color = new_color

    @result_color.setter
    def result_color(self, new_color: Color) -> None:
        self._result_color = new_color
