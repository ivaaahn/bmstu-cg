from timeit import timeit
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox as QMB

from design.main_window_ui import Ui_MainWindow
from models.point import Point
from plotter import BarPlotter
from properties.mode import Mode
from testing import TimeTesting


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.bind_buttons()
        self.canvas.init_border_color_list(self.color_list_border)

    def _read_point_coords(self) -> Point:
        return Point(self.x_input.value(), self.y_input.value())

    def _read_seed_pixel_coords(self) -> Point:
        return Point(self.x_seed_input.value(), self.y_seed_input.value())

    def _cleanup_controller(self) -> None:
        self.canvas.clear()

    def time_info_controller(self, result: Optional[float]) -> None:
        if result is not None:
            text = f'Время закраски: {round(result, 2)} мс'
        else:
            text = f'Время закраски: None'

        self.time_info_lbl.setText(text)

    def _fill_controller(self) -> None:
        fill_color, mode = self.color_list_fill.get(), self.mode_list.get()
        result = None
        if mode is Mode.NO_DELAY:
            result = timeit(lambda: self.canvas.fill(fill_color, mode), number=1) * 1000
        else:
            self.canvas.fill(fill_color, mode)

        self.time_info_controller(result)

    def bind_buttons(self) -> None:
        self.set_seed_pixel_btn.clicked.connect(
            lambda: self.canvas.add_seed_pixel_controller(self._read_seed_pixel_coords()))
        self.add_point_btn.clicked.connect(lambda: self.canvas.add_point_controller(self._read_point_coords()))
        self.close_figure_btn.clicked.connect(self.canvas.close_poly_controller)
        self.fill_btn.clicked.connect(self._fill_controller)
        self.clear_btn.clicked.connect(self._cleanup_controller)

    def closeEvent(self, event):
        reply = QMB.question(self, 'Message', "Вы уверены?",
                             QMB.Yes | QMB.No, QMB.Yes)
        if reply == QMB.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self._fill_controller()
