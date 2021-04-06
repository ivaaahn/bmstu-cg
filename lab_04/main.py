from PyQt5.QtWidgets import QApplication
from loguru import logger

import sys

from main_window import MainWindow


logger.remove()
logger.add("./logs/spam.log", rotation="08:00", level='DEBUG')
logger.add(sys.stderr, level="ERROR")
logger.add('./logs/errors.log', level="ERROR")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
