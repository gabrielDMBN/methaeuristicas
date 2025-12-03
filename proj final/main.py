# main.py
import random

from TowerType import TowerType
from TDInstance import TDInstance
from TDSolution import TDSolution
from MapLoader import build_instance_from_ascii
from visualize import show_instance_grid

# ============================================================
# Instância de teste simples
# ============================================================

def create_instance_from_ascii() -> TDInstance:
    # Mapa ASCII: primeira linha = y=0 (baixo)
    ascii_map = [
        "XXXXXXXXXX",
        "X........X",
        "X.SPPPP.EX",
        "X........X",
        "XXXXXXXXXX",
    ]

    tower_types = [
        TowerType(0, "Fraca", 20, 1.5, 5.0),
        TowerType(1, "Média", 35, 2.5, 8.0),
        TowerType(2, "Forte", 50, 3.5, 12.0),
    ]

    budget = 200

    instance = build_instance_from_ascii(
        map_lines=ascii_map,
        tower_types=tower_types,
        budget=budget,
    )
    return instance


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
# Hill-Climb simples
# ============================================================

def hill_climb(instance, sol, iters=30, seed=0):
    rnd = random.Random(seed)

    current = TDSolution(sol.assignments[:])
    current_value = current.total_damage(instance)

    print("\n===== HILL CLIMB =====")
    print(f"Inicial -> custo {current.total_cost(instance)}/{instance.budget} | dano {current_value:.2f}")

    for it in range(1, iters + 1):
        pos = rnd.randrange(instance.num_buildable())
        old = current.assignments[pos]

        num_types = len(instance.tower_types)
        candidates = [-1] + list(range(num_types))
        candidates.remove(old)
        new = rnd.choice(candidates)

        candidate = TDSolution(current.assignments[:])
        candidate.assignments[pos] = new

        new_value = candidate.total_damage(instance)

        print(f"[Iter {it}] Mudando célula {pos}: {old} → {new}")
        print(f"    dano atual = {current_value:.2f} | dano vizinho = {new_value:.2f}")

        if new_value > current_value:
            print("    Aceitou!")
            current = candidate
            current_value = new_value
        else:
            print("    Rejeitou.")

    print("\n=== FINAL ===")
    print(f"Dano final: {current_value:.2f}")
    print(f"Custo final: {current.total_cost(instance)}/{instance.budget}")
    print(f"Solução: {current.assignments}")

    return current


# ============================================================
# MAIN
# ============================================================

def main():
    instance = create_instance_from_ascii()

    print("Instância carregada:")
    print(f"  Grid: {instance.width}x{instance.height}")
    print(f"  Buildable cells: {len(instance.buildable_cells)}")
    print(f"  Path length: {len(instance.path)}")
    print(f"  Path (primeiros 10): {instance.path[:10]}")
    print(f"  Tipos de torres: {len(instance.tower_types)}")
    print(f"  Budget: {instance.budget}\n")

    # Visualização
    show_instance_grid(instance, title="Mapa Tower Defense - ASCII")

    # resto do código igual: solução aleatória, hill-climb, etc.
    seed = 42 #
    rnd = random.Random(seed)

    from main import random_initial_solution, hill_climb  # se estiver em outro módulo, ajustar

    init_sol = random_initial_solution(instance, rnd)
    print("Solução inicial:")
    print(f"  Assignments: {init_sol.assignments}")
    print(f"  Custo: {init_sol.total_cost(instance)}/{instance.budget}")
    print(f"  Dano: {init_sol.total_damage(instance):.2f}")

    hill_climb(instance, init_sol, iters=40, seed=seed)


if __name__ == "__main__":
    main()