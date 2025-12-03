# MapLoader.py
from typing import List, Set, Dict, Tuple
import os

from TDInstance import TDInstance
from TowerType import TowerType
from utils import Coord
from collections import deque


def build_instance_from_ascii(
    map_lines: List[str],
    tower_types: List[TowerType],
    budget: int,
) -> TDInstance:
    """
    Constrói uma TDInstance a partir de um mapa ASCII.

    Convenção:
      'X' -> bloqueado (não construível, não path)
      '.' -> construível
      'P' -> path
      'S' -> início do path (start)
      'E' -> fim do path (end)

    O path é obtido com um BFS de S até E, passando apenas por {P,S,E}.
    """
    if not map_lines:
        raise ValueError("Mapa vazio.")

    height = len(map_lines)
    width = len(map_lines[0])

    # garante retângulo
    for row in map_lines:
        if len(row) != width:
            raise ValueError("Todas as linhas do mapa devem ter o mesmo comprimento.")

    buildable_cells: List[Coord] = []
    walkable: Set[Coord] = set()
    start: Coord | None = None
    end: Coord | None = None

    # 1) varre o mapa
    for y, line in enumerate(map_lines):
        for x, ch in enumerate(line):
            pos = (x, y)
            if ch == '.':
                buildable_cells.append(pos)
            elif ch in ("P", "S", "E"):
                walkable.add(pos)
                if ch == "S":
                    start = pos
                elif ch == "E":
                    end = pos

    if start is None:
        raise ValueError("Mapa não possui 'S' (start).")
    if end is None:
        raise ValueError("Mapa não possui 'E' (end).")

    # 2) BFS de start até end
    q = deque([start])
    visited: Set[Coord] = {start}
    parent: Dict[Coord, Coord | None] = {start: None}

    found = False
    while q:
        cx, cy = cur = q.popleft()
        if cur == end:
            found = True
            break

        neighbors: List[Coord] = [
            (cx + 1, cy),
            (cx - 1, cy),
            (cx, cy + 1),
            (cx, cy - 1),
        ]
        for nb in neighbors:
            if nb in walkable and nb not in visited:
                visited.add(nb)
                parent[nb] = cur
                q.append(nb)

    if not found:
        raise ValueError("Não foi possível encontrar caminho de S até E usando tiles P/S/E.")

    # 3) reconstrói caminho end -> start
    path: List[Coord] = []
    cur: Coord | None = end
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()  # agora start -> end

    return TDInstance(
        width=width,
        height=height,
        buildable_cells=buildable_cells,
        path=path,
        tower_types=tower_types,
        budget=budget,
    )
def load_instance_from_txt(
    instance_id: int,
    tower_types: List[TowerType],
    base_dir: str = "instances",
) -> TDInstance:
    """
    Lê um arquivo 'instances/map<id>.txt' e monta uma TDInstance.
    Formato:
      primeira linha: 'BUDGET <int>'
      demais linhas: mapa ASCII
    """
    filename = f"map{instance_id}.txt"
    filepath = os.path.join(base_dir, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f if line.strip()]

    # primeira linha: budget
    header = lines[0]
    parts = header.split()
    if len(parts) != 2 or parts[0].upper() != "BUDGET":
        raise ValueError(f"Linha de cabeçalho inválida em {filepath}: '{header}'")

    budget = int(parts[1])
    map_lines = lines[1:]  # restante é o mapa

    return build_instance_from_ascii(
        map_lines=map_lines,
        tower_types=tower_types,
        budget=budget,
    )
