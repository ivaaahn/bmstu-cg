from typing import List

import utils


class Horizon:
    def __init__(self) -> None:
        self._top: List[int] = []
        self._bottom: List[int] = []

        self.reset_all()

    @property
    def top(self) -> List[int]:
        return self._top

    @property
    def bottom(self) -> List[int]:
        return self._bottom

    def reset_all(self) -> None:
        self.reset_top()
        self.reset_bottom()

    def reset_top(self) -> None:
        self._top: List[int] = [0 for _ in range(utils.W)]

    def reset_bottom(self) -> None:
        self._bottom: List[int] = [utils.H for _ in range(utils.W)]
