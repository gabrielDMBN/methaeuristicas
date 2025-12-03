# TDMetaGRASP.py
import random
from typing import Dict

from TDSolution import TDSolution
from TDInstance import TDInstance


def greedy_randomized_construction(
    instance: TDInstance,
    alpha: float,
    rnd: random.Random,
    max_no_improve: int = 5,
) -> TDSolution:
    """
    Construção GRASP:
      - Começa com solução vazia (tudo -1).
      - Em cada passo, avalia os incrementos de dano de adicionar uma torre
        em uma célula construível, respeitando o budget.
      - Ordena candidatos pelo ganho de dano.
      - Monta uma RCL (Restricted Candidate List) contendo os 'top K'
        candidatos, onde K = max(1, int(alpha * len(candidates))).
      - Escolhe um candidato aleatoriamente da RCL e adiciona.
      - Para quando não há mais candidato viável ou não encontra melhorias.
    """
    num_cells = instance.num_buildable()
    num_types = len(instance.tower_types)

    # começa sem torres
    current = TDSolution([-1] * num_cells)
    current_value = current.total_damage(instance)

    no_improve = 0

    while True:
        candidates = []  # (gain, cell_index, tower_type)

        for i in range(num_cells):
            if current.assignments[i] != -1:
                # já tem torre aqui
                continue

            for t in range(num_types):
                new_assign = current.assignments[:]
                new_assign[i] = t
                cand = TDSolution(new_assign)

                if not cand.is_feasible(instance):
                    continue

                gain = cand.total_damage(instance) - current_value
                if gain > 0:
                    candidates.append((gain, i, t))

        if not candidates:
            break  # não há mais como melhorar pela construção

        # ordena por ganho decrescente
        candidates.sort(key=lambda x: x[0], reverse=True)

        # monta RCL com top-K candidatos
        k = max(1, int(alpha * len(candidates)))
        rcl = candidates[:k]

        # escolhe um candidato aleatório da RCL
        gain, i_chosen, t_chosen = rnd.choice(rcl)

        new_assign = current.assignments[:]
        new_assign[i_chosen] = t_chosen
        current = TDSolution(new_assign)
        current_value += gain
        no_improve = 0

        # critério extra de parada (opcional)
        if max_no_improve is not None:
            no_improve += 1
            if no_improve >= max_no_improve:
                break

    return current


def local_search_first_improvement(
    instance: TDInstance,
    initial_solution: TDSolution,
    max_iters: int,
    rnd: random.Random,
) -> TDSolution:
    """
    Busca local First Improvement:
      - Explora vizinhos alterando uma célula por vez (FLIP).
      - Assim que encontra um vizinho melhor (mais dano), move pra ele e recomeça.
      - Para quando nenhuma melhoria é encontrada ou atinge max_iters.
    """
    num_cells = instance.num_buildable()
    num_types = len(instance.tower_types)

    current = TDSolution(initial_solution.assignments[:])
    current_value = current.total_damage(instance)

    for _ in range(max_iters):
        improved = False

        indices = list(range(num_cells))
        rnd.shuffle(indices)

        for i in indices:
            old_type = current.assignments[i]
            candidates_types = [-1] + list(range(num_types))

            for t in candidates_types:
                if t == old_type:
                    continue

                new_assign = current.assignments[:]
                new_assign[i] = t
                cand = TDSolution(new_assign)

                if not cand.is_feasible(instance):
                    continue

                value = cand.total_damage(instance)
                if value > current_value:
                    current = cand
                    current_value = value
                    improved = True
                    break  # sai do loop de tipos

            if improved:
                break  # sai do loop de índices

        if not improved:
            break

    return current


def grasp_td(
    instance: TDInstance,
    params: Dict,
    seed: int | None = None,
) -> TDSolution:
    """
    GRASP + Local Search para Tower Defense.

    params:
      - max_iters: número de iterações GRASP
      - alpha: parâmetro da RCL na construção
      - ls_max_iters: iterações da busca local
    """
    rnd = random.Random(seed)

    max_iters = params.get("max_iters", 20)
    alpha = params.get("alpha", 0.3)
    ls_max_iters = params.get("ls_max_iters", 50)

    best_solution: TDSolution | None = None
    best_value: float = float("-inf")

    print("\n===== GRASP + LS (Tower Defense) =====")
    print(f"Parâmetros: max_iters={max_iters}, alpha={alpha}, ls_max_iters={ls_max_iters}, seed={seed}")

    for it in range(1, max_iters + 1):
        print(f"\n[GRASP] Iteração {it}/{max_iters}")

        # 1) Construção gulosa randomizada
        sol_constr = greedy_randomized_construction(instance, alpha, rnd)
        val_constr = sol_constr.total_damage(instance)
        print(f"  Construção: dano = {val_constr:.2f}, custo = {sol_constr.total_cost(instance)}/{instance.budget}")

        # 2) Busca local (First Improvement)
        sol_refined = local_search_first_improvement(instance, sol_constr, ls_max_iters, rnd)
        val_refined = sol_refined.total_damage(instance)
        print(f"  Pós-LS:     dano = {val_refined:.2f}, custo = {sol_refined.total_cost(instance)}/{instance.budget}")

        # 3) Atualiza melhor global
        if val_refined > best_value:
            best_value = val_refined
            best_solution = TDSolution(sol_refined.assignments[:])
            print("  >>> Atualizou melhor solução global!")

    print("\n===== FIM GRASP + LS (Tower Defense) =====")
    if best_solution is not None:
        print(f"Melhor dano encontrado: {best_value:.2f}")
        print(f"Custo da melhor solução: {best_solution.total_cost(instance)}/{instance.budget}")
        print(f"Solução (assignments): {best_solution.assignments}")
        return best_solution
    else:
        # fallback: nunca deveria acontecer se tiver buildable_cells
        print("Nenhuma solução construída, retornando solução vazia.")
        return TDSolution([-1] * instance.num_buildable())
