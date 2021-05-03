from timeit import timeit
from typing import Callable

from models.figure import Figure
from properties.color import Color
from properties.mode import Mode


class TimeTesting:
    def __init__(self, fig: Figure, fill_func: Callable[[Color, Mode], None]) -> None:
        self.COUNT = 10
        self.fill = fill_func
        self.figure = fig

    def start(self) -> dict:
        """Замеряет время закраски в миллисекундах"""

        if not self.figure:
            self.figure.generate()

        result = timeit(lambda: self.fill(Color.BLACK, Mode.TESTING), number=self.COUNT) / self.COUNT * 1000

        return {'time': result, 'count': self.COUNT}
