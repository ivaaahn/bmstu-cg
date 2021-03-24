from typing import List
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from line import Line

class Drawer:
    def __init__(self, qp: QPainter) -> None:
        self.qp = qp
        self.qp.setPen(QPen(Qt.black, 1))


    def _draw_line(self, line: Line) -> None:
        color = line.color.to_qt()
        all_points = line.points
        if all_points is None:
            self.qp.setPen(color)
            self.qp.drawLine(line.p_start.x, line.p_start.y, line.p_end.x, line.p_end.y)
        else:
            for point in all_points:
                color.setAlpha(point.intensity)
                self.qp.setPen(color)
                self.qp.drawPoint(point.x, point.y)


    def draw_segments(self, segments: List[Line]) -> None:
        for segment in segments:
            self._draw_line(segment)

    def draw_spectrums(self, spectrums: List[List]) -> None:
        for spectrum in spectrums:
            for line in spectrum:
                self._draw_line(line)