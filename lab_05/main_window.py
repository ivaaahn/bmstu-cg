from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox as QMB

# from algorithms import AlgTester
from design.main_window_ui import Ui_MainWindow
from models.point import Point


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        # self._alg_tester = AlgTester()
        self.bind_buttons()

    def _read_point_coords(self) -> Point:
        return Point(self.x_input.value(), self.y_input.value())

    def _cleanup_controller(self) -> None:
        self.canvas.clear()

    def _timing_test_controller(self) -> None:
        pass

    def _fill_controller(self) -> None:
        self.canvas.fill(self.color_list.get(), self.mode_list.get())

    def bind_buttons(self) -> None:
        self.add_point_btn.clicked.connect(lambda: self.canvas.add_point_controller(self._read_point_coords()))
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
