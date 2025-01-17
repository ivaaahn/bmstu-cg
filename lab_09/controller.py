from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication as QGuiApp
from PyQt5.QtWidgets import QMessageBox

from canvas import Canvas
from exceptions import NonConvex, UnableToClose, DegenerateCutter, SelfIntersection, PolygonError
from models.cutter import Cutter
from models.point import Point
from models.polygon import Polygon as Polygon
from properties.color import Color
from properties.mode import Mode


class Controller:
    def __init__(self, canvas: Canvas, mode: Mode, cutter_color: Color, segment_color: Color, res_color: Color) -> None:
        self._canvas = canvas

        self._mouse_mode = mode
        self._cutter_color = cutter_color
        self._poly_color = segment_color
        self._result_color = res_color

        self._poly = Polygon()
        self._cutter = Cutter()

    def clear_all(self) -> None:
        self._canvas.clear()
        self._poly.reset()
        self._cutter.reset()

    def redraw_cutter(self) -> None:
        self._canvas.clear()
        self._canvas.draw_segments(self._cutter.edges, self.cutter_color)

    def redraw_poly(self) -> None:
        self._canvas.clear()
        self._canvas.draw_segments(self._poly.edges, self._poly_color)

    def reset_cutter(self) -> None:
        self._cutter.reset()
        self.redraw_poly()

    def reset_poly(self) -> None:
        self._poly.reset()
        self.redraw_cutter()

    def add_cutter_vertex(self, v: Point) -> None:
        if self._cutter.is_closed():
            self.reset_cutter()

        try:
            edge = self.cutter.add_vertex(v, QGuiApp.keyboardModifiers() & Qt.ShiftModifier)
        except NonConvex as e:
            QMessageBox.critical(self._canvas, "Ошибка", e.message)
            self.reset_cutter()
            return
        except PolygonError as e:
            QMessageBox.critical(self._canvas, "Ошибка", e.message)
            return

        if edge is not None:
            self._canvas.draw_segments([edge], self._cutter_color)

    def add_poly_vertex(self, v: Point) -> None:
        if self._poly.is_closed():
            self.reset_poly()

        if self.cutter.is_closed():
            if v.dist_to(closest_vertex := self.cutter.get_closest_vertex(v)) <= 10:
                v = closest_vertex
            elif v.dist_to(closest_proj := self.cutter.get_closest_project(v)) <= 10:
                v = closest_proj

        try:
            edge = self._poly.add_vertex(v, QGuiApp.keyboardModifiers() & Qt.ShiftModifier)
        except SelfIntersection as e:
            QMessageBox.critical(self._canvas, "Ошибка", e.message)
            return

        if edge is not None:
            self._canvas.draw_segments([edge], self._poly_color)

    def close_cutter(self) -> None:
        if self._cutter.is_closed():
            QMessageBox.information(self._canvas, "Внимание", "Отсекатель уже замкнут")
            return
        try:
            edge = self.cutter.close()
        except (NonConvex, DegenerateCutter) as e:
            QMessageBox.critical(self._canvas, "Ошибка", e.message)
            self.reset_cutter()
            return
        except PolygonError as e:
            QMessageBox.critical(self._canvas, "Ошибка", e.message)
            return

        self._canvas.draw_segments([edge], self._cutter_color)

    def close_poly(self) -> None:
        if self._poly.is_closed():
            QMessageBox.information(self._canvas, "Внимание", "Многоугольник уже замкнут")
            return

        try:
            edge = self._poly.close()
        except UnableToClose as e:
            QMessageBox.critical(self._canvas, "Ошибка", e.message)
            return
        except PolygonError as e:
            QMessageBox.critical(self._canvas, "Ошибка", e.message)
            return

        self._canvas.draw_segments([edge], self._poly_color)

    def click_handler(self, pos: Point, buttons: Qt.MouseButtons) -> None:
        if buttons == Qt.LeftButton:
            if self.mouse_mode is Mode.CUTTER:
                self.add_cutter_vertex(pos)
            else:
                self.add_poly_vertex(pos)

        elif buttons == Qt.RightButton:
            if self.mouse_mode is Mode.CUTTER:
                self.close_cutter()
            else:
                self.close_poly()

        else:
            if self.mouse_mode is Mode.CUTTER:
                self.reset_cutter()
            else:
                self.reset_poly()

    def cut(self) -> None:
        if not self._cutter.is_closed():
            QMessageBox.critical(self._canvas, "Ошибка", "Для отсечения необходимо задать отсекатель")
            return

        if not self._poly.is_closed():
            QMessageBox.critical(self._canvas, "Ошибка", "Необходимо задать многоугольник для отсечения")
            return

        if (result_poly := self.cutter.cut_poly(self._poly)) is not None:
            self.draw_result(result_poly)

    def draw_result(self, result_poly) -> None:
        self._canvas.draw_segments(result_poly.edges, self._result_color, is_result=True)

    @property
    def mouse_mode(self) -> Mode:
        return self._mouse_mode

    @property
    def cutter_color(self) -> Color:
        return self._cutter_color

    @property
    def segment_color(self) -> Color:
        return self._poly_color

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
        if self.mouse_mode is Mode.CUTTER and not self.cutter.is_closed():
            self.reset_cutter()
        elif self._mouse_mode is Mode.POLY and not self._poly.is_closed():
            self.reset_poly()

        self._mouse_mode = new_mode

    @cutter_color.setter
    def cutter_color(self, new_color: Color) -> None:
        self._cutter_color = new_color

    @segment_color.setter
    def segment_color(self, new_color: Color) -> None:
        self._poly_color = new_color

    @result_color.setter
    def result_color(self, new_color: Color) -> None:
        self._result_color = new_color
