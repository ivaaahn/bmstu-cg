from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from typing import NoReturn, Tuple
from enum import Enum

from line import Algorithm, Color
from point import Point

from loguru import logger


class Columns(Enum):
    BEGIN = 0
    END = 1
    COLOR = 2
    ALG = 3


class LinesTable(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def add(self, alg: Algorithm, color: Color, coords: Tuple[Point]) -> NoReturn:
        logger.debug(f"LinesTable.add({alg, color, coords})")
        logger.debug(f"rowCount() = {self.rowCount()}")


        curr_row = self.rowCount()
        self.insertRow(curr_row)

        self.setItem(curr_row, Columns.BEGIN.value, QTableWidgetItem(str(coords[0])))
        self.setItem(curr_row, Columns.END.value, QTableWidgetItem(str(coords[1])))
        self.setItem(curr_row, Columns.COLOR.value, QTableWidgetItem(str(color)))
        self.setItem(curr_row, Columns.ALG.value, QTableWidgetItem(str(alg)))

        logger.debug(f"rowCount() = {self.rowCount()}")



    def remove(self):
        curr_row = self.currentRow()
        if curr_row >= 0:
            self.removeRow(curr_row)

    def remove_all(self):
        self.setRowCount(0)