import random
import time
from typing import List, Set, Tuple
from utils import marginal_cost, solution_value, solution_weight

#1 funcao de construcao aleatoria
def constructive_random(m, b, c, a, pkg_deps, restarts=50, seed=None):
    rng = random.Random() if seed is None else random.Random(seed)
    best = (0, set())     # (valor,pacotes)
    for _ in range(restarts):
        order = list(range(m))
        rng.shuffle(order)
        chosen_pkgs = set()
        chosen_deps = set()
        used = 0
        for p in order:
            cost = marginal_cost(p, chosen_deps, pkg_deps, a)
            if used + cost <= b:
                chosen_pkgs.add(p)
                #atualiza dependências e peso
                new_deps = pkg_deps[p] - chosen_deps
                chosen_deps |= new_deps
                used += sum(a[d] for d in new_deps)
        val = solution_value(chosen_pkgs, c)
        if val > best[0]:
            best = (val, chosen_pkgs)
    return best

# 2 guloso ( utilizando a razao; razão benefício / custo marginal)
def constructive_greedy(m, b, c, a, pkg_deps):
    chosen_pkgs = set()
    chosen_deps = set()
    used = 0
    remaining = set(range(m))
    while True:
        best_p = None
        best_score = -1
        best_cost = None
        for p in remaining:
            cost = marginal_cost(p, chosen_deps, pkg_deps, a)
            if cost <= 0:
                # se todas deps já presentes ,escolha imediata
                best_p = p
                best_cost = 0
                best_score = float('inf')
                break
            if used + cost <= b:
                score = c[p] / cost
                if score > best_score:
                    best_score = score
                    best_cost = cost
                    best_p = p
        if best_p is None:
            break
        # add pacote
        chosen_pkgs.add(best_p)
        new_deps = pkg_deps[best_p] - chosen_deps
        chosen_deps |= new_deps
        used += sum(a[d] for d in new_deps)
        remaining.remove(best_p)
    return solution_value(chosen_pkgs, c), chosen_pkgs

# 3 Guloso random (com Rcl)
def constructive_grasp(m, b, c, a, pkg_deps, iters=50, rcl_size=10, seed=123):
    rng = random.Random(time.time() if seed is None else seed)
    best = (0, set())
    for _ in range(iters):
        chosen_pkgs = set()
        chosen_deps = set()
        used = 0
        remaining = set(range(m))
        while True:
            # calcula razões marginais para candidatos que cabem
            scored: List[Tuple[float, int, int]] = []  # (score, p, cost)
            for p in remaining:
                cost = marginal_cost(p, chosen_deps, pkg_deps, a)
                if cost <= 0:
                    scored.append((float('inf'), p, 0))
                elif used + cost <= b:
                    scored.append((c[p]/cost, p, cost))
            if not scored:
                break
            scored.sort(reverse=True, key=lambda x: x[0])
            # rcl = top k (candidatos restritos sao colocados em uma lista com o objetivo de utilizar a abordagem hibrida de guloso e aleatorio)
            rcl = scored[:max(1, min(rcl_size, len(scored)))]
            # escolhe aleatoriamente da rCL
            _, p, cost = rng.choice(rcl)
            chosen_pkgs.add(p)
            new_deps = pkg_deps[p] - chosen_deps
            chosen_deps |= new_deps
            used += sum(a[d] for d in new_deps)
            remaining.remove(p)
        val = solution_value(chosen_pkgs, c)
        if val > best[0]:
            best = (val, chosen_pkgs)
    return best
