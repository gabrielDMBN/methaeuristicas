# main.py
import random

from TowerType import TowerType
from TDInstance import TDInstance
from TDSolution import TDSolution
from MapLoader import build_instance_from_ascii, load_instance_from_txt
from visualize import show_instance_grid, show_solution_grid
from TDMetaSA import simulated_annealing_td

# ============================================================
# Instância de teste simples
# ============================================================

def create_tower_types():
    return [
        TowerType(0, "Fraca", 20, 1.5, 5.0),
        TowerType(1, "Média", 35, 2.5, 8.0),
        TowerType(2, "Forte", 50, 3.5, 12.0),
    ]

# ============================================================
# Solução inicial aleatória
# ============================================================

def random_initial_solution(instance, rnd):
    num_cells = instance.num_buildable()
    num_types = len(instance.tower_types)

    assignments = [rnd.choice([-1] + list(range(num_types)))
                   for _ in range(num_cells)]

    sol = TDSolution(assignments)

    # Ajuste para caber no orçamento
    while not sol.is_feasible(instance):
        idxs = [i for i, t in enumerate(sol.assignments) if t != -1]
        if not idxs:
            break
        sol.assignments[rnd.choice(idxs)] = -1

    return sol

# ============================================================
# MAIN
# ============================================================

def main():
    seed = random.randint(0, 10000)
    rnd = random.Random(seed)

    tower_types = create_tower_types()

    instance_id = 6
    instance = load_instance_from_txt(instance_id, tower_types)

    print(f"Instância {instance_id} carregada:")
    print(f"  Grid: {instance.width}x{instance.height}")
    print(f"  Buildable cells: {len(instance.buildable_cells)}")
    print(f"  Path length: {len(instance.path)}")
    print(f"  Budget: {instance.budget}\n")

    show_instance_grid(instance, title=f"Mapa Inicial - Instância {instance_id}")

    init_sol = random_initial_solution(instance, rnd)
    print("Solução inicial:")
    print(f"  Custo: {init_sol.total_cost(instance)}/{instance.budget}")
    print(f"  Dano: {init_sol.total_damage(instance):.2f}")

    sa_params = {
        "T0": 80,
        "alpha": 0.95,
        "SAmax": 120,
        "Tfinal": 1e-3,
        "max_neighbor_trials": 8,
    }

    best = simulated_annealing_td(instance, init_sol, sa_params, seed=seed)
    print("\nMelhor dano (SA):", best.total_damage(instance))

    show_solution_grid(
        instance,
        best,
        title=f"Mapa com Torres (SA) - Instância {instance_id}"
    )


if __name__ == "__main__":
    main()