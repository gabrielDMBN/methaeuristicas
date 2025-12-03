# td_solution.py
from typing import List
from utils import distance
from TDInstance import TDInstance


class TDSolution:
    """
    Representa uma solução para o problema.
    assignments[i] = -1  -> célula vazia
    assignments[i] = k   -> torre do tipo k naquela célula
    """

    def __init__(self, assignments: List[int]):
        self.assignments = assignments

    def total_cost(self, instance: TDInstance) -> int:
        total = 0
        for idx, tower_id in enumerate(self.assignments):
            if tower_id == -1:
                continue
            total += instance.get_tower_type(tower_id).cost
        return total

    def is_feasible(self, instance: TDInstance) -> bool:
        return self.total_cost(instance) <= instance.budget

    def total_damage(self, instance: TDInstance) -> float:
        """
        Dano total causado a UM inimigo que percorre o caminho.
        1 tile = 1 segundo.
        """
        if not self.is_feasible(instance):
            return -1e9  # penalização forte

        dmg = 0.0
        for idx, tower_id in enumerate(self.assignments):
            if tower_id == -1:
                continue

            tower = instance.get_tower_type(tower_id)
            tower_pos = instance.buildable_cells[idx]

            for tile in instance.path:
                if distance(tower_pos, tile) <= tower.range:
                    dmg += tower.dps  # 1 segundo por tile

        return dmg

    def __repr__(self):
        return f"TDSolution(assignments={self.assignments})"

    def copy(self):
        """Retorna uma cópia independente da solução atual."""
        return TDSolution(self.assignments.copy())
