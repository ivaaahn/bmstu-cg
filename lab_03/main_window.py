from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap

from loguru import logger
from math import radians
from typing import NamedTuple, NoReturn, List, Tuple
import typing

from design.main_window_ui import Ui_MainWindow
from popups import BChangePopup, TaskPopup
from errors import ErrorInput
from point import Point

from line import Line, Algorithm, Color
from data import Data
from lines_table import LinesTable


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = Data()
        self.bindButtons()

    def resizeEvent(self, event) -> NoReturn:
        self.canvas.init_sizes = False
        self.repaint()

    def _read_spectrum(self) -> tuple or None:
        def _round(num: float) -> int:
            return int(num + 0.5 if num >= 0 else -0.5)

        try:
            step = float(self.step_input.text()) % 360.0
            length = _round(float(self.len_input.text()))
        except ValueError:
            return None
        else:
            return step, length

    def _read_coords(self) -> Tuple[Point] or None:
        def _round(num: float) -> int:
            return int(num + 0.5 if num >= 0 else -0.5)

        try:
            x_start = _round(float(self.x_start_input.text()))
            y_start = _round(float(self.y_start_input.text()))
            x_end = _round(float(self.x_end_input.text()))
            y_end = _round(float(self.y_end_input.text()))

        except ValueError:
            return None
        else:
            return (Point(x_start, y_start), Point(x_end, y_end))

    def _read_color(self) -> Color:
        return Color(self.color_list.currentRow())

    def _read_alg(self) -> Algorithm:
        return Algorithm(self.alg_list.currentRow())

    def _add_spectrum_handler(self) -> NoReturn:
        color: Color = self._read_color()
        alg: Algorithm = self._read_alg()
        spectrum = self._read_spectrum()

        if spectrum is None:
            ErrorInput("Введите вещественное число")
        elif spectrum[1] < 1:
            ErrorInput("Длина должна быть неотрицательной")
        elif spectrum[0] == 0:
            ErrorInput("Шаг не может быть равен нулю")
        else:
            step, length = spectrum
            center_point = Point(self.canvas.xc, self.canvas.yc)

            self.data.add_spectrum(center_point, step, length, alg, color)
            self.repaint()


    def _add_line_handler(self) -> NoReturn:
        color: Color = self._read_color()
        alg: Algorithm = self._read_alg()
        coords: typing.Tuple[Point] = self._read_coords()
        line_id: int = self.data._get_id()

        logger.debug(f"_add_line_handler({alg, color, coords})")

        if coords is None:
            ErrorInput("Введите вещественное число")
        elif coords[0] == coords[1]:
            ErrorInput("Начало и конец отрезка не должны совпадать!")
        else:
            self.data.add_line(alg, color, coords, line_id)
            self.lines_table.add(alg, color, coords, line_id)

        logger.debug(f"Data.lines = {self.data.lines}")
        self.repaint()

    def _remove_line_handler(self) -> NoReturn:
        line_id = self.lines_table.read_id()
        logger.debug(f"line_id = {line_id}")
        if line_id is not None:
            self.data.remove_line(line_id)
            self.lines_table.remove()
            self.repaint()

    def _remove_all_lines_handler(self) -> NoReturn:
        self.data.remove_all_lines()
        self.lines_table.remove_all()
        self.repaint()

    def _remove_all_spectrums(self) -> NoReturn:
        self.data.remove_spectrums()
        self.repaint()

    def bindButtons(self):
        self.add_btn.clicked.connect(self._add_line_handler)
        self.remove_btn.clicked.connect(self._remove_line_handler)
        self.remove_all_btn.clicked.connect(self._remove_all_lines_handler)

        self.build_spectrum_btn.clicked.connect(self._add_spectrum_handler)
        self.clear_spectrum_btn.clicked.connect(self._remove_all_spectrums)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Вы уверены?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def _draw_line(self, line: Line, qp: QPainter) -> NoReturn:
        all_points = line.points
        if all_points is None:
            qp.drawLine(line.p_start.x, line.p_start.y,
                        line.p_end.x, line.p_end.y)
        else:
            for point in line.points:
                qp.drawPoint(point.x, point.y)

    def _getPen(self, color: Color) -> QPen:
        interp = {
            Color.BACK: QPen(Qt.white),
            Color.RED: QPen(Qt.red),
            Color.BLUE: QPen(Qt.blue),
            Color.BLACK: QPen(Qt.black)
        }
        return interp[color]

    def _draw_segments(self, qp: QPainter) -> NoReturn:
        for _, line in self.data.lines.items():
            qp.setPen(self._getPen(line.color))
            self._draw_line(line, qp)

    def _draw_spectrums(self, qp: QPainter) -> NoReturn:
        logger.info(f"spectrums: {self.data.spectrums}")

        for spectrum in self.data.spectrums:
            qp.setPen(self._getPen(spectrum[0].color))
            for line in spectrum:
                self._draw_line(line, qp)

    def paintEvent(self, event):
        if not self.canvas.init_sizes:
            self.canvas.calc_sizes()
            self.canvas.init_sizes = True

            self.x_min = self.canvas.x_min
            self.x_max = self.canvas.x_max

            self.y_min = self.canvas.y_min
            self.y_max = self.canvas.y_max

            self.x0 = self.canvas.x0
            self.y0 = self.canvas.y0

        qp = QPainter(self)

        pen = QPen(Qt.red, 1)
        qp.setPen(pen)

        qp.drawPixmap(QRect(self.x_min, self.y_min, self.x_max,
                            self.y_max), self.canvas.surf)

        self._draw_segments(qp)
        self._draw_spectrums(qp)

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
    #         self.draw()
    #     if event.key() == Qt.Key_Plus:
    #         self.canvas.increase()
    #     elif event.key() == Qt.Key_Minus:
    #         self.canvas.decrease()
