# visualize.py
from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from TDInstance import TDInstance
from TDSolution import TDSolution

Coord = Tuple[int, int]


def build_grid_matrix(instance: TDInstance) -> np.ndarray:
    """
    Códigos:
      0 = não construível (cinza)
      1 = construível (branco)
      2 = path normal (preto)
      3 = início (start) - verde
      4 = fim (end) - vermelho
      5 = torre tipo 0 (azul)
      6 = torre tipo 1 (roxa)
      7 = torre tipo 2 (amarela)
    """
    h, w = instance.height, instance.width
    grid = np.zeros((h, w), dtype=int)  # default: 0 (cinza)

    # 1) Construíveis (.)
    for (x, y) in instance.buildable_cells:
        grid[y, x] = 1

    # 2) Path inteiro como preto (2)
    for (x, y) in instance.path:
        grid[y, x] = 2

    # 3) Start e End, se existirem
    if instance.path:
        sx, sy = instance.path[0]
        ex, ey = instance.path[-1]
        grid[sy, sx] = 3  # verde
        grid[ey, ex] = 4  # vermelho

    return grid


# colormap fixo e alinhado com os códigos acima
_CMAP = ListedColormap([
    "#808080",  # 0 cinza  (não construível)
    "#FFFFFF",  # 1 branco (construível)
    "#000000",  # 2 preto  (path)
    "#00FF00",  # 3 verde  (start)
    "#FF0000",  # 4 vermelho (end)
    "#0000FF",  # 5 azul   (tower 0)
    "#800080",  # 6 roxo   (tower 1)
    "#FFFF00",  # 7 amarelo (tower 2)
])


def _show_grid(grid: np.ndarray, instance: TDInstance, title: str):
    plt.figure(figsize=(8, 4))
    plt.imshow(
        grid,
        cmap=_CMAP,
        origin="lower",
        aspect="equal",
        vmin=0,
        vmax=_CMAP.N - 1,   # garante 0→cor0, 1→cor1, ..., 7→cor7
    )

    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")

    plt.xticks(range(instance.width))
    plt.yticks(range(instance.height))

    ax = plt.gca()
    for x in range(instance.width + 1):
        ax.axvline(x - 0.5, color="k", linewidth=0.5)
    for y in range(instance.height + 1):
        ax.axhline(y - 0.5, color="k", linewidth=0.5)

    plt.tight_layout()
    plt.show()


def show_instance_grid(instance: TDInstance, title: str = "Mapa Tower Defense"):
    """
    Mostra apenas o mapa (sem torres).
    """
    grid = build_grid_matrix(instance)
    _show_grid(grid, instance, title)


def show_solution_grid(instance: TDInstance, solution: TDSolution,
                       title: str = "Mapa com Torres"):
    """
    Mostra o mapa + posição das torres:
      tipo 0 -> azul //fraco
      tipo 1 -> roxa //medio
      tipo 2 -> amarela //forte
    """
    grid = build_grid_matrix(instance)

    for idx, tower_id in enumerate(solution.assignments):
        if tower_id == -1:
            continue  # sem torre nesse tile

        x, y = instance.buildable_cells[idx]

        if tower_id == 0:
            code = 5  # azul
        elif tower_id == 1:
            code = 6  # roxo
        elif tower_id == 2:
            code = 7  # amarelo
        else:
            # fallback, se por acaso tiver mais tipos
            code = 5 + (tower_id % 3)

        grid[y, x] = code

    _show_grid(grid, instance, title)
