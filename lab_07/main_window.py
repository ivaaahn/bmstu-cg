from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox as QMB

from design.main_window_ui import Ui_MainWindow
from models.cutter import Cutter
from models.point import Point
from models.segment import Segment


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.bind_buttons()

        self.canvas.set_objects(self.mode_list, self.cutter_color_list,
                                self.default_segment_color_list, self.result_segment_color_list)

    def read_segment(self) -> Segment:
        return Segment(Point(self.x1_box.value(), self.y1_box.value()), Point(self.x2_box.value(), self.y2_box.value()))

    def read_cutter(self) -> Cutter:
        return Cutter(Point(self.xleft_box.value(), self.ytop_box.value()), Point(self.xright_box.value(), self.ybottom_box.value()))

    def clean_btn_handler(self) -> None:
        self.canvas.clear_all()

    def add_segment_btn_handler(self) -> None:
        self.canvas.add_segment(self.read_segment())

    def set_cutter_btn_handler(self) -> None:
        self.canvas.set_cutter(self.read_cutter())

    def cut_btn_handler(self) -> None:
        self.canvas.cut()

    def bind_buttons(self) -> None:
        self.clear_btn.clicked.connect(self.clean_btn_handler)
        self.add_segment_btn.clicked.connect(self.add_segment_btn_handler)
        self.set_cutter_btn.clicked.connect(self.set_cutter_btn_handler)
        self.cut_btn.clicked.connect(self.cut_btn_handler)

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
