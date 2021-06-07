from typing import List, Optional

from models.point import Point
from models.segment import Segment


class Cutter:
    def __init__(self):
        self._last_vertex: Optional[Point] = None
        self._edges: List[Segment] = []
        self._closed: bool = False
        self._sign = None

    @property
    def edges(self) -> List[Segment]:
        return self._edges

    def add_edge(self, new_edge: Segment) -> None:
        if len(self._edges) >= 2:
            self.check(self._edges[-1], new_edge)

        self.edges.append(new_edge)

        if len(self.edges) == 2:
            self.set_sign()

    def close(self) -> Segment:
        closing_edge = Segment(self.edges[-1].p2, self.edges[0].p1)

        self.check(closing_edge, self._edges[0])

        self.add_edge(closing_edge)

        self._closed = True
        return closing_edge

    def is_closed(self) -> bool:
        return self._closed

    def ready_to_close(self) -> bool:
        return len(self._edges) >= 2

    def check(self, e1: Segment, e2: Segment):
        if self._sign * Segment.cross_product(e1, e2) < 0:
            raise Exception("Невыпуклый отсекатель")

    def set_sign(self) -> None:
        self._sign = 1 if Segment.cross_product(self._edges[0], self._edges[1]) > 0 else -1
        print(self._sign)

    # def check_polygon():
    #     # Не существует многоугольника, у которого меньше 3 вершин
    #     if len(verteces_list) < 3:
    #         return False
    #         # Знаки всех векторых произведений должны быть одинаковыми:
    #     # запомним знак первого векторного произведения
    #     sign = 1 if vect_mul(get_vect(verteces_list[1], verteces_list[2]),
    #                          get_vect(verteces_list[0], verteces_list[1])) > 0 else -1
    #     # В цикле проверяем совпадения знаков векторных произведений
    #     # всех пар соседних ребер со знаком первого
    #     # векторного произведения
    #     for i in range(3, len(verteces_list)):
    #         if sign * vect_mul(get_vect(verteces_list[i - 1], verteces_list[i]),
    #                            get_vect(verteces_list[i - 2], verteces_list[i - 1])) < 0:
    #             # Возвращаем False при несовпадении знаков: прямоугольник невыпуклый
    #             return False
    #
    #     if sign < 0:
    #         # если знак отрицательный, значит обход был по часовой стрелке.
    #         # В дальнейших шагах мне нужно работать с обходом против часовой
    #         # стрелке (при выяснении направления нормали, например), поэтому
    #         # я переворчиваю список вершин (ну и соответственно при проходе
    #         # в обратном порядке, будет обход против часовой стрелки)
    #         verteces_list.reverse()
    #
    #     return True

    # @property
    # def left(self) -> int:
    #     return self._ltop.x
    #
    # @property
    # def right(self) -> int:
    #     return self._rbottom.x
    #
    # @property
    # def top(self) -> int:
    #     return self._ltop.y
    #
    # @property
    # def bottom(self) -> int:
    #     return self._rbottom.y
    #
    # @property
    # def rbottom(self) -> Point:
    #     return self._rbottom
    #
    # @property
    # def ltop(self) -> Point:
    #     return self._ltop
    #
    # @property
    # def lbottom(self) -> Point:
    #     return Point(self.left, self.bottom)
    #
    # @property
    # def rtop(self) -> Point:
    #     return Point(self.right, self.top)

    # def to_qrect(self) -> QRect:
    #     return QRect(self.ltop.to_qpoint(), self.rbottom.to_qpoint())
