# visualize.py
from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from TDInstance import TDInstance

Coord = Tuple[int, int]


def build_grid_matrix(instance: TDInstance) -> np.ndarray:
    """
    Códigos:
      0 = não construível (cinza)
      1 = construível (branco)
      2 = path normal (preto)
      3 = início (start) - verde
      4 = fim (end) - vermelho
    """
    h, w = instance.height, instance.width
    grid = np.zeros((h, w), dtype=int)

    # construíveis
    for (x, y) in instance.buildable_cells:
        grid[y, x] = 1

    # path normal
    for (x, y) in instance.path:
        grid[y, x] = 2

    # start e end, se existir path
    if instance.path:
        sx, sy = instance.path[0]
        ex, ey = instance.path[-1]
        grid[sy, sx] = 3  # start verde
        grid[ey, ex] = 4  # end vermelho

    return grid


def show_instance_grid(instance: TDInstance, title: str = "Mapa Tower Defense"):
    grid = build_grid_matrix(instance)

    # 0 cinza, 1 branco, 2 preto, 3 verde, 4 vermelho
    cmap = ListedColormap([
        "0.6",    # 0 não construível
        "1.0",    # 1 construível
        "0.0",    # 2 path
        "lime",   # 3 start
        "red"     # 4 end
    ])

    plt.figure(figsize=(8, 4))
    plt.imshow(grid, cmap=cmap, origin="lower", aspect="equal")

    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")

    # ticks no centro de cada célula
    plt.xticks(range(instance.width))
    plt.yticks(range(instance.height))

    # desenha grade 1:1
    ax = plt.gca()
    for x in range(instance.width + 1):
        ax.axvline(x - 0.5, color="k", linewidth=0.5)
    for y in range(instance.height + 1):
        ax.axhline(y - 0.5, color="k", linewidth=0.5)

    plt.tight_layout()
    plt.show()
