import math, random
from utils import solution_value, solution_weight
from local_search import deps_of_solution, delta_cost_swap

def sa_temperature_initial(m, b, c, a, pkg_deps, s_init,
                           SAmax=200, T0=1.0, gamma=0.95, beta=2.0,
                           max_levels=50, max_neighbor_trials=5, fallback_T0=100.0, seed=None):

    rng = random.Random() if seed is None else random.Random(seed)

    T = T0
    level = 0
    while level < max_levels:
        accepted = 0
        s = set(s_init)
        f_s = solution_value(s, c)

        it = 0
        while it < SAmax:
            # tenta gerar um vizinho viável em poucas tentativas
            trials = 0
            s2 = None
            while trials < max_neighbor_trials and s2 is None:
                p = rng.randrange(m)
                cand = set(s)
                if p in cand:
                    cand.remove(p)  # remover sempre viável
                else:
                    deps_now = deps_of_solution(cand, pkg_deps)
                    add_cost = sum(a[d] for d in (pkg_deps[p] - deps_now))
                    if solution_weight(cand, pkg_deps, a) + add_cost > b:
                        trials += 1
                        continue
                    cand.add(p)
                s2 = cand

            if s2 is None:  # não conseguiu vizinho viável -> conta iteração e segue
                it += 1
                continue

            f_s2 = solution_value(s2, c)
            delta = f_s2 - f_s  # maximização

            # aceita (Metrópolis)
            if delta > 0 or rng.random() < math.exp(delta / T):
                accepted += 1
                s, f_s = s2, f_s2

            it += 1

        # taxa de aceitação atingiu gamma? ótimo.
        if accepted >= gamma * SAmax:
            return T

        # senão, aumenta T e tenta de novo
        T *= beta
        level += 1

    # se não alcançou gamma dentro do limite, usa fallback
    return fallback_T0

# ---------- SA principal (maximização), com resfriamento geométrico ----------
def simulated_annealing(m, b, c, a, pkg_deps, initial_solution,
                        T0=None, alpha=0.97, SAmax=400, Tfinal=1e-3,
                        max_neighbor_trials=10, seed=None):

    rng = random.Random() if seed is None else random.Random(seed)

    if T0 is None:
        T0 = sa_temperature_initial(m, b, c, a, pkg_deps, initial_solution,
                                    SAmax=min(200, SAmax), T0=1.0, gamma=0.95, beta=2.0,
                                    max_levels=50, max_neighbor_trials=5, fallback_T0=100.0)
    T = T0

    current = set(initial_solution)
    f_cur = solution_value(current, c)
    best = set(current); f_best = f_cur

    while T > Tfinal:
        it = 0
        while it < SAmax:
            # tenta achar vizinho viável (flip 60% / swap 40%)
            trials = 0
            s2 = None
            while trials < max_neighbor_trials and s2 is None:
                if rng.random() < 0.6 or not current:
                    # FLIP
                    p = rng.randrange(m)
                    cand = set(current)
                    if p in cand:
                        cand.remove(p)
                    else:
                        deps_now = deps_of_solution(cand, pkg_deps)
                        add_cost = sum(a[d] for d in (pkg_deps[p] - deps_now))
                        if solution_weight(cand, pkg_deps, a) + add_cost > b:
                            trials += 1
                            continue
                        cand.add(p)
                    s2 = cand
                else:
                    # SWAP
                    p_out = rng.choice(tuple(current))
                    p_in = rng.randrange(m)
                    if p_in in current:
                        trials += 1
                        continue
                    delta_w = delta_cost_swap(p_out, p_in, current, pkg_deps, a)
                    if solution_weight(current, pkg_deps, a) + delta_w > b:
                        trials += 1
                        continue
                    cand = set(current); cand.remove(p_out); cand.add(p_in)
                    s2 = cand

            # se não achou vizinho viável, só avança a iteração
            if s2 is None:
                it += 1
                continue

            f_s2 = solution_value(s2, c)
            delta = f_s2 - f_cur  # MAX

            # aceita (Metrópolis)
            if delta > 0 or rng.random() < math.exp(delta / T):
                current, f_cur = s2, f_s2
                if f_cur > f_best:
                    best, f_best = set(current), f_cur

            it += 1

        T *= alpha  # resfriamento geométrico

    return f_best, best