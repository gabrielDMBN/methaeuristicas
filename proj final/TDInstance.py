# td_instance.py
from typing import List, Tuple
from TowerType import TowerType
from utils import Coord

class TDInstance:
    """
    Representa uma instância do problema de Tower Defense.
    """

    def __init__(self,
                 width: int,
                 height: int,
                 buildable_cells: List[Coord],
                 path: List[Coord],
                 tower_types: List[TowerType],
                 budget: int):
        self.width = width
        self.height = height
        self.buildable_cells = buildable_cells
        self.path = path
        self.tower_types = tower_types
        self.budget = budget

    def num_buildable(self) -> int:
        return len(self.buildable_cells)

    def get_tower_type(self, tower_id: int) -> TowerType:
        return self.tower_types[tower_id]
