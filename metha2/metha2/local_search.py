from typing import List, Set, Tuple
from utils import solution_value, solution_weight

##ATIVIDADE 2 - BUSCA LOCAL -----------------------------------

# funcao auxiliar para busca local,retorna o conjunto de todas as dependências exigidas pelos pacotes selecionados.
def deps_of_solution(selected, pkg_deps):
    deps = set()
    for p in selected:
        deps |= pkg_deps[p]
    return deps

# funcao auxiliar para busca local, calcula a variação no peso total ao trocar p_out por p_in
def delta_cost_swap(p_out, p_in, selected, pkg_deps, a):
    # deps que ficam se remover p_out (somente as ainda necessárias)
    remaining = selected - {p_out}
    deps_after_remove = deps_of_solution(remaining, pkg_deps)
    # custo de adicionar p_in depois da remoção
    add_cost = sum(a[d] for d in (pkg_deps[p_in] - deps_after_remove))
    # “crédito” de remover p_out = quanto peso some?
    # É a diferença entre deps atuais e deps_after_remove
    current_deps = deps_of_solution(selected, pkg_deps)
    freed = current_deps - deps_after_remove
    remove_credit = sum(a[d] for d in freed)
    # delta total no peso
    return add_cost - remove_credit

#examinar vizinhanca flip e swap, escolhendo a melhor melhoria
def improve_by_flip_best(m, b, c, a, pkg_deps, current):
    best = current
    best_val = solution_value(current, c)
    current_deps = deps_of_solution(current, pkg_deps)
    current_w = sum(a[d] for d in current_deps)

    # tenta remover (sempre viável)
    for p in list(current):
        cand = set(current); cand.remove(p)
        val = solution_value(cand, c)
        if val > best_val and solution_weight(cand, pkg_deps, a) <= b:
            best, best_val = cand, val

    # tenta adicionar
    for p in range(m):
        if p in current: continue
        cost = sum(a[d] for d in (pkg_deps[p] - current_deps))
        if current_w + cost <= b:
            cand = set(current); cand.add(p)
            val = solution_value(cand, c)
            if val > best_val:
                best, best_val = cand, val

    return best, (best != current)

def improve_by_swap_best(m, b, c, a, pkg_deps, current):
    best = current
    best_val = solution_value(current, c)
    # percorre pares (p_out in current, p_in not in current)
    for p_out in list(current):
        for p_in in range(m):
            if p_in in current: continue
            delta = delta_cost_swap(p_out, p_in, current, pkg_deps, a)
            # checa capacidade
            if solution_weight(current, pkg_deps, a) + delta <= b:
                cand = set(current)
                cand.remove(p_out); cand.add(p_in)
                val = solution_value(cand, c)
                if val > best_val:
                    best, best_val = cand, val
    return best, (best != current)

#aplica busca local com vizinhança flip e swap, até ótimo local
def local_search_best_improvement(m, b, c, a, pkg_deps, initial_solution):
    current = set(initial_solution)
    while True:
        # tenta FLIP
        cand, changed = improve_by_flip_best(m, b, c, a, pkg_deps, current)
        if changed:
            current = cand
            continue
        # tenta SWAP
        cand, changed = improve_by_swap_best(m, b, c, a, pkg_deps, current)
        if changed:
            current = cand
            continue
        # sem melhora em nenhuma vizinhança → ótimo local
        break
    return current

def local_search_first_improvement(m, b, c, a, pkg_deps, initial_solution):
    current = set(initial_solution)

    while True:
        current_val = solution_value(current, c)
        current_w   = solution_weight(current, pkg_deps, a)

        improved = False

        # --- FLIP ---
        for p in range(m):
            cand = set(current)
            if p in cand:
                cand.remove(p)
            else:
                deps_now = deps_of_solution(cand, pkg_deps)
                cost = sum(a[d] for d in (pkg_deps[p] - deps_now))
                if current_w + cost > b:
                    continue
                cand.add(p)

            val = solution_value(cand, c)
            if val > current_val and solution_weight(cand, pkg_deps, a) <= b:
                current = cand
                improved = True
                break   # aceita a primeira melhora

        if improved:
            continue  # volta para while com nova solução

        # --- SWAP ---
        for p_out in list(current):
            for p_in in range(m):
                if p_in in current:
                    continue
                delta = delta_cost_swap(p_out, p_in, current, pkg_deps, a)
                if current_w + delta <= b:
                    cand = set(current)
                    cand.remove(p_out)
                    cand.add(p_in)
                    val = solution_value(cand, c)
                    if val > current_val:
                        current = cand
                        improved = True
                        break
            if improved:
                break

        if not improved:
            break  # nenhum vizinho melhora → ótimo local

    return current
