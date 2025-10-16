import random, time
from utils import log_execution, read_instance, solution_weight, solution_value
from constructive import constructive_random, constructive_greedy, constructive_grasp
from local_search import local_search_best_improvement, local_search_first_improvement
from meta_sa import simulated_annealing

if __name__ == "__main__":
    path = "prob-software2.txt"
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
    # --- SA-FAST
    start = time.time()
    val_sa_fast, pkgs_sa_fast = simulated_annealing(
        m, b, c, a, pkg_deps, pkgs_grasp,
        T0=80,  # temperatura inicial moderada
        alpha=0.90,  # esfria mais rápido => menos níveis de T
        SAmax=120,  # menos iterações por temperatura
        Tfinal=1e-3,
        max_neighbor_trials=8
    )
    elapsed = time.time() - start
    wt = solution_weight(pkgs_sa_fast, pkg_deps, a)
    log_execution(run_id, "SA_FAST", val_sa_fast, wt, len(pkgs_sa_fast), b, elapsed)
    print(f"[SA-FAST] valor={val_sa_fast} peso={wt}/{b} pacotes={len(pkgs_sa_fast)} tempo={elapsed:.4f}s")

    # --- SA-QUALITY (tentativa com parametros mais rigidos)
    start = time.time()
    val_sa_q, pkgs_sa_q = simulated_annealing(
        m, b, c, a, pkg_deps, pkgs_grasp,
        T0=120,  # mais quente => aceita mais pioras no início
        alpha=0.95,  # esfria devagar => mais níveis de T
        SAmax=300,  # mais iterações por temperatura
        Tfinal=1e-3,
        max_neighbor_trials=12
    )
    elapsed = time.time() - start
    wt = solution_weight(pkgs_sa_q, pkg_deps, a)
    log_execution(run_id, "SA_QUALITY", val_sa_q, wt, len(pkgs_sa_q), b, elapsed)
    print(f"[SA-QUALITY] valor={val_sa_q} peso={wt}/{b} pacotes={len(pkgs_sa_q)} tempo={elapsed:.4f}s")

    print("\nExecução concluída e salva em resultados.txt")
