from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox as QMB

from controller import Controller
from design.main_window_ui import Ui_MainWindow
from models.point import Point
from models.segment import Segment


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.controller = Controller(self.canvas, self.mode_list.get(), self.cutter_color_list.get(),
                                     self.default_segment_color_list.get(), self.result_segment_color_list.get())
        self.bind_buttons()
        self.canvas.canvas_clicked.connect(self.controller.click_handler)

    def read_segment(self) -> Segment:
        return Segment(Point(self.x1_box.value(), self.y1_box.value()), Point(self.x2_box.value(), self.y2_box.value()))

    def read_cutter_point(self) -> Point:
        return Point(self.x_cutter_box.value(), self.y_cutter_box.value())

    def clean_btn_handler(self) -> None:
        self.controller.clear_all()

    def add_segment_btn_handler(self) -> None:
        self.controller.add_segment(self.read_segment())

    def add_cutter_point_btn_handler(self) -> None:
        self.controller.add_cutter_point(self.read_cutter_point())

    def cut_btn_handler(self) -> None:
        self.controller.cut()

    def mode_changed(self) -> None:
        self.controller.mouse_mode = self.mode_list.get()

    def cutter_color_changed(self) -> None:
        self.controller.cutter_color = self.cutter_color_list.get()

    def segment_color_changed(self) -> None:
        self.controller.segment_color = self.default_segment_color_list.get()

    def result_color_changed(self) -> None:
        self.controller.result_color = self.result_segment_color_list.get()

    def bind_buttons(self) -> None:
        self.mode_list.currentIndexChanged.connect(self.mode_changed)
        self.cutter_color_list.currentIndexChanged.connect(self.cutter_color_changed)
        self.default_segment_color_list.currentIndexChanged.connect(self.segment_color_changed)
        self.result_segment_color_list.currentIndexChanged.connect(self.result_color_changed)

        self.close_cutter_btn.clicked.connect(self.controller.close_cutter)

        self.clear_btn.clicked.connect(self.clean_btn_handler)
        self.add_segment_btn.clicked.connect(self.add_segment_btn_handler)

        self.add_cutter_point_btn.clicked.connect(self.add_cutter_point_btn_handler)
        self.cut_btn.clicked.connect(self.cut_btn_handler)

        # self.canvas.mousePressEvent.connect(self.controller.click)

    def closeEvent(self, event):
        reply = QMB.question(self, 'Message', "Вы уверены?",
                             QMB.Yes | QMB.No, QMB.Yes)
        if reply == QMB.Yes:
            event.accept()
        else:
            event.ignore()

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
    #         self._fill_controller()
