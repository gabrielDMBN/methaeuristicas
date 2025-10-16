import random, time,json
from typing import List, Set, Tuple

#funcao para salvamento de metricas
def log_execution(run_id: int, method: str, value: int, weight: int, num_pkgs: int, capacity: int, elapsed: float, filename="resultados.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{run_id};{method};{value};{weight}/{capacity};{num_pkgs};{elapsed:.4f}\n")

def read_instance(path: str):
    with open(path, "r", encoding="utf-8") as f:
        # 1 m, n, ne, b
        m, n, ne, b = map(int, f.readline().split())
        #2 beneficios c (m)
        c = list(map(int, f.readline().split()))
     #   assert len(c) == m, f"Esperava {m} benefícios, veio {len(c)}" #debug
        # 3 tamanhos a (n)
        a = list(map(int, f.readline().split()))
       # assert len(a) == n, f"Esperava {n} tamanhos, veio {len(a)}" #debug
        # 4 ne linhas pacote dependencia (0-based)
        pkg_deps = [set() for _ in range(m)]
        for _ in range(ne):
            p, d = map(int, f.readline().split())
            pkg_deps[p].add(d)
    return m, n, ne, b, c, a, pkg_deps

def marginal_cost(pkg: int, chosen_deps: Set[int], pkg_deps: List[Set[int]], a: List[int]) -> int:
    new_deps = pkg_deps[pkg] - chosen_deps
    return sum(a[d] for d in new_deps)

def solution_value(chosen_pkgs: Set[int], c: List[int]) -> int:
    return sum(c[p] for p in chosen_pkgs)

def solution_weight(chosen_pkgs: Set[int], pkg_deps: List[Set[int]], a: List[int]) -> int:
    deps = set()
    for p in chosen_pkgs:
        deps |= pkg_deps[p]
    return sum(a[d] for d in deps)

def deps_of_solution(selected, pkg_deps):
    deps = set()
    for p in selected:
        deps |= pkg_deps[p]
    return deps

def binaries_from_solution(selected_pkgs, m, selected_deps, n):
    pkgs_bin = [0]*m
    for p in selected_pkgs:
        pkgs_bin[p] = 1
    deps_bin = [0]*n
    for d in selected_deps:
        deps_bin[d] = 1
    # strings no formato pedido: "[0, 1, 0, ...]"
    pkgs_str = "[" + ", ".join(map(str, pkgs_bin)) + "]"
    deps_str = "[" + ", ".join(map(str, deps_bin)) + "]"
    return pkgs_str, deps_str

def log_experiment_detail(filename, instance_path, method_name, best_value, total_weight,
                          pkgs_str, deps_str, params_dict, seed, elapsed_seconds):
    """
    Salva um bloco de experimento contendo:
      - caminho da instância
      - método (meta-heurística)
      - melhor valor
      - peso total (MB)
      - solução binária (pacotes / dependências)
      - parâmetros usados
      - semente aleatória
      - tempo em segundos
    """
    with open(filename, "a", encoding="utf-8") as f:
        f.write("========================================\n")
        f.write(f"instance_path: {instance_path}\n")
        f.write(f"method: {method_name}\n")
        f.write(f"best_value: {best_value}\n")
        f.write(f"total_weight: {total_weight}\n")
        f.write("packages_binary: " + pkgs_str + "\n")
        f.write("dependencies_binary: " + deps_str + "\n")
        f.write("params: " + json.dumps(params_dict, ensure_ascii=False) + "\n")
        f.write(f"seed: {seed}\n")
        f.write(f"time_seconds: {elapsed_seconds:.6f}\n")
