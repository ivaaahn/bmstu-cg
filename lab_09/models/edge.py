from models.point import Point
from models.segment import Segment
from models.vector import Vector


class Edge(Segment):
    def __init__(self, p1: Point, p2: Point) -> None:
        super(Edge, self).__init__(p1, p2)

    @staticmethod
    def build(p1: Point, p2: Point, straight: bool = False) -> 'Edge':
        if straight:
            if abs(p2.x - p1.x) < abs(p2.y - p1.y):
                p2.x = p1.x
            else:
                p2.y = p1.y
        return Edge(p1, p2)

    def point_is_visible(self, point: Point) -> bool:
        """при учете, что обход будет против часовой"""
        return Vector.cross_prod(self.to_vector(), Segment(self.p1, point).to_vector()) >= 0

    def find_intersect(self, s: Segment, n: Vector) -> Point:
        w = Segment(self.p1, s.p1).to_vector()
        d = s.to_vector()

        t = -Vector.dot_prod(w, n) / Vector.dot_prod(d, n)

        return Point(round(s.p1.x + d.x * t), round(s.p1.y + d.y * t))
