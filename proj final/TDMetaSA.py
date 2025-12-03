# TDMetaSA.py
import math
import random
from TDSolution import TDSolution


def generate_neighbor_td(instance, solution, rnd, max_trials=8):
    """
    Gera um vizinho viável a partir de uma TDSolution.
    - Representação: solution.assignments (lista com índices de torres ou -1)
    - Movimento: ou FLIP (trocar tipo de torre em uma célula) ou SWAP (trocar duas posições).
    - Garante viabilidade (custo <= budget).
    """
    num_cells = instance.num_buildable()
    num_types = len(instance.tower_types)

    for _ in range(max_trials):
        new_assignments = solution.assignments[:]  # cópia rasa da lista

        # Escolhe tipo de movimento
        if rnd.random() < 0.5:
            # FLIP: altera o tipo de torre em uma célula
            pos = rnd.randrange(num_cells)
            old = new_assignments[pos]
            candidates = [-1] + list(range(num_types))
            if old in candidates:
                candidates.remove(old)
            new_assignments[pos] = rnd.choice(candidates)
        else:
            # SWAP: troca duas posições da lista
            if num_cells < 2:
                continue
            i, j = rnd.sample(range(num_cells), 2)
            new_assignments[i], new_assignments[j] = new_assignments[j], new_assignments[i]

        candidate = TDSolution(new_assignments)
        if candidate.is_feasible(instance):
            return candidate

    # Se não achou vizinho viável em max_trials tentativas, retorna None
    return None


def simulated_annealing_td(instance, initial_solution, params, seed=None):
    """
    Simulated Annealing para o problema de Tower Defense.

    - instance: TDInstance
    - initial_solution: TDSolution já viável
    - params: dict com T0, alpha, SAmax, Tfinal, max_neighbor_trials
    - seed: semente opcional para reprodutibilidade
    """
    rnd = random.Random(seed)

    T0 = params.get("T0", 80.0)
    alpha = params.get("alpha", 0.90)
    SAmax = params.get("SAmax", 120)
    Tfinal = params.get("Tfinal", 1e-3)
    max_neighbor_trials = params.get("max_neighbor_trials", 8)

    # Clona solução inicial
    current = TDSolution(initial_solution.assignments[:])
    current_value = current.total_damage(instance)

    best = TDSolution(current.assignments[:])
    best_value = current_value

    print("\n===== SIMULATED ANNEALING (Tower Defense) =====")
    print(f"Solução inicial: custo {current.total_cost(instance)}/{instance.budget}, "
          f"dano = {current_value:.2f}")
    print(f"Parâmetros: T0={T0}, alpha={alpha}, SAmax={SAmax}, "
          f"Tfinal={Tfinal}, max_neighbor_trials={max_neighbor_trials}")

    T = T0
    iter_global = 0

    while T > Tfinal:
        iter_global += 1
        accepted = 0

        print(f"\n-- Temperatura {iter_global}: T = {T:.6f}")

        for it in range(SAmax):
            neighbor = generate_neighbor_td(
                instance, current, rnd, max_trials=max_neighbor_trials
            )
            if neighbor is None:
                # Não conseguiu vizinho viável nesta temperatura
                break

            neighbor_value = neighbor.total_damage(instance)
            delta = neighbor_value - current_value  # maximização

            if delta >= 0:
                # Melhorou ou empatou → aceita sempre
                accept = True
            else:
                # Piorou → aceita com probabilidade e^(delta / T)
                prob = math.exp(delta / T)
                x = rnd.random()
                accept = (x < prob)

            if accept:
                current = neighbor
                current_value = neighbor_value
                accepted += 1

                if current_value > best_value:
                    best = TDSolution(current.assignments[:])
                    best_value = current_value

        print(f"Vizinhos aceitos nesta temperatura: {accepted}/{SAmax}")
        print(f"Dano corrente: {current_value:.2f} | Melhor dano até agora: {best_value:.2f}")

        # Resfriamento
        T *= alpha

    print("\n===== FIM DO SA (Tower Defense) =====")
    print(f"Melhor dano encontrado: {best_value:.2f}")
    print(f"Custo da melhor solução: {best.total_cost(instance)}/{instance.budget}")
    print(f"Solução (assignments): {best.assignments}")

    return best
