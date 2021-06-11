from dataclasses import dataclass
from enum import Enum
from math import pi

W, H = 1354, 941


def to_rad(angle: [float, int]) -> float:
    return angle * pi / 180


def custom_round(num: float) -> int:
    return int(num + (0.5 if num > 0 else -0.5))


@dataclass
class Ranges:
    x_from: float = -10
    x_to: float = 10
    x_step: float = 0.1
    z_from: float = -10
    z_to: float = 10
    z_step: float = 0.1


class Axis(Enum):
    X = 0
    Y = 1
    Z = 2
