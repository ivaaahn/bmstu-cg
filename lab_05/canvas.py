from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage, QColor
from PyQt5.QtWidgets import QLabel

from algorithms import Algorithms
from properties.color import Color
from models.figure import Figure
from properties.mode import Mode
from models.point import Point
from utils import delay


class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.w, self.h = 771, 663
        self.img = self._new_image()
        self._update_pixmap()
        self.figure = Figure()

    def clear(self) -> None:
        self.figure.clear()
        self.img = self._new_image()
        self._update_pixmap()

    def mousePressEvent(self, event):
        position = Point(event.pos().x(), event.pos().y())
        if event.buttons() == Qt.LeftButton:
            self.add_point_controller(position)
        elif event.buttons() == Qt.RightButton:
            self.close_poly_controller()

    def fill(self, figure_color: Color, mode: Mode):
        self.mode = mode
        self.figure.color = figure_color
        self.img = self._new_image()
        self.handle_outline()

        p_min, p_max = self.figure.p_min, self.figure.p_max
        mark_color = self.figure.get_mark_color().toQcolor()
        bg_color = Color.BG.toQcolor()
        figure_color = figure_color.toQcolor()
        curr_color = bg_color

        def change_color(c) -> QColor:
            return bg_color if (c == figure_color) else figure_color

        for y in range(p_max.y, p_min.y - 1, -1):
            for x in range(p_min.x, p_max.x + 1, 1):
                if self.img.pixelColor(x, y) == mark_color:
                    curr_color = change_color(curr_color)

                self.img.setPixelColor(x, y, curr_color)

            if self.mode is Mode.DELAY:
                delay()
                self._update_pixmap()

        self._update_pixmap()

    def handle_outline(self) -> None:
        polygons = self.figure.all_polygons

        for poly in polygons:
            vertices, length = poly.all_vertices, len(poly.all_vertices)
            extrema = poly.all_extrema

            for i in range(length):
                print(i, (i + 1) % length)
                self._handle_segment(vertices[i], vertices[(i + 1) % length],
                                     [i in extrema, (i + 1) % length in extrema])

    def _handle_segment(self, p0: Point, p1: Point, is_extremum) -> None:
        if p0.y == p1.y:
            return

        if p0.y > p1.y:
            p0, p1 = p1, p0
            is_extremum.reverse()

        dy, dx = 1, (p1.x - p0.x) / (p1.y - p0.y)

        curr_p = Point(p0.x, p0.y)
        mark_color = self.figure.get_mark_color().toQcolor()
        while curr_p.y < p1.y:
            if self.img.pixelColor(int(curr_p.x + 0.5), int(curr_p.y)) != mark_color:
                self.img.setPixelColor(int(curr_p.x + 0.5), int(curr_p.y), mark_color)
            else:
                self.img.setPixelColor(int(curr_p.x + 0.5), int(curr_p.y), Color.BG.toQcolor())

            if self.mode is Mode.DELAY:
                delay()
                self._update_pixmap()

            curr_p.x += dx
            curr_p.y += dy

    def _new_image(self) -> QImage:
        img = QImage(self.w, self.h, QImage.Format_ARGB32_Premultiplied)
        img.fill(Qt.white)
        return img

    def _update_pixmap(self):
        self.pixmap = QPixmap().fromImage(self.img)
        self.setPixmap(self.pixmap)

    def add_point_controller(self, pos: Point) -> None:
        self.figure.add_vertex(pos)

        qp = QPainter(self.img)
        qp.setPen(QPen(Qt.blue, 4))
        qp.drawEllipse(pos.to_qpoint(), 2, 2)

        last_poly = self.figure.last_polygon
        if last_poly.size() > 1:
            Algorithms.dda(self.img, last_poly.pre_last_vrtx, last_poly.last_vrtx)

        qp.end()
        self.pixmap = QPixmap().fromImage(self.img)
        self.setPixmap(self.pixmap)

    def close_poly_controller(self) -> None:
        qp = QPainter(self.img)
        qp.setPen(QPen(Qt.black, 1))
        last_poly = self.figure.last_polygon
        Algorithms.dda(self.img, last_poly.first_vrtx, last_poly.last_vrtx)
        qp.end()

        self.figure.close_this_polygon()
        self._update_pixmap()
