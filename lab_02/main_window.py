from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap
from design.main_window import Ui_MainWindow
from point import Point
from astroid import Astroid
from errors import ErrorInput
from popups import BChangePopup
from loguru import logger
from math import radians
from typing import NamedTuple

import typing


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.astroid = Astroid()
        self.bindButtons()
        self.task_popup = None
        self.b_value.setText(str(self.astroid.b))

    def resizeEvent(self, event):
        self.canvas.init_sizes = False
        self.repaint()

    # @logger.catch
    def move(self):
        def _get_data(self) -> typing.NamedTuple or None:
            class MoveData(NamedTuple):
                dx: float = None
                dy: float = None

                def __repr__(self) -> str:
                    return f'dx: {self.dx} dy: {self.dy}'

            try:
                data = MoveData(float(self.dx_input.text()),
                                float(self.dy_input.text()))
            except ValueError:
                err = ErrorInput("Введите вещественное число")
                if err.clickedButton() is QMessageBox.Cancel:
                    return None
            else:
                return data

        move_data = _get_data(self)
        if move_data:
            self.back_btn.setEnabled(True)
            self.astroid.move(move_data)
            self.center_info_value.setText(str(self.astroid.center))
            self.repaint()

    def scale(self) -> typing.NoReturn:
        def _get_data(self) -> typing.NamedTuple or None:
            class ScaleData(NamedTuple):
                center: Point = None
                x_coef: float = None
                y_coef: float = None

                def __repr__(self) -> str:
                    return f'center: {self.center}, x_coef: {self.x_coef}, y_coef: {self.y_coef}'

            try:
                xc, yc = float(self.xc_scale_input.text()), float(
                    self.yc_scale_input.text())
                x_coef = float(self.x_coef_input.text())
                y_coef = float(self.y_coef_input.text())
            except ValueError:
                err = ErrorInput("Введите вещественное число")
                if err.clickedButton() is QMessageBox.Cancel:
                    return None
            else:
                data = ScaleData(Point(point=(xc, yc)), x_coef, y_coef)
                return data

        scale_data = _get_data(self)
        if scale_data:
            self.back_btn.setEnabled(True)
            self.astroid.scale(scale_data)
            self.center_info_value.setText(str(self.astroid.center))
            self.repaint()

    def rotate(self):
        def _get_data(self) -> typing.NamedTuple or None:
            class RotateData(NamedTuple):
                center: Point = None
                angle: float = None

                def __repr__(self) -> str:
                    return f'center: {self.center}, angle: {self.angle}'

            try:
                xc, yc = float(self.xc_rotate_input.text()), float(
                    self.yc_rotate_input.text())
                angle = radians(float(self.angle_input.text()))
            except ValueError:
                err = ErrorInput("Введите вещественное число")
                if err.clickedButton() is QMessageBox.Cancel:
                    return None
            else:
                data = RotateData(Point(point=(xc, yc)), angle)
                return data

        rotate_data = _get_data(self)
        if rotate_data:
            self.back_btn.setEnabled(True)
            self.astroid.rotate(rotate_data)
            self.center_info_value.setText(str(self.astroid.center))
            self.repaint()

    def b_change(self):
        self.b_change_popup = BChangePopup(
            self.astroid, self.b_value, self.repaint)
        self.b_change_popup.show()

    def change_btn_state(self):
        val = self.astroid._need_draw
        self.move_btn.setEnabled(val)
        self.scale_btn.setEnabled(val)
        self.rotate_btn.setEnabled(val)
        self.reset_btn.setEnabled(val)

    def draw(self):
        self.astroid.change_draw()
        self.change_btn_state()
        self.repaint()

    def set_center(self):
        self.best_scale_btn.clicked.connect(self.scaleAnswer)

    def bindButtons(self):
        self.best_scale_btn.clicked.connect(self.scaleAnswer)
        self.bchange_btn.clicked.connect(self.b_change)

        self.draw_btn.clicked.connect(self.draw)
        self.dec_btn.clicked.connect(self.canvas.decrease)
        self.inc_btn.clicked.connect(self.canvas.increase)

        self.move_btn.clicked.connect(self.move)
        self.move_btn.setEnabled(False)

        self.scale_btn.clicked.connect(self.scale)
        self.scale_btn.setEnabled(False)

        self.rotate_btn.clicked.connect(self.rotate)
        self.rotate_btn.setEnabled(False)

        self.back_btn.clicked.connect(self.back)
        self.back_btn.setEnabled(False)

        self.reset_btn.clicked.connect(self.reset)
        self.reset_btn.setEnabled(False)

    def back(self):
        self.astroid.back()
        self.back_btn.setEnabled(False)
        self.set_center()
        self.repaint()

    def reset(self):
        self.astroid.reset()
        self.back_btn.setEnabled(True)
        self.set_center()
        self.repaint()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Вы уверены?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def scaleAnswer(self):
        self.canvas.scaleUp(self.astroid)

    def _drawGrid(self, qp: QPainter):
        pen = QPen(Qt.green, 1)
        qp.setPen(pen)

        coef = self.canvas.coef
        step = self.canvas.step

        for x in range(self.x0, self.x_max, coef * step):
            qp.drawLine(x, self.y_min, x, self.y_max)

        for x in range(self.x0 - coef * step, self.x_min, -coef * step):
            qp.drawLine(x, self.y_min, x, self.y_max)

        for y in range(self.y0, self.y_max, coef * step):
            qp.drawLine(self.x_min, y, self.x_max, y)

        for y in range(self.y0 - coef * step, self.y_min, -coef * step):
            qp.drawLine(self.x_min, y, self.x_max, y)

    def _drawAxis(self, qp):
        penAx = QPen(Qt.black, 3)
        pen_l = QPen(Qt.black)
        font = qp.font()
        font.setPointSize(14)
        qp.setFont(font)
        qp.setPen(penAx)

        step = self.canvas.step
        coef = self.canvas.coef

        qp.drawText(self.x0 - 15, self.y0 + 20, '0')

        if self.canvas.dx < -self.canvas.width() // 2:
            qp.setPen(penAx)
            qp.drawLine(self.x_min, self.y_min, self.x_min, self.y_max)
            qp.setPen(pen_l)

            k = -step
            for y in range(self.y0 + coef * step, self.y_max, step * coef):
                qp.drawText(self.x_min + 20, y + 7, str(k))
                k -= step

            k = step
            for y in range(self.y0 - coef * step, self.y_min, -step * coef):
                qp.drawText(self.x_min + 20, y + 7, str(k))
                k += step

        elif self.canvas.dx > self.canvas.width() // 2:
            qp.setPen(penAx)
            qp.drawLine(self.x_max, self.y_min, self.x_max, self.y_max)
            qp.setPen(pen_l)

            k = -step
            for y in range(self.y0 + coef * step, self.y_max, step * coef):
                qp.drawText(self.x_max-30, y+7, str(k))
                k -= step

            k = step
            for y in range(self.y0 - coef * step, self.y_min, -step * coef):
                qp.drawText(self.x_max-25, y+7, str(k))
                k += step

        else:
            qp.setPen(penAx)
            qp.drawLine(self.x0, self.y_min, self.x0, self.y_max)
            qp.drawLine(self.x0, self.y_min, self.x0-7, self.y_min+12)
            qp.drawLine(self.x0, self.y_min, self.x0+7, self.y_min+12)
            qp.setPen(pen_l)

            if self.canvas.coef <= 4:
                offset_p, offset_m = 40, 35
            else:
                offset_p, offset_m = 30, 25

            k = -step
            for y in range(self.y0 + coef * step, self.y_max, step * coef):
                qp.drawText(self.x0 - offset_p, y + 7, str(k))
                k -= step

            k = step
            for y in range(self.y0 - coef * step, self.y_min, -step * coef):
                qp.drawText(self.x0 - offset_m, y + 7, str(k))
                k += step

        if self.canvas.dy > self.canvas.height() // 2:
            qp.setPen(penAx)
            qp.drawLine(self.x_min, self.y_max, self.x_max, self.y_max)
            qp.setPen(pen_l)

            k = step
            for x in range(self.x0 + coef * step, self.x_max, step * coef):
                qp.drawText(x - 5, self.y_max - 15, str(k))
                k += step

            k = -step
            for x in range(self.x0 - coef * step, self.x_min, -step * coef):
                qp.drawText(x - 10, self.y_max - 15, str(k))
                k -= step

        elif self.canvas.dy < -self.canvas.height() // 2:
            qp.setPen(penAx)
            qp.drawLine(self.x_min, self.y_min, self.x_max, self.y_min)
            qp.setPen(pen_l)

            k = step
            for x in range(self.x0 + coef * step, self.x_max, step * coef):
                qp.drawText(x - 5, self.y_min + 15, str(k))
                k += step

            k = -step
            for x in range(self.x0 - coef * step, self.x_min, -step * coef):
                qp.drawText(x - 10, self.y_min + 15, str(k))
                k -= step

        else:
            qp.setPen(penAx)
            qp.drawLine(self.x_min, self.y0, self.x_max, self.y0)
            qp.drawLine(self.x_max - 12, self.y0 - 7, self.x_max, self.y0)
            qp.drawLine(self.x_max - 12, self.y0 + 7, self.x_max, self.y0)
            qp.setPen(pen_l)

            k = step
            for x in range(self.x0 + coef * step, self.x_max, step * coef):
                qp.drawText(x - 5, self.y0 + 20, str(k))
                k += step

            k = -step
            for x in range(self.x0 - coef * step, self.x_min, -step * coef):
                qp.drawText(x - 10, self.y0 + 20, str(k))
                k -= step

    def _draw_astroid(self, qp: QPainter):
        qp.setPen(QPen(Qt.red, 3))
        for point in self.astroid.values:
            point = self.canvas.toCanv(point)
            qp.drawPoint(point.x, point.y)

        border_points = self.astroid.border_points
        if len(border_points):
            tl, tr, bl, br = list(
                map(lambda x: self.canvas.toCanv(x).to_qpoint(), border_points))
            qp.drawLine(tl, tr)
            qp.drawLine(bl, br)
            qp.drawLine(tl, bl)
            qp.drawLine(tr, br)

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
        self._drawGrid(qp)
        self._drawAxis(qp)
        self._draw_astroid(qp)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.draw()
        if event.key() == Qt.Key_Plus:
            self.canvas.increase()
        elif event.key() == Qt.Key_Minus:
            self.canvas.decrease()
