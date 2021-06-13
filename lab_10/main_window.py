from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox as QMB

from controller import Controller
from qt.design import Ui_MainWindow
from utils import Ranges, Axis


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.controller = Controller(self.canvas, self.func_list.get(), self.color_list.get())
        self.bind_buttons()

    def _read_scale(self) -> int:
        return self.scale_coeff_box.value()

    def _read_rotate_x(self) -> float:
        return self.rotate_x_box.value()

    def _read_rotate_y(self) -> float:
        return self.rotate_y_box.value()

    def _read_rotate_z(self) -> float:
        return self.rotate_z_box.value()

    def _read_ranges(self) -> Ranges:
        r = Ranges()
        r.x_from = self.range_x_from_box.value()
        r.x_to = self.range_x_to_box.value()
        r.x_step = self.range_x_step_box.value()

        r.z_from = self.range_z_from_box.value()
        r.z_to = self.range_z_to_box.value()
        r.z_step = self.range_z_step_box.value()

        return r

    def change_ranges_btn_handler(self) -> None:
        self.controller.ranges = self._read_ranges()

    def rotate_btn_handler(self, box: Axis) -> None:
        if box is Axis.X:
            rotate_params = self.rotate_x_box.value()
        elif box is Axis.Y:
            rotate_params = self.rotate_y_box.value()
        else:
            rotate_params = self.rotate_z_box.value()

        self.controller.rotate(rotate_params, box)

    def scale_btn_handler(self) -> None:
        self.controller.scale_param = self._read_scale()

    def func_changed(self) -> None:
        self.controller.function = self.func_list.get()

    def color_changed(self) -> None:
        self.controller.color = self.color_list.get()

    def render_btn_handler(self) -> None:
        self.controller.render()

    def clear_btn_handler(self) -> None:
        self.controller.clear_all()
        
    def bind_buttons(self) -> None:
        self.func_list.currentIndexChanged.connect(self.func_changed)
        self.color_list.currentIndexChanged.connect(self.color_changed)

        self.change_ranges_btn.clicked.connect(self.change_ranges_btn_handler)

        self.rotate_x_btn.clicked.connect(lambda _: self.rotate_btn_handler(Axis.X))
        self.rotate_y_btn.clicked.connect(lambda _: self.rotate_btn_handler(Axis.Y))
        self.rotate_z_btn.clicked.connect(lambda _: self.rotate_btn_handler(Axis.Z))

        self.scale_btn.clicked.connect(self.scale_btn_handler)

        self.render_btn.clicked.connect(self.render_btn_handler)
        self.clear_btn.clicked.connect(self.clear_btn_handler)

    def closeEvent(self, event):
        reply = QMB.question(self, 'Message', "Вы уверены?",
                             QMB.Yes | QMB.No, QMB.Yes)
        if reply == QMB.Yes:
            event.accept()
        else:
            event.ignore()
