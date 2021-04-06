
from enum import Enum

class Way(Enum):
    CAN = 0
    PARAM = 1
    BRES = 2
    MIDP = 3
    LIB = 4

    def __str__(self) -> str:
        interp = {
            Way.CAN: 'Каноническое уравнение',
            Way.PARAM: 'Параметрическое уравнение',
            Way.BRES: 'Брезенхем',
            Way.MIDP: 'Средней точки',
            Way.LIB: 'Библиотечная функция'
        }
        return interp[self]

    @staticmethod
    def get_all() -> list:
        return [Way(i) for i in range(len(Way))]

