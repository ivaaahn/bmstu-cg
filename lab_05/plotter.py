import numpy

from algorithms import Algorithms
from typing import Dict, Tuple, Callable, List
import matplotlib.pyplot as plt

from models.point import Point


class BarPlotter:
    def __init__(self, data: dict) -> None:
        labels = ['', 'Алгоритм заполнения со списком ребер и флагом.', '']
        values = [0, data.get('time'), 0]

        x = numpy.arange(len(labels))
        width = 0.35

        fig, ax = plt.subplots()
        rects = ax.bar(x, values, width)

        ax.set_ylabel('мс', fontsize=10)
        ax.set_title('Алгоритмы', pad=0)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)

        # ax.legend()
        fig.suptitle(f'Результат: {round(data.get("time"), 2)} мс ({data.get("count")} повторений)', fontsize=15)

        # ax.bar_label(rects, padding=3)

        plt.show()


class GraphPlotter:
    def __init__(self, rads: Tuple[int], data: Dict[Callable[[Point, int], List[Point]], float]) -> None:
        self._rads = rads
        self._data = data

        plt.title("Сравнение времени работы алгоритмов")
        plt.xlabel('Радиус окружности', fontsize=12, color='blue')
        plt.ylabel('Время выполнения (мкс)', fontsize=12, color='red')

        for alg, time in data.items():
            plt.plot(self._rads, time, label=str(
                Algorithms.get_way_and_figure(alg)[0]))

        plt.grid(True)
        plt.legend()
        plt.show()
