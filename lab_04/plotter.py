from algorithms import Algorithms
from typing import Dict, Tuple, Callable, List
import matplotlib.pyplot as plt

from point import Point

class BarPlotter:
    def __init__(self, data: dict) -> None:
        self._names = [str(alg)[:10]+'\n'+str(alg)[10:] for alg in data.keys()]
        self._values = [round(value, 2) for value in data.values()]
        self._fig, self._ax = plt.subplots(figsize=(14, 8))

        self._fig.suptitle('Замеры времени', fontsize=24)

        self._ax.set_xlabel('мс', fontsize=18)
        self._ax.barh(self._names, self._values)

        for tick in self._ax.xaxis.get_major_ticks() + self._ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(14)

        plt.show()

class GraphPlotter:
    def __init__(self, rads: Tuple[int], data: Dict[Callable[[Point, int], List[Point]], float]) -> None:
        self._rads = rads
        self._data = data

        plt.title("Сравнение времени работы алгоритмов")
        plt.xlabel('Радиус окружности', fontsize=12, color='blue')
        plt.ylabel('Время выполнения (мкс)', fontsize=12, color='red')

        # print(rads)

        # for key, value in self._data.items():
        #     print(f'{key}: {value}')

        for alg, time in data.items():
            plt.plot(self._rads, time, label=str(Algorithms.get_way_and_figure(alg)[0]))

        plt.grid(True)
        plt.legend()
        plt.show()
