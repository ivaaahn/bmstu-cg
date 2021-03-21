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
        # self.lines_table = LinesTable()
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

        logger.debug(f"_add_line_handler({alg, color, coords})")
        if coords is not None:
            self.data.add_line(alg, color, coords)
            self.lines_table.add(alg, color, coords)

        logger.debug(f"Data.lines = {self.data.lines}")
        


    
    # def draw(self):
    #     self.astroid.change_draw()
    #     self.change_btn_state()
    #     self.repaint()


    def bindButtons(self):
        self.clear_btn.clicked.connect(self.clear)
        self.segment_btn.clicked.connect(self._add_line_handler)

    # Чо-как сделать это...
    def clear(self):
        pass

    # def reset(self):
    #     self.astroid.reset()
    #     self.back_btn.setEnabled(True)
    #     self.set_center()
    #     self.repaint()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Вы уверены?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

   
    def _draw_line(self, qp: QPainter) -> typing.NoReturn:
        pass


    def _draw_grid(self, qp: QPainter):
        qp.setPen(QPen(Qt.green, 1))

        coef = self.canvas.coef

        for x in range(self.x0, self.x_max, coef):
            qp.drawLine(x, self.y_min, x, self.y_max)

        for x in range(self.x0 - coef, self.x_min, -coef):
            qp.drawLine(x, self.y_min, x, self.y_max)

        for y in range(self.y0, self.y_max, coef):
            qp.drawLine(self.x_min, y, self.x_max, y)

        for y in range(self.y0 - coef, self.y_min, -coef):
            qp.drawLine(self.x_min, y, self.x_max, y)


    def _draw_axis(self, qp: QPainter) -> typing.NoReturn:
        qp.setPen(QPen(Qt.black, 3))
        # Отрисовка самих осей
        qp.drawLine(self.x0, self.y_min, self.x0, self.y_max)
        qp.drawLine(self.x_min, self.y0, self.x_max, self.y0)

        # Отрисовка стрелок
        qp.drawLine(self.x_max-12, self.y0-7, self.x_max, self.y0)
        qp.drawLine(self.x_max-12, self.y0+7, self.x_max, self.y0)
        qp.drawLine(self.x0, self.y_min, self.x0-7, self.y_min+12)
        qp.drawLine(self.x0, self.y_min, self.x0+7, self.y_min+12)


        font = qp.font()
        font.setPointSize(14)
        coef = self.canvas.coef

        qp.setFont(font)
        qp.setPen(QPen(Qt.black))
        qp.drawText(self.x0 - 15, self.y0 + 20, '0')

        offset_yp, offset_ym = 30, 25
        offset_x = 20

        # Отрисовка чисел
        k = -1
        for y in range(self.y0 + coef, self.y_max, coef):
            qp.drawText(self.x0 - offset_yp, y + 7, str(k))
            k -= 1

        k = 1
        for y in range(self.y0 - coef, self.y_min, -coef):
            qp.drawText(self.x0 - offset_ym, y + 7, str(k))
            k += 1

        k = 1
        for x in range(self.x0 + coef, self.x_max, coef):
            qp.drawText(x - 5, self.y0 + offset_x, str(k))
            k += 1

        k = -1
        for x in range(self.x0 - coef, self.x_min, -coef):
            qp.drawText(x - 10, self.y0 + offset_x, str(k))
            k -= 1

    # def _draw_astroid(self, qp: QPainter):
    #     qp.setPen(QPen(Qt.red, 3))
    #     for point in self.astroid.values:
    #         point = self.canvas.toCanv(point)
    #         qp.drawPoint(point.x, point.y)

    #     border_points = self.astroid.border_points
    #     if len(border_points):
    #         tl, tr, bl, br = list(
    #             map(lambda x: self.canvas.toCanv(x).to_qpoint(), border_points))
    #         qp.drawLine(tl, tr)
    #         qp.drawLine(bl, br)
    #         qp.drawLine(tl, bl)
    #         qp.drawLine(tr, br)


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
        qp.drawPixmap(QRect(self.x_min, self.y_min, self.x_max,
                            self.y_max), self.canvas.surf)

        self._draw_grid(qp)
        self._draw_axis(qp)
        self._draw_line(qp)



    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
    #         self.draw()
    #     if event.key() == Qt.Key_Plus:
    #         self.canvas.increase()
    #     elif event.key() == Qt.Key_Minus:
    #         self.canvas.decrease()
