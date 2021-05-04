from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication as QGuiApp
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage, QColor
from PyQt5.QtWidgets import QLabel, QMessageBox

import utils
from algorithms import Algorithms
from models.figure import Figure
from models.point import Point
from properties.color import Color, ColorListBorder
from properties.mode import Mode


class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.img = self._new_image()
        self._update_pixmap()
        self._figure = Figure()

    # TODO это ужасно, и надо сделать иначе
    def init_border_color_list(self, color_list: ColorListBorder):
        self.border_color_list = color_list

    @property
    def figure(self) -> Figure:
        return self._figure

    def clear(self) -> None:
        self.figure.clear()
        self.img = self._new_image()
        self._update_pixmap()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        position = Point(ev.pos().x(), ev.pos().y())
        if ev.buttons() == Qt.LeftButton:
            if QGuiApp.keyboardModifiers() & Qt.ControlModifier:
                self.add_seed_pixel_controller(Point(ev.pos().x(), ev.pos().y()))
            else:
                exactly = QGuiApp.keyboardModifiers() & Qt.ShiftModifier
                self.add_point_controller(position, exactly=exactly)
        elif ev.buttons() == Qt.RightButton:
            self.close_poly_controller()

    def init_stack(self):
        if self.figure.seed_pixel is None:
            QMessageBox.critical(self, "Ошибка", "Необходимо установить затравочный пиксел!")
            return
        return [self.figure.seed_pixel]

    def border_fill(self) -> None:
        """Ограничивает полотно, чтобы заливка не выходила за границы"""
        Algorithms.dda(self.img, self.border_color_list.get(), Point(0, 0), Point(0, utils.H - 1))
        Algorithms.dda(self.img, self.border_color_list.get(), Point(0, 0), Point(utils.W - 1, 0))
        Algorithms.dda(self.img, self.border_color_list.get(), Point(0, utils.H - 1), Point(utils.W - 1, utils.H - 1))
        Algorithms.dda(self.img, self.border_color_list.get(), Point(utils.W - 1, 0), Point(utils.W - 1, utils.H - 1))

    def fill(self, fill_color: Color, mode: Mode) -> None:
        # stack = []
        if not self.figure.seed_pixels:
            QMessageBox.critical(self, "Ошибка", "Необходимо установить затравочный пиксел!")
            return
        # else:
            # stack += self.figure.seed_pixels

        self.border_fill()

        self.mode = mode
        self.figure.color = fill_color

        fill_color = fill_color.toQColor()
        border_color = self.border_color_list.get().toQColor()

        def cmp_pix(pixel: Point, color: QColor) -> bool:
            return self.img.pixelColor(pixel.to_qpoint()) == color

        def set_pix(pixel: Point, color: QColor) -> None:
            self.img.setPixelColor(pixel.to_qpoint(), color)

        while self.figure.seed_pixels:
            p_curr = self.figure.seed_pixels.pop()
            set_pix(p_curr, fill_color)
            tmp_x = p_curr.x

            p_curr.x += 1
            while not cmp_pix(p_curr, border_color):
                set_pix(p_curr, fill_color)
                p_curr.x += 1

            rx = p_curr.x - 1
            p_curr.x = tmp_x

            p_curr.x -= 1
            while not cmp_pix(p_curr, border_color):
                set_pix(p_curr, fill_color)
                p_curr.x -= 1

            lx = p_curr.x + 1
            p_curr.x = tmp_x

            tmp_y = p_curr.y
            for i in (1, -1):
                p_curr.x = lx
                p_curr.y = tmp_y + i

                while p_curr.x <= rx:
                    flag = False
                    while not cmp_pix(p_curr, border_color) and not cmp_pix(p_curr, fill_color) and p_curr.x < rx:
                        p_curr.x += 1
                        flag = True

                    if flag:
                        x, y = p_curr.x, p_curr.y
                        if p_curr.x != rx or cmp_pix(p_curr, border_color) or cmp_pix(p_curr, fill_color):
                            x -= 1
                        self.figure.seed_pixels.append(Point(x, y))

                    x_input = p_curr.x
                    while (cmp_pix(p_curr, border_color) or cmp_pix(p_curr, fill_color)) and p_curr.x < rx:
                        p_curr.x += 1

                    if p_curr.x == x_input:
                        p_curr.x += 1

            if self.mode is Mode.DELAY:
                utils.delay()
                self._update_pixmap()

        self._update_pixmap()

    @staticmethod
    def _new_image() -> QImage:
        img = QImage(utils.W, utils.H, QImage.Format_ARGB32_Premultiplied)
        img.fill(Qt.white)
        return img

    def _update_pixmap(self):
        self.pixmap = QPixmap().fromImage(self.img)
        self.setPixmap(self.pixmap)

    def add_seed_pixel_controller(self, pos: Point) -> None:
        self.figure.add_seed_pixel(pos)
        # qp = QPainter(self.img)
        # qp.setPen(QPen(Qt.green, 5))
        # qp.drawPoint(pos.to_qpoint())
        # qp.end()
        # self._update_pixmap()

    def add_point_controller(self, pos: Point, exactly: bool = False) -> None:
        if exactly and self.figure.last_polygon.size():
            last_vertex = self.figure.last_polygon.last_vrtx
            dx, dy = abs(pos.x - last_vertex.x), abs(pos.y - last_vertex.y)

            if dx < dy:
                pos.x = last_vertex.x
            else:
                pos.y = last_vertex.y

        self.figure.add_vertex(pos)

        qp = QPainter(self.img)
        qp.setPen(QPen(Qt.gray, 4))
        qp.drawEllipse(pos.to_qpoint(), 2, 2)

        last_poly = self.figure.last_polygon
        if last_poly.size() > 1:
            Algorithms.dda(self.img, self.border_color_list.get(), last_poly.pre_last_vrtx, last_poly.last_vrtx)

        qp.end()
        self._update_pixmap()

    def close_poly_controller(self) -> None:
        last_poly = self.figure.last_polygon
        if last_poly.size() < 3:
            return

        qp = QPainter(self.img)
        qp.setPen(QPen(Qt.black, 1))
        Algorithms.dda(self.img, self.border_color_list.get(), last_poly.first_vrtx, last_poly.last_vrtx)
        qp.end()

        self.figure.close_this_polygon()
        self._update_pixmap()
