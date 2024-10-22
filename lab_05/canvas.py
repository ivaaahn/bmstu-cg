from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication as QGuiApp
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage, QColor
from PyQt5.QtWidgets import QLabel

import utils
from algorithms import Algorithms
from models.figure import Figure
from models.point import Point
from points_table import PointsTable
from properties.color import Color, ColorListBorder, ColorList
from properties.mode import Mode

class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.img = self._new_image()
        self._update_pixmap()
        self._figure = Figure()

    def init_other(self, ptable: PointsTable, bcolor_list: ColorListBorder):
        self.ptable = ptable
        self.bcolor_list = bcolor_list

    @property
    def figure(self) -> Figure:
        return self._figure

    def clear(self) -> None:
        self.figure.clear()
        self.img = self._new_image()
        self._update_pixmap()

    def mousePressEvent(self, event):
        position = Point(event.pos().x(), event.pos().y())
        if event.buttons() == Qt.LeftButton:
            exactly = QGuiApp.keyboardModifiers() & Qt.ShiftModifier
            self.add_point_controller(position, exactly=exactly)
        elif event.buttons() == Qt.RightButton:
            self.close_poly_controller()

    def fill(self, figure_color: Color, mode: Mode):
        self.mode = mode
        self.figure.color = figure_color
        self.img = self._new_image()
        self.handle_outline()

        p_min, p_max = self.figure.p_min, self.figure.p_max
        mark_color = Color.FLAG.toQcolor()
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
                utils.delay()
                self._update_pixmap()

        self._redraw_borders_and_points()
        self._update_pixmap()

    def handle_outline(self) -> None:
        polygons = self.figure.all_polygons

        for poly in polygons:
            vertices, length = poly.all_vertices, len(poly.all_vertices)
            extrema = poly.all_extrema

            for i in range(length):
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
        mark_color = Color.FLAG.toQcolor()

        while curr_p.y < p1.y:
            if self.img.pixelColor(int(curr_p.x + 0.5), int(curr_p.y)) != mark_color:
                self.img.setPixelColor(int(curr_p.x + 0.5), int(curr_p.y), mark_color)
            else:
                self.img.setPixelColor(int(curr_p.x + 0.5), int(curr_p.y), Color.BG.toQcolor())

            if self.mode is Mode.DELAY:
                utils.delay()
                self._update_pixmap()

            curr_p.x += dx
            curr_p.y += dy

        # if self.mode is Mode.DELAY:
        #     utils.delay()
        #     self._update_pixmap()

    def _new_image(self) -> QImage:
        img = QImage(utils.W, utils.H, QImage.Format_ARGB32_Premultiplied)
        img.fill(Qt.white)
        return img

    def _update_pixmap(self):
        self.pixmap = QPixmap().fromImage(self.img)
        self.setPixmap(self.pixmap)

    def add_point_controller(self, pos: Point, exactly: bool = False) -> None:
        pos.set_title()

        if exactly and self.figure.last_polygon.size():
            last_vertex = self.figure.last_polygon.last_vrtx
            dx, dy = abs(pos.x - last_vertex.x), abs(pos.y - last_vertex.y)

            if dx < dy:
                pos.x = last_vertex.x
            else:
                pos.y = last_vertex.y

        self.figure.add_vertex(pos)
        self.ptable.add(pos)

        qp = QPainter(self.img)
        qp.setPen(QPen(Color.POINT.toQcolor(), 4))
        qp.drawEllipse(pos.to_qpoint(), 2, 2)
        qp.drawText(pos.x - 10, pos.y - 10, pos.title)

        last_poly = self.figure.last_polygon
        edge_color = self.bcolor_list.get().toQcolor()
        if last_poly.size() > 1:
            Algorithms.dda(self.img, last_poly.pre_last_vrtx, last_poly.last_vrtx, edge_color)

        qp.end()
        self._update_pixmap()

    def _redraw_borders_and_points(self) -> None:
        qp = QPainter(self.img)
        qp.setPen(QPen(Color.POINT.toQcolor(), 4))
        edge_color = self.bcolor_list.get().toQcolor()

        for poly in self.figure.all_polygons:
            vert = poly.all_vertices
            for i in range(len(vert) - 1):
                Algorithms.dda(self.img, vert[i], vert[i + 1], edge_color)
                qp.drawEllipse(vert[i].to_qpoint(), 2, 2)
                qp.drawText(vert[i].x - 10, vert[i].y - 10, vert[i].title)
        qp.end()

    def close_poly_controller(self) -> None:
        last_poly = self.figure.last_polygon
        if last_poly.size() < 3:
            return

        qp = QPainter(self.img)
        qp.setPen(QPen(Qt.black, 1))
        self.figure.close_this_polygon()
        edge_color = self.bcolor_list.get().toQcolor()
        Algorithms.dda(self.img, last_poly.pre_last_vrtx, last_poly.last_vrtx, edge_color)
        qp.end()

        self._update_pixmap()
