from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QImage, QPainter, QColor

import utils
from models.point import Point
from properties.color import Color


class Algorithms:
    @staticmethod
    def dda(qp: QPainter, p_begin: Point, p_end: Point):
        if p_begin == p_end:
            qp.drawPoint(p_begin.to_qpoint())
            return

        length = int(max(abs(p_end.x - p_begin.x), abs(p_end.y - p_begin.y)))
        dx = (p_end.x - p_begin.x) / length
        dy = (p_end.y - p_begin.y) / length

        curr_x, curr_y = p_begin.x, p_begin.y
        tmp_x, tmp_y = curr_x, curr_y

        for _ in range(1, length + 2):
            qp.drawPoint(tmp_x, tmp_y)

            curr_x += dx
            curr_y += dy

            rx, ry = utils.custom_round(curr_x), utils.custom_round(curr_y)
            tmp_x, tmp_y = rx, ry
