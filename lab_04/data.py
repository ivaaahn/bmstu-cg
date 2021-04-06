from typing import List

from ellipse import Ellipse
from spectrum import Spectrum


class Data:
    def __init__(self) -> None:
        self._ellipses: List[Ellipse] = []
        self._spectrums: List[Spectrum] = []

    @property
    def ellipses(self) -> List[Ellipse]:
        return self._ellipses

    @property
    def spectrums(self) -> List[List]:
        return self._spectrums

    def add_ellipse(self, ellipse: Ellipse) -> None:
        self._ellipses.append(ellipse)

    def add_spectrum(self, spectrum: Spectrum) -> None:
        self._spectrums.append(spectrum)

    def clear_all(self) -> None:
        self._clear_ellipses()
        self._clear_spectrums()

    def _clear_circles(self) -> None:
        self._circles.clear()

    def _clear_ellipses(self) -> None:
        self._ellipses.clear()

    def _clear_spectrums(self) -> None:
        self._spectrums.clear()
