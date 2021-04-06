from enum import Enum


class Figure(Enum):
    CIRCLE = 0
    ELLIPSE = 1

    def __str__(self) -> str:
        interp = {
            Figure.CIRCLE: 'Окружность',
            Figure.ELLIPSE: 'Эллипс'
        }
        return interp[self]
