# utils.py
import math
from typing import Tuple
import os
import json

Coord = Tuple[int, int]  # (x, y)

def distance(a: Coord, b: Coord) -> float:
    """
    Distância Euclidiana entre duas células do grid.
    """
    (x1, y1), (x2, y2) = a, b
    return math.hypot(x1 - x2, y1 - y2)


def log_td_result(
    file_path: str,
    instance_label: str,
    method: str,
    seed: int,
    damage: float,
    cost: int,
    budget: int,
    num_towers: int,
    time_seconds: float,
    params: dict,
    assignments: list[int],
):
    """
    Escreve um bloco de resultado legível em arquivo TXT,
    com cara de "tabela", incluindo a solução (assignments).
    """

    # Garante que o arquivo existe
    if not os.path.exists(file_path):
        open(file_path, "w", encoding="utf-8").close()

    params_str = json.dumps(params, ensure_ascii=False)

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"Método...............: {method}\n")
        f.write(f"Instância............: {instance_label}\n")
        f.write(f"Semente (seed).......: {seed}\n")
        f.write(f"Melhor dano..........: {damage:.4f}\n")
        f.write(f"Custo / Budget.......: {cost} / {budget}\n")
        f.write(f"Número de torres.....: {num_towers}\n")
        f.write(f"Tempo de execução....: {time_seconds:.6f} s\n")
        f.write(f"Parâmetros...........: {params_str}\n")
        f.write(f"Solução (assignments): {assignments}\n")
        f.write("-" * 80 + "\n")