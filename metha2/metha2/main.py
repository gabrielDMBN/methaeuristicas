import time
from utils import log_execution, read_instance, solution_weight, solution_value
from constructive import constructive_random, constructive_greedy, constructive_grasp
from local_search import local_search_best_improvement, local_search_first_improvement
from meta_sa import simulated_annealing

if __name__ == "__main__":
    path = "prob-software7.txt"
    #teste

    m, n, ne, b, c, a, pkg_deps = read_instance(path)
    print(f"Lido: m={m}, n={n}, ne={ne}, b={b}, instância: {path}" )

    run_id = 3  ################################## incrementar para mudar id individualmente de cada execução

    # RANDOM
    start = time.time()
    val_rnd, pkgs_rnd = constructive_random(m, b, c, a, pkg_deps, restarts=200, seed=None)
    elapsed = time.time() - start
    wt_rnd = solution_weight(pkgs_rnd, pkg_deps, a)
    log_execution(run_id, "RANDOM", val_rnd, wt_rnd, len(pkgs_rnd), b, elapsed)
    print(f"Random: valor {val_rnd}, peso {wt_rnd}/{b}, pacotes {len(pkgs_rnd)}, tempo {elapsed:.4f}s")

    # GREEDY
    start = time.time()
    val_gre, pkgs_gre = constructive_greedy(m, b, c, a, pkg_deps)
    elapsed = time.time() - start
    wt_gre = solution_weight(pkgs_gre, pkg_deps, a)
    log_execution(run_id, "GREEDY", val_gre, wt_gre, len(pkgs_gre), b, elapsed)
    print(f"Greedy: valor {val_gre}, peso {wt_gre}/{b}, pacotes {len(pkgs_gre)}, tempo {elapsed:.4f}s")

    # GRASP
    start = time.time()
    val_grasp, pkgs_grasp = constructive_grasp(m, b, c, a, pkg_deps, iters=200, rcl_size=8, seed=None)
    elapsed = time.time() - start
    wt_grasp = solution_weight(pkgs_grasp, pkg_deps, a)
    log_execution(run_id, "GRASP", val_grasp, wt_grasp, len(pkgs_grasp), b, elapsed)
    print(f"GRASP: valor {val_grasp}, peso {wt_grasp}/{b}, pacotes {len(pkgs_grasp)}, tempo {elapsed:.4f}s")

    # ATIVIDADE 2 - BUSCA LOCAL ------------------------------
    # ATIVIDADE 3 - METHAEURISTICA GRASP + Local Search------------------------------
    start = time.time()
    refined = local_search_best_improvement(m, b, c, a, pkg_deps, pkgs_grasp)
    elapsed = time.time() - start
    val_refined = solution_value(refined, c)
    wt_refined = solution_weight(refined, pkg_deps, a)
    log_execution(run_id, "LOCAL_BEST", val_refined, wt_refined, len(refined), b, elapsed)
    print(
        f"Local Search (Best): valor {val_refined}, peso {wt_refined}/{b}, pacotes {len(refined)}, tempo {elapsed:.4f}s")

    start = time.time()
    refined = local_search_first_improvement(m, b, c, a, pkg_deps, pkgs_grasp)
    elapsed = time.time() - start
    val_refined = solution_value(refined, c)
    wt_refined = solution_weight(refined, pkg_deps, a)
    log_execution(run_id, "LOCAL_FIRST", val_refined, wt_refined, len(refined), b, elapsed)
    print(
        f"Local Search (First): valor {val_refined}, peso {wt_refined}/{b}, pacotes {len(refined)}, tempo {elapsed:.4f}s")

    # -------------------------------------------------
    # META-HEURÍSTICA 2: SIMULATED ANNEALING
    # -------------------------------------------------
    start = time.time()
    val_sa, pkgs_sa = simulated_annealing(
        m, b, c, a, pkg_deps, pkgs_grasp,
        T0=100.0,  # fixa T0 (evita calibrar e garante finalizar)
        alpha=0.97,  # resfriamento geométrico
        SAmax=400,  # iterações por temperatura
        Tfinal=1e-3,  # temperatura final
        max_neighbor_trials=10  # evita travar tentando vizinhos inviáveis
    )
    elapsed = time.time() - start
    wt_sa = solution_weight(pkgs_sa, pkg_deps, a)
    log_execution(run_id, "SIMULATED_ANNEALING", val_sa, wt_sa, len(pkgs_sa), b, elapsed)
    print(f"SIMULATED_ANNEALING valor={val_sa} peso={wt_sa}/{b} pacotes={len(pkgs_sa)} tempo={elapsed:.4f}s")
    #-------------------------------------------------------------

    print("\nExecução concluída e salva em resultados.txt")
