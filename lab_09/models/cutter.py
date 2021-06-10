from copy import deepcopy
from typing import List, Optional

from exceptions import NonConvex, DegenerateCutter
from models.point import Point
from models.polygon import Polygon
from models.edge import Edge
from models.segment import Segment
from models.vector import Vector


class Cutter(Polygon):
    def __init__(self):
        super().__init__(from_user=True)
        self._normals: List[Vector] = []
        self._sign = None

    def reset(self) -> None:
        super().reset()
        self._sign = None
        self._normals.clear()

    def reverse(self) -> None:
        super().reverse()
        self._normals.reverse()

    def add_vertex(self, v: Point, straight: bool = False, closing: bool = False) -> Optional[Edge]:
        edge = super().add_vertex(v, straight, closing)

        if len(self.vertices) >= 3 and self._sign is None:
            self._set_sign()

        if len(self.vertices) >= 4 and not self._is_convex(closing):
            raise NonConvex("Невыпуклый отсекатель")

        return edge

    def close(self) -> Edge:
        edge = super().close()

        if not self._is_convex():
            raise NonConvex("Невыпуклый отсекатель")

        if self._sign is None:
            raise DegenerateCutter("Вырожденный отсекатель")

        if self._sign == -1:
            self.reverse()

        return edge

    def _is_convex(self, closing: bool = False) -> bool:
        if self._sign is None:
            return True

        prev = Edge(self.vertices[-3], self.vertices[-2]).to_vector()
        last = Edge(self.vertices[-2], self.vertices[-1]).to_vector()

        result = self._sign * Vector.cross_prod(prev, last) >= 0

        if closing:
            first = Edge(self.vertices[0], self.vertices[1]).to_vector()
            result = result and (self._sign * Vector.cross_prod(last, first) >= 0)

        return result

    def _set_sign(self) -> None:
        prev = Edge(self.vertices[-3], self.vertices[-2]).to_vector()
        last = Edge(self.vertices[-2], self.vertices[-1]).to_vector()

        cross_prod = Vector.cross_prod(prev, last)
        if cross_prod > 0:
            self._sign = 1
        elif cross_prod < 0:
            self._sign = -1

    def _get_normal(self, first_seg_vert: int):
        vert_start = self.vertices[first_seg_vert]
        edge = Edge(vert_start, self.vertices[first_seg_vert + 1])
        vector = edge.to_vector()

        n = vector.normal()

        dot_prod = 0
        p = first_seg_vert + 2
        while not dot_prod and p < len(self.vertices) + first_seg_vert:
            dot_prod = Vector.dot_prod(n, Edge(vert_start, self.vertices[p % len(self.vertices)]).to_vector())
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

    def get_closest_project(self, p: Point) -> Point:
        edges = iter(self.edges)
        best_edge = next(edges)

        min_proj = best_edge.proj(p)

        for edge in edges:
            proj = edge.proj(p)
            if p.dist_to(proj) < p.dist_to(min_proj):
                min_proj, best_edge = proj, edge

        return min_proj

    def cut_poly(self, poly: Polygon) -> Optional[Polygon]:
        res_poly = deepcopy(poly)
        for i in range(len(self.vertices) - 1):
            curr_edge = Edge(self.vertices[i], self.vertices[i + 1])
            res_poly = Cutter.cut_relative_to_edge(res_poly, curr_edge, self.normals[i])
            res_poly.close()

            if len(res_poly.vertices) < 3:
                return None

        return res_poly

    @staticmethod
    def cut_relative_to_edge(src_poly: Polygon, edge: Edge, n: Vector) -> Polygon:
        result = Polygon(from_user=False)

        vertices = iter(src_poly.vertices)

        prev = next(vertices)
        prev_is_visible = edge.point_is_visible(prev)

        if prev_is_visible:
            result.add_vertex(prev)

        for vert in vertices:
            curr_is_visible = edge.point_is_visible(vert)

            if prev_is_visible:
                if curr_is_visible:
                    result.add_vertex(vert)
                else:
                    result.add_vertex(edge.find_intersect(Segment(prev, vert), n))
            else:
                if curr_is_visible:
                    result.add_vertex(edge.find_intersect(Segment(prev, vert), n))
                    result.add_vertex(vert)

            prev, prev_is_visible = vert, curr_is_visible

        return result
