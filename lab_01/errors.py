from PyQt5.QtWidgets import QMessageBox


class ErrorInput(QMessageBox):
    def __init__(self, text: str):
        super().__init__(QMessageBox.Critical, "Неккоректный ввод", text)
        self.setStandardButtons(QMessageBox.Cancel)
        self.exec_()


class ErrorCount(QMessageBox):
    def __init__(self, text: str):
        super().__init__(QMessageBox.Critical, "Недостаточно точек", text)

        self.setStandardButtons(QMessageBox.Cancel)
        self.exec_()


class ScaleInfo(QMessageBox):
    def __init__(self, text: str):
        super().__init__(QMessageBox.Critical, "Масштаб", text)

        self.setStandardButtons(QMessageBox.Cancel)
        self.exec_()
