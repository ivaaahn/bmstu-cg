from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox as QMB
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter
from typing import Tuple, NamedTuple
from collections import namedtuple

from design.main_window_ui import Ui_MainWindow
from algorithms import AlgsTesting
from plotter import BarPlotter, GraphPlotter
from errors import ErrorInput
from drawer import Drawer
from point import Point
from color import Color
from figure import Figure
from data import Data
from ellipse import Ellipse
from spectrum import Spectrum
from way import Way


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.bind_buttons()

        self.data = Data()
        self.algs_testing = AlgsTesting()

    def resizeEvent(self, event) -> None:
        self.canvas.init_sizes = False
        self.repaint()

    def _read_figure(self) -> Figure:
        return Figure(self.figure_list.currentIndex())

    def _read_color(self) -> Color:
        return Color(self.color_list.currentIndex())

    def _read_way(self) -> Way:
        return Way(self.way_list.currentIndex())

    def _read_center_coords(self) -> Point:
        return Point(self.x_c_input.value(), self.y_c_input.value())

    def _read_r(self) -> int:
        return self.r_input.value()

    def _read_rx(self) -> int:
        return self.a_input.value()

    def _read_ry(self) -> int:
        return self.b_input.value()

    def _read_r_start(self) -> int:
        return self.r_start_input.value()

    def _read_rx_start(self) -> int:
        return self.rx_start_input.value()

    def _read_ry_start(self) -> int:
        return self.ry_start_input.value()

    def _read_step(self) -> int:
        return self.step_input.value()

    def _read_count(self) -> int:
        return self.count_input.value()

    def _read_common_params(self) -> NamedTuple:
        class CommonParams(NamedTuple):
            ftype: Figure = self._read_figure()
            way: Way = self._read_way()
            color: Color = self._read_color()
            center: Point = self._read_center_coords()
        return CommonParams()

    def _draw_spectrum_handler(self) -> None:
        cp = self._read_common_params()
        step: int = self._read_step()
        count: int = self._read_count()

        if cp.ftype is Figure.CIRCLE:
            r_start: int = self._read_r()
            rx_start, ry_start = r_start, r_start
        else:
            rx_start: int = self._read_rx_start()
            ry_start: int = self._read_ry_start()

        self.data.add_spectrum(Spectrum(
            cp.ftype, cp.way, cp.color, cp.center, rx_start, ry_start, step, count))
        self.repaint()

    def _draw_figure_handler(self) -> None:
        cp = self._read_common_params()

        if cp.ftype is Figure.CIRCLE:
            r: int = self._read_r()
            rx, ry = r, r
        else:
            rx: int = self._read_rx()
            ry: int = self._read_ry()

        self.data.add_ellipse(Ellipse(cp.center, rx, ry, cp.way, cp.color))
        self.repaint()

    def _clear_handler(self) -> None:
        self.data.clear_all()
        self.repaint()

    def _time_test_handler(self) -> None:
        data: dict = self.algs_testing.time_test()
        BarPlotter(data)

    def _stairs_test_handler(self) -> None:
        all_angles, res = self.algs_testing.stairs_test()
        GraphPlotter(all_angles, res)

    def bind_buttons(self) -> None:
        self.draw_figure_btn.clicked.connect(self._draw_figure_handler)
        self.draw_spectrum_btn.clicked.connect(self._draw_spectrum_handler)
        self.clear_btn.clicked.connect(self._clear_handler)
        self.figure_list.currentIndexChanged.connect(self._fig_changed)
        self._fig_changed(None)

    def closeEvent(self, event):
        reply = QMB.question(self, 'Message', "Вы уверены?",
                             QMB.Yes | QMB.No, QMB.Yes)
        if reply == QMB.Yes:
            event.accept()
        else:
            event.ignore()

    def _fig_changed(self, ix) -> None:
        if self._read_figure() is Figure.ELLIPSE:
            self.r_input.setDisabled(True)
            self.r_start_input.setDisabled(True)

            self.rx_input.setDisabled(False)
            self.ry_input.setDisabled(False)
            self.rx_start_input.setDisabled(False)
            self.ry_start_input.setDisabled(False)
        else:
            self.r_input.setDisabled(False)
            self.r_start_input.setDisabled(False)
            self.rx_input.setDisabled(True)
            self.ry_input.setDisabled(True)
            self.rx_start_input.setDisabled(True)
            self.ry_start_input.setDisabled(True)

    def paintEvent(self, event):
        if not self.canvas.init_sizes:
            self.canvas.calc_sizes()
            self.canvas.init_sizes = True

        qp: QPainter = QPainter(self)
        qp.drawPixmap(QRect(self.canvas.x_min, self.canvas.y_min, self.canvas.x_max,
                            self.canvas.y_max), self.canvas.surf)
        drawer = Drawer(qp)
        drawer.draw_ellipses(self.data.ellipses)
        drawer.draw_spectrums(self.data.spectrums)
