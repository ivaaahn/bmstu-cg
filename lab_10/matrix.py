from math import cos, sin

import numpy as np
import utils
from models.point import Point
from utils import to_rad, Axis


class Matrix:
    def __init__(self, n: int = 4, m: int = 4) -> None:
        self._value = np.eye(n, m)

    def rotate(self, theta: [int, float], axis: Axis):
        self._value = self._value @ self._get_rotation_matrix(to_rad(theta), axis)

    def transform_point(self, p: Point, scale: float):
        res_point = p.to_ndarray() @ self._value

        for i in range(3):
            res_point[i] *= scale

        res_point = Point(res_point[0], res_point[1], res_point[2])
        res_point.translate(dx=(utils.W / 2), dy=(utils.H / 2))

        return res_point

    @staticmethod
    def _get_rotation_matrix(theta: float, axis: Axis) -> np.ndarray:
        if axis is Axis.X:
            m = np.array([[1, 0, 0, 0],
                          [0, cos(theta), sin(theta), 0],
                          [0, -sin(theta), cos(theta), 0],
                          [0, 0, 0, 1]])
        elif axis is Axis.Y:
            m = np.array([[cos(theta), 0, -sin(theta), 0],
                          [0, 1, 0, 0],
                          [sin(theta), 0, cos(theta), 0],
                          [0, 0, 0, 1]])
        else:
            m = np.array([[cos(theta), sin(theta), 0, 0],
                          [-sin(theta), cos(theta), 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])

        return m
