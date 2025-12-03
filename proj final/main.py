# main.py
import random
import time
from TowerType import TowerType
from TDInstance import TDInstance
from TDSolution import TDSolution
from MapLoader import build_instance_from_ascii, load_instance_from_txt
from visualize import show_instance_grid, show_solution_grid
from TDMetaSA import simulated_annealing_td
from TDMetaGRASP import grasp_td
from utils import log_td_result

RESULTS_FILE = "resultados_td.txt"

def create_tower_types():
    return [
        TowerType(0, "Fraca", 14, 3.5, 4),
        TowerType(1, "Média", 21, 3, 7),
        TowerType(2, "Forte", 23, 2, 15),
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
    seed = random.randint(0, 100000)  # ou defina um valor fixo para reprodutibilidade =====================================================================================
    print(f"Seed sorteada para esta execução: {seed}")
    rnd = random.Random(seed)

    # ===== Separador de execução no arquivo de resultados =====
    with open(RESULTS_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 80 + "\n")
        f.write(f"Nova execução | seed={seed}\n")
        f.write("=" * 80 + "\n\n")

    # =================== INSTÂNCIA ===================
    tower_types = create_tower_types()

    instance_id = 6  # ajuste aqui para 1,2,3 =========================================================================================================
    instance = load_instance_from_txt(instance_id, tower_types)

    instance_label = f"inst_{instance_id}"

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
    t0 = time.perf_counter()
    best_sa = simulated_annealing_td(instance, init_sol, sa_params, seed=seed)
    sa_time = time.perf_counter() - t0

    sa_damage = best_sa.total_damage(instance)
    sa_cost = best_sa.total_cost(instance)
    sa_towers = sum(1 for a in best_sa.assignments if a != -1)

    print("\n=== Resultado SA ===")
    print(f"Melhor dano (SA): {sa_damage:.2f}")
    print(f"Custo (SA):       {sa_cost}/{instance.budget}")
    print(f"Nº de torres (SA): {sa_towers}")
    print(f"Tempo (SA):        {sa_time:.4f} s\n")

    # Log em arquivo (SA)
    log_td_result(
        RESULTS_FILE,
        instance_label=instance_label,
        method="SA",
        seed=seed,
        damage=sa_damage,
        cost=sa_cost,
        budget=instance.budget,
        num_towers=sa_towers,
        time_seconds=sa_time,
        params=sa_params,
        assignments=best_sa.assignments,
    )

    # Mapa com torres escolhidas pelo SA
    show_solution_grid(
        instance,
        best_sa,
        title=f"Mapa com Torres (SA) - Instância {instance_id}"
    )

    # =================== META 2: GRASP + Local Search ===================
    num_cells = instance.num_buildable() # verifica tamanho da instância para ajustar parâmetros do GRASP
    if num_cells <= 40:
        grasp_params = {"max_iters": 20, "alpha": 0.3, "ls_max_iters": 50}
    elif num_cells <= 80:
        grasp_params = {"max_iters": 10, "alpha": 0.3, "ls_max_iters": 25}
    else:
        grasp_params = {"max_iters": 6, "alpha": 0.3, "ls_max_iters": 12}

    grasp_params = {"max_iters": 10, "alpha": 0.3, "ls_max_iters": 25} # ajuste fixo para teste =====================================================================================

    print("\n=== Rodando GRASP + Local Search ===")
    t0 = time.perf_counter()
    best_grasp = grasp_td(instance, grasp_params, seed=seed)  # seed
    grasp_time = time.perf_counter() - t0

    grasp_damage = best_grasp.total_damage(instance)
    grasp_cost = best_grasp.total_cost(instance)
    grasp_towers = sum(1 for a in best_grasp.assignments if a != -1)

    print("\n=== Resultado GRASP+LS ===")
    print(f"Melhor dano (GRASP+LS): {grasp_damage:.2f}")
    print(f"Custo (GRASP+LS):       {grasp_cost}/{instance.budget}")
    print(f"Nº de torres (GRASP+LS): {grasp_towers}")
    print(f"Tempo (GRASP+LS):        {grasp_time:.4f} s\n")

    # Log em arquivo (GRASP+LS)
    log_td_result(
        RESULTS_FILE,
        instance_label=instance_label,
        method="GRASP+LS",
        seed=seed,
        damage=grasp_damage,
        cost=grasp_cost,
        budget=instance.budget,
        num_towers=grasp_towers,
        time_seconds=grasp_time,
        params=grasp_params,
        assignments=best_grasp.assignments,
    )

    # Mapa com torres escolhidas pelo GRASP+LS
    show_solution_grid(
        instance,
        best_grasp,
        title=f"Mapa com Torres (GRASP+LS) - Instância {instance_id}"
    )

if __name__ == "__main__":
    main()