from typing import Tuple
import matplotlib.pyplot as plt


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
    def __init__(self, all_angles: Tuple[int], data: dict) -> None:
        self._all_angles: Tuple = all_angles
        self._data = data

        plt.title("Сравнение кол-ва ступенек (длина отрезка = 50)")
        plt.xlabel('Угол (в градусах)', fontsize=12, color='blue')
        plt.ylabel('Кол-во ступенек', fontsize=12, color='red')

        for alg, stairs in data.items():
            plt.plot(self._all_angles, stairs, label=alg)

        plt.grid(True)
        plt.legend()
        plt.show()
