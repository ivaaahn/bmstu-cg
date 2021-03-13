from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from points import Points
from point import Point
from bisect import insort


class PointsTable(QTableWidget):
    def __init_(self, parent):
        super().__init__(parent)

    def add(self, new_point: Point):
        new_point.label = Points.getLabel()
        row_pos = self.rowCount()
        self.insertRow(row_pos)
        self.setItem(row_pos, 0, QTableWidgetItem(repr(new_point)))
        Points.data[new_point.label] = new_point

        Points.need_update = True

    def removeAll(self):
        Points.numbers = [x for x in range(1, 500)]
        self.setRowCount(0)

    def editPoint(self, new_point: Point):
        row_index = self.currentRow()
        Points.data.pop(new_point.label)

        item = QTableWidgetItem()
        item.setText(repr(new_point))

        self.setItem(row_index, 0, item)

        Points.data[new_point.label] = new_point
        Points.clearAns()

    def remove(self):
        row_index = self.currentRow()
        if row_index >= 0:
            rm_point = Point(text=self.item(row_index, 0).text())
            self.removeRow(row_index)

            Points.data.pop(rm_point.label)
            insort(Points.numbers, int(rm_point.label[1:]))

            Points.clearAns()
