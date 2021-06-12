from collections import Callable
from enum import Enum

from PyQt5.QtWidgets import QComboBox

from numpy import sin, cos, exp, sqrt


class Func(Enum):
    F1 = 0
    F2 = 1
    F3 = 2
    F4 = 3
    F5 = 4
    F6 = 5
    F7 = 6

    def __str__(self) -> str:
        interp = {
            Func.F1: 'sin(x) * sin(x) + cos(z) * cos(z)',
            Func.F2: 'x^2 / 20 - z^2 / 20',
            Func.F3: 'x^2 / 20 + z^2 / 20',
            Func.F4: 'exp(sin(sqrt(x^2 + z^2)))',
            Func.F5: 'x * z / 10',
            Func.F6: 'sqrt(x^2 + z^2 + 25)',
            Func.F7: 'sin(x) * cos(z)',
        }
        return interp[self]

    def _get_source(self) -> Callable:
        interp = {
            Func.F1: lambda x, z: sin(x) * sin(x) + cos(z) * cos(z),
            Func.F2: lambda x, z: x ** 2 / 20 - z ** 2 / 20,
            Func.F3: lambda x, z: x ** 2 / 20 + z ** 2 / 20,
            Func.F4: lambda x, z: exp(sin(sqrt(x ** 2 + z ** 2))),
            Func.F5: lambda x, z: x * z,
            Func.F6: lambda x, z: sqrt(x ** 2 + z ** 2 + 25),
            Func.F7: lambda x, z: sin(x) * cos(z),
        }
        return interp[self]

    def calculate(self, x, z):
        func = self._get_source()
        return func(x, z)


class FuncList(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

    def get(self) -> Func:
        return Func(self.currentIndex())
