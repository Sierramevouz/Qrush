import csv
import time
import multiprocessing as mp
from core.rewrite_rules import generate_variants, is_rewritten
from core.ilp_scheduler import schedule_ilp
from core.equivalence import verify_equivalence


def estimate_swap_cost(gates, coupling_graph):
    if not coupling_graph:
        return 0
    from core.topology import compute_distance_matrix
    distances = compute_distance_matrix(coupling_graph)
    # 👇 去除 lambda，变成普通字典
    distances = {k: dict(v) for k, v in distances.items()}
    cost = 0
    for gate, qlist in gates:
        if gate == "cx" and len(qlist) == 2:
            q1, q2 = qlist
            if q1 in distances and q2 in distances[q1]:
                dist = distances[q1][q2]
                if dist > 1:
                    cost += dist - 1
    return cost


def _evaluate_variant(args):
    idx, variant, original_gates, num_qubits, coupling_graph, distance_matrix = args
    sched, depth = schedule_ilp(
        variant, num_qubits,
        coupling_graph=coupling_graph,
        distance_matrix=distance_matrix
    )
    if sched is None:
        return None
    equiv = verify_equivalence(original_gates, variant, num_qubits)
    if not equiv:
        return None
    rewritten = is_rewritten(original_gates, variant)
    swap_cost = estimate_swap_cost(variant, coupling_graph) if coupling_graph else 0

    return {
        "variant_id": idx,
        "depth": depth,
        "equiv": True,
        "rewritten": rewritten,
        "sched": sched,
        "gates": variant,
        "swap_cost": swap_cost
    }


def analyze_variants(gates, num_qubits,
                     csv_path=None,
                     coupling_graph=None,
                     distance_matrix=None,
                     use_parallel=True):
    start_time = time.time()

    variants = generate_variants(gates)
    best_result = None
    rows = []

    if distance_matrix is not None:
        # ✅ 解决 lambda 无法被多进程 pickle 的问题
        distance_matrix = {k: dict(v) for k, v in distance_matrix.items()}

    args_list = [
        (idx, variant, gates, num_qubits, coupling_graph, distance_matrix)
        for idx, variant in enumerate(variants)
    ]

    if use_parallel:
        cpu_count = mp.cpu_count()
        print(f"🚀 Analyzing {len(args_list)} variants with multiprocessing = True")
        print(f"🧵 Using {cpu_count} CPU cores")
        with mp.Pool(processes=cpu_count) as pool:
            results = pool.map(_evaluate_variant, args_list)
    else:
        print(f"🔍 Analyzing {len(args_list)} variants sequentially...")
        results = map(_evaluate_variant, args_list)

    for result in results:
        if result is None:
            continue

        rows.append({
            "variant_id": result["variant_id"],
            "depth": result["depth"],
            "equiv": result["equiv"],
            "rewritten": result["rewritten"],
        })

        if best_result is None or result["depth"] < best_result["depth"]:
            best_result = result

    # 输出 CSV（可选）
    if csv_path:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["variant_id", "depth", "equiv", "rewritten"])
            writer.writeheader()
            writer.writerows(rows)

    # 打印 top-k 简要统计
    print(f"\n📋 Found {len(rows)} valid rewrite variants")
    top_rows = sorted(rows, key=lambda r: r["depth"])[:100]
    for row in top_rows:
        tag = "🔁 Rewrite" if row["rewritten"] else "— Rewrite"
        print(f"  Variant {row['variant_id']:>3} | Depth: {row['depth']:>3} | ✅ Equiv | {tag}")

    if best_result:
        print(f"\n🥇 Best Variant = {best_result['variant_id']}, Depth = {best_result['depth']}, Rewritten = {best_result['rewritten']}")
        print(f"🔀 Estimated SWAP Cost (non-adjacent CX): {best_result['swap_cost']}")

    print(f"\n⏱️  Total time: {time.time() - start_time:.2f} seconds")

    return best_result
