# main.py
import random

from TowerType import TowerType
from TDInstance import TDInstance
from TDSolution import TDSolution
from MapLoader import build_instance_from_ascii, load_instance_from_txt
from visualize import show_instance_grid, show_solution_grid
from TDMetaSA import simulated_annealing_td
from TDMetaGRASP import grasp_td

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
    # =================== SEED ===================
    seed = random.randint(0, 100000)
    print(f"Seed sorteada para esta execução: {seed}")
    rnd = random.Random(seed)

    # =================== INSTÂNCIA ===================
    tower_types = create_tower_types()

    instance_id = 6  # ajuste aqui para 1,2,3,... conforme seus arquivos
    instance = load_instance_from_txt(instance_id, tower_types)

    print(f"\nInstância {instance_id} carregada:")
    print(f"  Grid: {instance.width}x{instance.height}")
    print(f"  Buildable cells: {len(instance.buildable_cells)}")
    print(f"  Path length: {len(instance.path)}")
    print(f"  Budget: {instance.budget}\n")

    # Mapa inicial (sem torres)
    show_instance_grid(instance, title=f"Mapa Inicial - Instância {instance_id}")

    # =================== SOLUÇÃO INICIAL ===================
    init_sol = random_initial_solution(instance, rnd)
    print("Solução inicial (aleatória):")
    print(f"  Custo: {init_sol.total_cost(instance)}/{instance.budget}")
    print(f"  Dano : {init_sol.total_damage(instance):.2f}\n")

    # =================== META 1: SIMULATED ANNEALING ===================
    sa_params = {
        "T0": 80.0,
        "alpha": 0.90,
        "SAmax": 120,
        "Tfinal": 1e-3,
        "max_neighbor_trials": 8,
    }

    print("\n=== Rodando Simulated Annealing ===")
    best_sa = simulated_annealing_td(instance, init_sol, sa_params, seed=seed)

    print("\n=== Resultado SA ===")
    print(f"Melhor dano (SA): {best_sa.total_damage(instance):.2f}")
    print(f"Custo (SA):       {best_sa.total_cost(instance)}/{instance.budget}\n")

    # Mapa com torres escolhidas pelo SA
    show_solution_grid(
        instance,
        best_sa,
        title=f"Mapa com Torres (SA) - Instância {instance_id}"
    )

    # =================== META 2: GRASP + Local Search ===================
    grasp_params = {
        "max_iters": 20,
        "alpha": 0.3,
        "ls_max_iters": 50,
    }

    print("\n=== Rodando GRASP + Local Search ===")
    best_grasp = grasp_td(instance, grasp_params, seed=seed + 1)  # pode usar seed+1 pra variar

    print("\n=== Resultado GRASP+LS ===")
    print(f"Melhor dano (GRASP+LS): {best_grasp.total_damage(instance):.2f}")
    print(f"Custo (GRASP+LS):       {best_grasp.total_cost(instance)}/{instance.budget}\n")

    # Mapa com torres escolhidas pelo GRASP+LS
    show_solution_grid(
        instance,
        best_grasp,
        title=f"Mapa com Torres (GRASP+LS) - Instância {instance_id}"
    )


if __name__ == "__main__":
    main()