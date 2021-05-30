from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from models.point import Point


class PointsTable(QTableWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

    def add(self, point: Point) -> None:
        curr_row = self.rowCount()
        self.insertRow(curr_row)

        self.setItem(curr_row, 0, QTableWidgetItem(point.title))
        self.setItem(curr_row, 1, QTableWidgetItem(str(point.x)))
        self.setItem(curr_row, 2, QTableWidgetItem(str(point.y)))

    def clear(self) -> None:
        self.setRowCount(0)
