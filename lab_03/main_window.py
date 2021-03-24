from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter
from typing import Tuple

from design.main_window_ui import Ui_MainWindow
from algorithms import AlgType, AlgsTesting
from plotter import BarPlotter, GraphPlotter
from errors import ErrorInput
from drawer import Drawer
from point import Point
from color import Color
from data import Data


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bind_buttons()

        self.data = Data()
        self.algs_testing = AlgsTesting()

    def resizeEvent(self, event) -> None:
        self.canvas.init_sizes = False
        self.repaint()

    def _read_spectrum(self) -> tuple or None:
        def _round(num: float) -> int:
            return int(num + (0.5 if num >= 0 else -0.5))

        try:
            start_angle = float(self.start_angle_input.text())
            end_angle = float(self.end_angle_input.text())
            step = float(self.step_input.text())
            length: int = _round(float(self.len_input.text()))
        except ValueError:
            return None
        else:
            return step, length, start_angle, end_angle

    def _read_coords(self) -> Tuple[Point] or None:
        def _round(num: float) -> int:
            return int(num + 0.5 if num >= 0 else -0.5)

        try:
            x_start: int = _round(float(self.x_start_input.text()))
            y_start: int = _round(float(self.y_start_input.text()))
            x_end: int = _round(float(self.x_end_input.text()))
            y_end: int = _round(float(self.y_end_input.text()))
        except ValueError:
            return None
        else:
            return (Point(x_start, y_start), Point(x_end, y_end))

    def _read_color(self) -> Color:
        return Color(self.color_list.currentRow())

    def _read_alg(self) -> AlgType:
        return AlgType(self.alg_list.currentRow())

    def _add_spectrum_handler(self) -> None:
        color: Color = self._read_color()
        alg: AlgType = self._read_alg()
        spectrum_data: tuple = self._read_spectrum()

        if spectrum_data is None:
            ErrorInput("Числа должны быть вещественными!")
        elif spectrum_data[0] <= 0:
            ErrorInput("Шаг должен быть положительным!")
        elif spectrum_data[1] < 0:
            ErrorInput("Длина должна быть неотрицательной!")
        elif spectrum_data[2] > spectrum_data[3]:
            ErrorInput("Начало спектра не должно превышать конец спектра!")
        else:
            step, length, start_angle, end_angle = spectrum_data
            center_point = self.canvas.center_point

            self.data.add_spectrum(
                center_point, step, length, (start_angle, end_angle), alg, color)
            self.repaint()

    def _add_line_handler(self) -> None:
        color: Color = self._read_color()
        alg: AlgType = self._read_alg()
        coords: Tuple[Point] = self._read_coords()
        line_id: int = self.data._get_id()

        if coords is None:
            ErrorInput("Введите вещественное число")
        else:
            self.data.add_line(alg, color, coords, line_id)
            self.lines_table.add(alg, color, coords, line_id)

        self.repaint()

    def _remove_line_handler(self) -> None:
        line_id = self.lines_table.read_id()
        if line_id is not None:
            self.data.remove_line(line_id)
            self.lines_table.rm_current_line()
            self.repaint()

    def _remove_all_lines_handler(self) -> None:
        self.data.remove_all_lines()
        self.lines_table.remove_all()
        self.repaint()

    def _remove_all_spectrums(self) -> None:
        self.data.remove_spectrums()
        self.repaint()

    def _time_test_handler(self) -> None:
        data: dict = self.algs_testing.time_test()
        BarPlotter(data)

    def _stairs_test_handler(self) -> None:
        all_angles, res = self.algs_testing.stairs_test()
        GraphPlotter(all_angles, res)

    def bind_buttons(self) -> None:
        self.add_btn.clicked.connect(self._add_line_handler)
        self.remove_btn.clicked.connect(self._remove_line_handler)
        self.remove_all_btn.clicked.connect(self._remove_all_lines_handler)

        self.build_spectrum_btn.clicked.connect(self._add_spectrum_handler)
        self.clear_spectrum_btn.clicked.connect(self._remove_all_spectrums)
        self.time_btn.clicked.connect(self._time_test_handler)
        self.stairs_btn.clicked.connect(self._stairs_test_handler)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Вы уверены?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def paintEvent(self, event):
        if not self.canvas.init_sizes:
            self.canvas.calc_sizes()
            self.canvas.init_sizes = True


        qp = QPainter(self)
        qp.drawPixmap(QRect(self.canvas.x_min, self.canvas.y_min, self.canvas.x_max,
                            self.canvas.y_max), self.canvas.surf)
        drawer = Drawer(qp)

        drawer.draw_segments(self.data.lines_without_labels)
        drawer.draw_spectrums(self.data.spectrums)
