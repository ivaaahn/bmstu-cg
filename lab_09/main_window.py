from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox as QMB

from controller import Controller
from qt.design import Ui_MainWindow
from models.point import Point
from models.segment import Segment


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.controller = Controller(self.canvas, self.mode_list.get(), self.cutter_color_list.get(),
                                     self.poly_color_list.get(), self.result_color_list.get())
        self.bind_buttons()
        self.canvas.canvas_clicked.connect(self.controller.click_handler)

    def read_point(self) -> Point:
        return Point(self.x_box.value(), self.y_box.value())

    def add_cutter_btn_handler(self) -> None:
        self.controller.add_cutter_vertex(self.read_point())

    def close_cutter_btn_handler(self) -> None:
        self.controller.close_cutter()

    def add_poly_btn_handler(self) -> None:
        self.controller.add_poly_vertex(self.read_point())

    def close_poly_btn_handler(self) -> None:
        self.controller.close_poly()

    def cut_btn_handler(self) -> None:
        self.controller.cut()

    def clear_btn_handler(self) -> None:
        self.controller.clear_all()

    def mode_changed(self) -> None:
        self.controller.mouse_mode = self.mode_list.get()

    def cutter_color_changed(self) -> None:
        self.controller.cutter_color = self.cutter_color_list.get()

    def segment_color_changed(self) -> None:
        self.controller.segment_color = self.rect_color_list.get()

    def result_color_changed(self) -> None:
        self.controller.result_color = self.result_color_list.get()

    def bind_buttons(self) -> None:
        self.mode_list.currentIndexChanged.connect(self.mode_changed)
        self.cutter_color_list.currentIndexChanged.connect(self.cutter_color_changed)
        self.poly_color_list.currentIndexChanged.connect(self.segment_color_changed)
        self.result_color_list.currentIndexChanged.connect(self.result_color_changed)

        self.cut_btn.clicked.connect(self.cut_btn_handler)
        self.clear_btn.clicked.connect(self.clear_btn_handler)

    def closeEvent(self, event):
        reply = QMB.question(self, 'Message', "Вы уверены?",
                             QMB.Yes | QMB.No, QMB.Yes)
        if reply == QMB.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.cut_btn_handler()
