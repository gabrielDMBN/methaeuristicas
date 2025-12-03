# tower_type.py
from dataclasses import dataclass

@dataclass
class TowerType:
    """
    Representa um tipo de torre disponível no jogo.
    """
    id: int
    name: str
    cost: int
    range: float
    dps: float

    def __repr__(self) -> str:
        return (f"TowerType(id={self.id}, name={self.name}, "
                f"cost={self.cost}, range={self.range}, dps={self.dps})")
