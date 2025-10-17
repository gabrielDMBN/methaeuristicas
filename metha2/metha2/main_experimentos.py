import random, time
from utils import read_instance, solution_value, log_experiment_detail, \
deps_of_solution, binaries_from_solution
from constructive import constructive_grasp
from local_search import local_search_first_improvement
from meta_sa import simulated_annealing


if __name__ == "__main__":
    path = "prob-software6.txt"
    #prob-software8 -> prob-software10 instancias da maratona (2,7,28 respectivamente)
    m, n, ne, b, c, a, pkg_deps = read_instance(path)
    print(f"Lido: m={m}, n={n}, ne={ne}, b={b}, instância: {path}")

    #=====Seeds=====
    run_seed = int(time.time())  # semente baseada no relógio
    #run_seed = 20251003 # semente definida
    random.seed(run_seed)

    # ========== META 1: GRASP + Local Search (First fit) ==========
    # GRASP
    start = time.time()
    val_grasp, pkgs_grasp = constructive_grasp(m, b, c, a, pkg_deps, iters=200, rcl_size=8, seed=run_seed)
    t_grasp = time.time() - start

    # Local Search (First)
    start = time.time()
    pkgs_ls = local_search_first_improvement(m, b, c, a, pkg_deps, pkgs_grasp)
    t_ls = time.time() - start

    val_ls = solution_value(pkgs_ls, c)
    deps_ls = deps_of_solution(pkgs_ls, pkg_deps)
    wt_ls  = sum(a[d] for d in deps_ls)

    pkgs_str, deps_str = binaries_from_solution(pkgs_ls, m, deps_ls, n)
    params_grasp_ls = {
        "grasp_iters": 200,
        "grasp_rcl_size": 8,
        "local_search": "first_improvement",
        "seed": run_seed
    }
    # (tempo total = GRASP + LS)
    log_experiment_detail("experimentos.txt", path, "GRASP+LS_FIRST",
                          best_value=val_ls,
                          total_weight=wt_ls,
                          pkgs_str=pkgs_str,
                          deps_str=deps_str,
                          params_dict=params_grasp_ls,
                          seed=run_seed,
                          elapsed_seconds=(t_grasp + t_ls))

    print(f"Local Search (First): valor {val_ls}, peso {wt_ls}/{b}, pacotes {len(pkgs_ls)}, tempo {(t_grasp+t_ls):.4f}s")

    # ========== META 2: Simulated Annealing (preset FAST)
    sa_params = {
        "T0": 80,
        "alpha": 0.90,
        "SAmax": 120,
        "Tfinal": 1e-3,
        "max_neighbor_trials": 8
    }
    start = time.time()
    val_sa, pkgs_sa = simulated_annealing(m, b, c, a, pkg_deps, pkgs_grasp,
                                          T0=sa_params["T0"],
                                          alpha=sa_params["alpha"],
                                          SAmax=sa_params["SAmax"],
                                          Tfinal=sa_params["Tfinal"],
                                          max_neighbor_trials=sa_params["max_neighbor_trials"],
                                          seed=run_seed)
    t_sa = time.time() - start

    deps_sa = deps_of_solution(pkgs_sa, pkg_deps)
    wt_sa   = sum(a[d] for d in deps_sa)
    pkgs_str, deps_str = binaries_from_solution(pkgs_sa, m, deps_sa, n)

    log_experiment_detail("experimentos.txt", path, "SA_FAST",
                          best_value=val_sa,
                          total_weight=wt_sa,
                          pkgs_str=pkgs_str,
                          deps_str=deps_str,
                          params_dict=sa_params,
                          seed=run_seed,
                          elapsed_seconds=t_sa)

    print(f"[SA-FAST] valor={val_sa} peso={wt_sa}/{b} pacotes={len(pkgs_sa)} tempo={t_sa:.4f}s")

    print("\nExecução concluída e salva em experimentos.txt")
