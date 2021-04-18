from typing import List
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen

from ellipse import Ellipse
from spectrum import Spectrum


class Drawer:
    def __init__(self, qp: QPainter) -> None:
        self.qp = qp
        self.qp.setPen(QPen(Qt.black, 1))

    def _draw_ellipse(self, ellipse: Ellipse) -> None:
        points = ellipse.points
        self.qp.setPen(ellipse.color.toQcolor())

        if points is None:
            self.qp.drawEllipse(ellipse.center.to_qpointf(),
                                ellipse.rx, ellipse.ry)
        else:
            for point in points:
                self.qp.drawPoint(point.x, point.y)

    def _draw_spectrum(self, spectrum: Spectrum) -> None:
        for ellipse in spectrum.ellipses:
            self._draw_ellipse(ellipse)

    def draw_ellipses(self, ellipses: List[Ellipse]) -> None:
        for ellipse in ellipses:
            self._draw_ellipse(ellipse)

    def draw_spectrums(self, spectrums: List[Spectrum]) -> None:
        for spectrum in spectrums:
            self._draw_spectrum(spectrum)
