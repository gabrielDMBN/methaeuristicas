# utils.py
import math
from typing import Tuple

Coord = Tuple[int, int]  # (x, y)

def distance(a: Coord, b: Coord) -> float:
    """
    Distância Euclidiana entre duas células do grid.
    """
    (x1, y1), (x2, y2) = a, b
    return math.hypot(x1 - x2, y1 - y2)
