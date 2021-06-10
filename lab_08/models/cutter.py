from typing import List, Optional, Tuple

from exceptions import UnableToClose, NonConvex, DegenerateCutter, SelfIntersection
from models.point import Point
from models.segment import Segment
from models.vector import Vector


class Cutter:
    def __init__(self):
        self._vertices: List[Point] = []
        self._closed: bool = False

        self._normals: List[float] = []
        self._sign = None

    def reset(self) -> None:
        self._vertices.clear()
        self._closed = False

        self._normals.clear()
        self._sign = None

    @property
    def vertices(self) -> List[Point]:
        return self._vertices

    def add_vertex(self, v: Point, straight: bool = False, closing: bool = False) -> Optional[Segment]:
        if len(self.vertices) >= 1 and straight:
            prev = self.vertices[-1]
            if abs(v.x - prev.x) < abs(v.y - prev.y):
                v.x = prev.x
            else:
                v.y = prev.y

        if len(self.vertices) >= 3 and self.self_intersections_exist(v, closing):
            raise SelfIntersection("Многоугольник не может содержать самопересечения")

        self.vertices.append(v)

        if len(self.vertices) >= 3 and self._sign is None:
            self._set_sign()

        if len(self.vertices) >= 4 and not self._is_convex(closing):
            raise NonConvex("Невыпуклый отсекатель")

        if len(self.vertices) < 2:
            return None

        return Segment(self.vertices[-2], self.vertices[-1])

    def _vertices_enough_to_close(self) -> bool:
        return len(self._vertices) >= 3

    @property
    def edges(self) -> List[Segment]:
        v = self._vertices
        return [Segment(v[i], v[i + 1]) for i in range(len(v) - 1)]

    def close(self) -> Segment:
        if not self._vertices_enough_to_close():
            raise UnableToClose('Недостаточно ребер, чтобы замкнуть')

        if self.vertices[-1] != self.vertices[0]:
            self.add_vertex(self.vertices[0], closing=True)

        if self._sign is None:
            raise DegenerateCutter("Вырожденный отсекатель")

        self._closed = True

        # if self._sign == -1:
        #     self.vertices.reverse()

        return Segment(self.vertices[-2], self.vertices[-1])

    def is_closed(self) -> bool:
        return self._closed

    def _is_convex(self, closing) -> bool:
        if self._sign is None:
            return True

        prev = Segment(self.vertices[-3], self.vertices[-2]).to_vector()
        last = Segment(self.vertices[-2], self.vertices[-1]).to_vector()

        result = self._sign * Vector.cross_prod(prev, last) >= 0

        if closing:
            first = Segment(self.vertices[0], self.vertices[1]).to_vector()
            result = result and (self._sign * Vector.cross_prod(last, first) >= 0)

        return result

    def _set_sign(self) -> None:
        prev = Segment(self.vertices[-3], self.vertices[-2]).to_vector()
        last = Segment(self.vertices[-2], self.vertices[-1]).to_vector()

        cross_prod = Vector.cross_prod(prev, last)
        if cross_prod > 0:
            self._sign = 1
        elif cross_prod < 0:
            self._sign = -1

    def _get_normal(self, first_seg_vert: int):
        vert_start = self.vertices[first_seg_vert]
        edge = Segment(vert_start, self.vertices[first_seg_vert + 1])
        vector = edge.to_vector()

        n = vector.normal()

        dot_prod = 0
        p = first_seg_vert + 2
        while not dot_prod and p < len(self.vertices) + first_seg_vert:
            dot_prod = Vector.dot_prod(n, Segment(vert_start, self.vertices[p % len(self.vertices)]).to_vector())
            p += 1

        if dot_prod < 0:
            n = -n

        return n

    @property
    def tangents(self) -> List[Optional[float]]:
        return [e.tangent for e in self.edges]

    @property
    def normals(self) -> List[Vector]:
        if not self._normals:
            # self._normals = [e.to_vector().normal() for e in self.edges]
            self._normals = [self._get_normal(i) for i in range(len(self.vertices) - 1)]

        return self._normals

    def get_closest_vertex(self, p: Point) -> Point:
        vertices = iter(self.vertices)
        best_vert = next(vertices)
        best_dist = p.dist_to(best_vert)

        for v in vertices:
            dist = p.dist_to(v)
            if dist < best_dist:
                best_dist, best_vert = dist, v

        return best_vert

    def get_closest_grad(self, s: Segment) -> float:
        closest_edge = self._get_closest_edge_and_proj(s.p1)[0]
        return closest_edge.tangent

    def self_intersections_exist(self, v: Point, closing: bool) -> bool:
        # edges = iter(self.edges[:-1])

        # if closing:
        #     next(edges)

        edges = self.edges

        new_seg = Segment(self.vertices[-1], v)

        for edge in edges:
            if Segment.is_intersect(edge, new_seg):
                return True

        return False

    def _get_closest_edge_and_proj(self, p: Point) -> Tuple[Segment, Point]:
        edges = iter(self.edges)
        best_edge = next(edges)

        min_proj = best_edge.proj(p)

        for edge in edges:
            proj = edge.proj(p)
            if p.dist_to(proj) < p.dist_to(min_proj):
                min_proj, best_edge = proj, edge

        return best_edge, min_proj

    def get_closest_project(self, p: Point) -> Point:
        return self._get_closest_edge_and_proj(p)[1]

    def cut(self, segment: Segment) -> Optional[Segment]:
        t_start, t_end = 0.0, 1.0

        d = segment.to_vector()

        for edge, n in zip(self.edges, self.normals):
            f = edge.p1 if edge.p1 != segment.p1 else edge.p2

            w = Segment(f, segment.p1).to_vector()

            d_dp = Vector.dot_prod(d, n)
            w_dp = Vector.dot_prod(w, n)

            if d_dp == 0:
                if w_dp < 0: return
                continue

            t = -w_dp / d_dp

            if d_dp > 0:
                if t > 1: return
                t_start = max(t, t_start)

            else:
                if t < 0: return
                t_end = min(t, t_end)

        if t_start <= t_end:
            p1 = Point(round(segment.p1.x + d.x * t_start), round(segment.p1.y + d.y * t_start))
            p2 = Point(round(segment.p1.x + d.x * t_end), round(segment.p1.y + d.y * t_end))
            return Segment(p1, p2)

        return None
