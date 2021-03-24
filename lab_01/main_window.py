from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap
import design.main_window as mainUI
from popups import EditPointPopup, AddPointPopup, TaskPopup, AnsPopup
from points import Points
from circle import Circle
from triangle import Triangle
from errors import ErrorCount
from point import Point


class MainWindow(QMainWindow, mainUI.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initCanvas()
        self.initPopups()
        self.bindButtons()
        self.drawer.addition_init(
            self.pointsTable, self.moveBtn, self.pointBtn)

    def initPopups(self):
        self.addPopup = None
        self.editPopup = None
        self.taskPopup = None
        self.ansPopup = None

    def initCanvas(self):
        self.canvas = QPixmap(1, 1)
        self.canvas.fill(Qt.white)
        self.step = 2

    def bindButtons(self):
        self.addBtn.clicked.connect(self.showAddPopup)
        self.delBtn.clicked.connect(self.rmPoint)
        self.editBtn.clicked.connect(self.showEditPopup)
        self.incBtn.clicked.connect(self.drawer.increase)
        self.decBtn.clicked.connect(self.drawer.decrease)
        self.helpBtn.clicked.connect(self.showTaskPopup)
        self.solveBtn.clicked.connect(self.solve)
        self.scaleAns.clicked.connect(self.scaleAnswer)
        self.clearBtn.clicked.connect(self.clearTable)

    def clearTable(self):
        self.pointsTable.removeAll()
        Points.data.clear()
        Points.clearAns()
        self.repaint()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Вы уверены?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def showAddPopup(self):
        self.addPopup = AddPointPopup(self.pointsTable, self.repaint)
        self.addPopup.show()

    def showTaskPopup(self):
        self.taskPopup = TaskPopup()
        self.taskPopup.show()

    def showEditPopup(self):
        if self.pointsTable.currentRow() >= 0:
            self.editPopup = EditPointPopup(self.pointsTable, self.repaint)
            self.editPopup.show()

    def rmPoint(self):
        self.pointsTable.remove()
        self.repaint()

    def solve(self):
        if len(Points.data) >= 3:
            if Points.need_update:
                Points.clearAns()
                Points.updateSolve()

                if Points.no_solve:
                    ErrorCount("Треугольник выродился в прямую или точку")
                else:
                    self.drawer.changeCenter(
                        Circle(Points.best_triangle).center)
        else:
            ErrorCount(
                'Вы ввели недостаточно попарно различных точек!\n'
                f'Необходимо, как минимум, 3 точки.\nВведите еще {3 - len(Points.data)}')

        Points.need_update = False

        if Points.no_solve is False:
            circle = Circle(Points.best_triangle)
            diff = Points.best_diff
            outside = Points.outside_triangle
            into = Points.into_triangle

            text = \
                '<html>'\
                '<style>'\
                'h3 {text-align: center}'\
                'p {text-align: center}'\
                '</style>'\
                '<h3>Искомый треугольник:</h3>'\
                f'<p><b><font size="4" color="red" face="Sawasdee">{str(Points.best_triangle)}</font></b></p>'\
                f'<b>Описанная окружность:</b> {str(circle)}.<br>'\
                f'<b>Внутри треугольника:</b> {into} точек.<br>'\
                f'<b>Вне треугольника, но внутри окружности</b>: {outside} точек.<br>'\
                f'<b>Разница:</b> {diff}'\
                '</html>'

            self.ansPopup = AnsPopup(text)
            self.ansPopup.show()

    def scaleAnswer(self):
        if Points.no_solve is False:
            self.drawer.scaleUp(Circle(Points.best_triangle))

        elif Points.no_solve and len(Points.data) >= 2:
            p_min, p_max = Points.getMinMaxPoints()

            cx = (p_max.x + p_min.x) / 2
            cy = (p_max.y + p_min.y) / 2

            center_p = Point(point=(cx, cy))

            self.drawer.fullSize(p_min, p_max)
            self.drawer.changeCenter(center_p)

        elif Points.no_solve and len(Points.data) == 1:
            p = list(Points.data.items())[0][1]
            self.drawer.changeCenter(p)

        else:
            self.drawer.dx = self.drawer.dy = 0
            self.drawer.coef = 40
            self.drawer.updateSizes()
            self.drawer.stepUpdate()
            self.repaint()

    def _drawGrid(self, qp: QPainter):
        pen = QPen(Qt.green)
        pen.setWidth(1)
        qp.setPen(pen)

        coef = self.drawer.coef
        step = self.drawer.step

        for x in range(self.x0, self.x_max, coef * step):
            qp.drawLine(x, self.y_min, x, self.y_max)

        for x in range(self.x0 - coef * step, self.x_min, -coef * step):
            qp.drawLine(x, self.y_min, x, self.y_max)

        for y in range(self.y0, self.y_max, coef * step):
            qp.drawLine(self.x_min, y, self.x_max, y)

        for y in range(self.y0 - coef * step, self.y_min, -coef * step):
            qp.drawLine(self.x_min, y, self.x_max, y)

    def _drawPoints(self, qp: QPainter):
        pen = QPen(Qt.black)
        pen.setWidth(1)

        pen_lbl = QPen(Qt.red)
        pen_lbl.setWidth(1)

        brush = QBrush(Qt.red)
        brush_ans = QBrush(Qt.magenta)
        brush_triang = QBrush(Qt.darkGreen)

        font = qp.font()
        font.setPointSize(16)
        font.setBold(True)
        qp.setFont(font)

        for point in Points.data.values():
            point_canv = self.drawer.toCanv(point)
            solve = Points.data_into + Points.data_outside

            if not Points.no_solve and point in solve:
                qp.setBrush(brush_ans)
                qp.setPen(pen)
                qp.drawEllipse(point_canv.toQpoint(), 8, 8)
                qp.setPen(pen_lbl)
                qp.drawText(point_canv.x - 40, point_canv.y - 12, str(point))
            elif not Points.no_solve and point in Points.best_triangle.getPoints():
                qp.setBrush(brush_triang)
                qp.setPen(pen)
                qp.drawEllipse(point_canv.toQpoint(), 8, 8)
                qp.setPen(pen_lbl)
                qp.drawText(point_canv.x - 40, point_canv.y - 12, str(point))
            else:
                qp.setPen(pen)
                qp.setBrush(brush)
                qp.drawEllipse(point_canv.toQpoint(), 7, 7)
                qp.setPen(pen_lbl)
                qp.drawText(point_canv.x - 20, point_canv.y - 10, point.label)

    def _drawAnswer(self, qp: QPainter):
        def _drawTriangle(qp: QPainter, triangle: Triangle):
            raw_points = (triangle.pA, triangle.pB, triangle.pC)
            points = list(
                map(lambda x: self.drawer.toCanv(x).toQpoint(), raw_points))

            pen = QPen(Qt.blue)
            pen.setWidth(4)
            qp.setPen(pen)

            qp.drawLine(points[0], points[1])
            qp.drawLine(points[0], points[2])
            qp.drawLine(points[1], points[2])

        def _drawCircle(qp: QPainter, circle: Circle):
            center = self.drawer.toCanv(circle.center)
            rad = self.drawer.valueToCanv(circle.radius)

            pen = QPen(Qt.darkMagenta)
            pen.setWidth(5)

            pen_center = QPen(Qt.darkCyan)
            pen_center.setWidth(6)

            pen_lbl = QPen(Qt.black)
            font = qp.font()
            font.setPointSize(18)

            qp.setPen(pen)
            qp.drawEllipse(center.toQpoint(), rad, rad)

            qp.setPen(pen_center)
            qp.drawEllipse(center.toQpoint(), 3, 3)

            qp.setPen(pen_lbl)
            qp.setFont(font)
            qp.drawText(center.x - 10, center.y - 10, center.label)

        def _drawPerp(qp, triangle: Triangle, circle: Circle):
            pen = QPen(Qt.black)
            pen.setWidth(3)
            qp.setPen(pen)

            midAB = triangle.midline(triangle.pA, triangle.pB)
            midBC = triangle.midline(triangle.pB, triangle.pC)
            midAC = triangle.midline(triangle.pA, triangle.pC)

            mids = [self.drawer.toCanv(p).toQpoint()
                    for p in (midAB, midAC, midBC)]
            O = self.drawer.toCanv(circle.center).toQpoint()

            qp.drawLine(mids[0], O)
            qp.drawLine(mids[1], O)
            qp.drawLine(mids[2], O)

        if Points.no_solve is False:
            triangle = Points.best_triangle
            circle = Circle(triangle)

            _drawTriangle(qp, triangle)
            _drawCircle(qp, circle)
            _drawPerp(qp, triangle, circle)

    def _drawAxis(self, qp):
        penAx = QPen(Qt.black)
        penAx.setWidth(3)
        pen_l = QPen(Qt.black)
        font = qp.font()
        font.setPointSize(14)
        qp.setFont(font)
        qp.setPen(penAx)

        step = self.drawer.step
        coef = self.drawer.coef

        qp.drawText(self.x0 - 15, self.y0 + 20, '0')

        if self.drawer.dx < -self.drawer.width() // 2:
            qp.setPen(penAx)
            qp.drawLine(self.x_min, self.y_min, self.x_min, self.y_max)
            qp.setPen(pen_l)

            k = -step
            for y in range(self.y0 + coef * step, self.y_max, step * coef):
                qp.drawText(self.x_min + 20, y + 7, str(k))
                k -= step

            k = step
            for y in range(self.y0 - coef * step, self.y_min, -step * coef):
                qp.drawText(self.x_min + 20, y + 7, str(k))
                k += step

        elif self.drawer.dx > self.drawer.width() // 2:
            qp.setPen(penAx)
            qp.drawLine(self.x_max, self.y_min, self.x_max, self.y_max)
            qp.setPen(pen_l)

            k = -step
            for y in range(self.y0 + coef * step, self.y_max, step * coef):
                qp.drawText(self.x_max - 30, y + 7, str(k))
                k -= step

            k = step
            for y in range(self.y0 - coef * step, self.y_min, -step * coef):
                qp.drawText(self.x_max - 25, y + 7, str(k))
                k += step

        else:
            qp.setPen(penAx)
            qp.drawLine(self.x0, self.y_min, self.x0, self.y_max)
            qp.drawLine(self.x0, self.y_min, self.x0 - 7, self.y_min + 12)
            qp.drawLine(self.x0, self.y_min, self.x0 + 7, self.y_min + 12)
            qp.setPen(pen_l)

            if self.drawer.coef <= 4:
                offset_p, offset_m = 40, 35
            else:
                offset_p, offset_m = 30, 25

            k = -step
            for y in range(self.y0 + coef * step, self.y_max, step * coef):
                qp.drawText(self.x0 - offset_p, y + 7, str(k))
                k -= step

            k = step
            for y in range(self.y0 - coef * step, self.y_min, -step * coef):
                qp.drawText(self.x0 - offset_m, y + 7, str(k))
                k += step

        if self.drawer.dy > self.drawer.height() // 2:
            qp.setPen(penAx)
            qp.drawLine(self.x_min, self.y_max, self.x_max, self.y_max)
            qp.setPen(pen_l)

            k = step
            for x in range(self.x0 + coef * step, self.x_max, step * coef):
                qp.drawText(x - 5, self.y_max - 15, str(k))
                k += step

            k = -step
            for x in range(self.x0 - coef * step, self.x_min, -step * coef):
                qp.drawText(x - 10, self.y_max - 15, str(k))
                k -= step

        elif self.drawer.dy < -self.drawer.height() // 2:
            qp.setPen(penAx)
            qp.drawLine(self.x_min, self.y_min, self.x_max, self.y_min)
            qp.setPen(pen_l)

            k = step
            for x in range(self.x0 + coef * step, self.x_max, step * coef):
                qp.drawText(x - 5, self.y_min + 15, str(k))
                k += step

            k = -step
            for x in range(self.x0 - coef * step, self.x_min, -step * coef):
                qp.drawText(x - 10, self.y_min + 15, str(k))
                k -= step

        else:
            qp.setPen(penAx)
            qp.drawLine(self.x_min, self.y0, self.x_max, self.y0)
            qp.drawLine(self.x_max - 12, self.y0 - 7, self.x_max, self.y0)
            qp.drawLine(self.x_max - 12, self.y0 + 7, self.x_max, self.y0)
            qp.setPen(pen_l)

            k = step
            for x in range(self.x0 + coef * step, self.x_max, step * coef):
                qp.drawText(x - 5, self.y0 + 20, str(k))
                k += step

            k = -step
            for x in range(self.x0 - coef * step, self.x_min, -step * coef):
                qp.drawText(x - 10, self.y0 + 20, str(k))
                k -= step

    def paintEvent(self, event):
        self.drawer.updateSizes()

        self.x_min = self.drawer.x_min
        self.x_max = self.drawer.x_max

        self.y_min = self.drawer.y_min
        self.y_max = self.drawer.y_max

        self.x0 = self.drawer.x0
        self.y0 = self.drawer.y0

        qp = QPainter(self)
        qp.drawPixmap(QRect(self.x_min, self.y_min,
                            self.x_max, self.y_max), self.canvas)
        self._drawGrid(qp)
        self._drawAxis(qp)
        self._drawAnswer(qp)
        self._drawPoints(qp)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.solve()
        elif event.key() == Qt.Key_Plus:
            self.drawer.increase()
        elif event.key() == Qt.Key_Minus:
            self.drawer.decrease()
