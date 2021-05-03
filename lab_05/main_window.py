from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox as QMB

# from algorithms import AlgTester
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

    def _read_point_coords(self) -> Point:
        return Point(self.x_input.value(), self.y_input.value())

    def _cleanup_controller(self) -> None:
        self.canvas.clear()

    def _timing_test_controller(self) -> None:
        result = TimeTesting(self.canvas.figure, self.canvas.fill).start()
        BarPlotter(result)
        self.canvas.fill(self.color_list.get(), Mode.NO_DELAY)

    def _fill_controller(self) -> None:
        self.canvas.fill(self.color_list.get(), self.mode_list.get())

    def bind_buttons(self) -> None:
        self.add_point_btn.clicked.connect(lambda: self.canvas.add_point_controller(self._read_point_coords()))
        self.close_figure_btn.clicked.connect(self.canvas.close_poly_controller)
        self.fill_btn.clicked.connect(self._fill_controller)
        self.clear_btn.clicked.connect(self._cleanup_controller)
        self.time_measure_btn.clicked.connect(self._timing_test_controller)

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
