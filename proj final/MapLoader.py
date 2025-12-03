# MapLoader.py
from typing import List, Tuple, Set

from TDInstance import TDInstance
from TowerType import TowerType
from utils import Coord


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
      'S' -> início do path (start, também conta como path)
      'E' -> fim do path (end, também conta como path)

    O path é ordenado automaticamente percorrendo vizinhos 4-direcionais
    a partir de 'S' até chegar em 'E'.
    """
    if not map_lines:
        raise ValueError("Mapa vazio.")

    height = len(map_lines)
    width = len(map_lines[0])

    # Garante que todas as linhas têm o mesmo comprimento
    for row in map_lines:
        if len(row) != width:
            raise ValueError("Todas as linhas do mapa devem ter o mesmo comprimento.")

    buildable_cells: List[Coord] = []
    path_cells: Set[Coord] = set()
    start: Coord | None = None

    # 1) Identifica construíveis, path, e start
    for y, line in enumerate(map_lines):
        for x, ch in enumerate(line):
            pos = (x, y)
            if ch == '.':
                buildable_cells.append(pos)
            elif ch in ("P", "S", "E"):
                path_cells.add(pos)
                if ch == "S":
                    start = pos

    if not path_cells:
        raise ValueError("Mapa não possui nenhum tile de path ('P', 'S' ou 'E').")

    # Se não tiver 'S', escolhe qualquer path como início (não é o ideal, mas evita crash)
    if start is None:
        start = next(iter(path_cells))

    # 2) Constrói caminho ordenado a partir de 'start'
    path: List[Coord] = []
    visited: Set[Coord] = set()

    current = start
    previous: Coord | None = None

    while True:
        path.append(current)
        visited.add(current)

        x, y = current
        ch_here = map_lines[y][x]

        # Se chegou em 'E', encerra path aqui
        if ch_here == "E":
            break

        # Vizinhos 4-direcionais
        neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]

        next_cell: Coord | None = None
        for nb in neighbors:
            if nb in path_cells and nb not in visited:
                next_cell = nb
                break

        if next_cell is None:
            # Caminho "morreu" sem chegar em 'E' → encerra mesmo assim
            break

        previous = current
        current = next_cell

    return TDInstance(
        width=width,
        height=height,
        buildable_cells=buildable_cells,
        path=path,
        tower_types=tower_types,
        budget=budget,
    )
