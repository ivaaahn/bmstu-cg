from PyQt5.QtGui import QImage, QColor

import utils
from models.point import Point
from properties.color import Color


class Algorithms:
    @staticmethod
    def dda(img: QImage, p_begin: Point, p_end: Point, qt_color: QColor):
        if p_begin == p_end:
            img.setPixelColor(p_begin.to_qpoint(), qt_color)
            return

        length = int(max(abs(p_end.x - p_begin.x), abs(p_end.y - p_begin.y)))
        dx = (p_end.x - p_begin.x) / length
        dy = (p_end.y - p_begin.y) / length

        curr_x, curr_y = p_begin.x, p_begin.y
        tmp_x, tmp_y = curr_x, curr_y

        for _ in range(1, length + 2):
            img.setPixelColor(tmp_x, tmp_y, qt_color)

            curr_x += dx
            curr_y += dy

            rx, ry = utils.round(curr_x), utils.round(curr_y)
            tmp_x, tmp_y = rx, ry
