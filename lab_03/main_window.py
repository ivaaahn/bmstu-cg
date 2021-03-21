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
from data import Action, Data, Action
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

    def _read_coords(self) -> Tuple[Point] or None:
        try:
            x_start, y_start = float(self.x_start_input.text()), float(self.y_start_input.text())
            x_end, y_end = float(self.x_end_input.text()), float(self.y_end_input.text())
        except ValueError:
            err = ErrorInput("Введите вещественное число")
            if err.clickedButton() is QMessageBox.Cancel:
                return None
        else:
            return (Point(x_start, y_start), Point(x_end, y_end))

    def _read_color(self) -> Color:
        return Color(self.color_list.currentRow())

    def _read_alg(self) -> Algorithm:
        return Algorithm(self.alg_list.currentRow())

    def _add_line_handler(self) -> NoReturn:
        color: Color = self._read_color()
        alg: Algorithm = self._read_alg()
        coords: typing.Tuple[Point] = self._read_coords()
        line_id: int = self.data._get_id()

        logger.debug(f"_add_line_handler({alg, color, coords})")
        if coords is not None:
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


    def bindButtons(self):
        self.add_btn.clicked.connect(self._add_line_handler)
        self.remove_btn.clicked.connect(self._remove_line_handler)
        self.remove_all_btn.clicked.connect(self._remove_all_lines_handler)


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
            qp.drawLine(line.p_start.x, line.p_start.y, line.p_end.x, line.p_end.y)
        else:
            for point in line.points:
                qp.drawPoint(point.x, point.y)


    def _draw_lines(self, qp: QPainter) -> NoReturn:
        for _, line in self.data.lines.items():
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

        self._draw_lines(qp)



    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
    #         self.draw()
    #     if event.key() == Qt.Key_Plus:
    #         self.canvas.increase()
    #     elif event.key() == Qt.Key_Minus:
    #         self.canvas.decrease()
