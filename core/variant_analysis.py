import csv
from core.rewrite_rules import generate_variants, is_rewritten
from core.ilp_scheduler import schedule_ilp
from core.equivalence import verify_equivalence

def estimate_swap_cost(gates, coupling_graph):
    if not coupling_graph:
        return 0
    from core.topology import compute_distance_matrix
    distances = compute_distance_matrix(coupling_graph)
    cost = 0
    for gate, qlist in gates:
        if gate == "cx" and len(qlist) == 2:
            q1, q2 = qlist
            dist = distances[q1][q2]
            if dist > 1:
                cost += dist - 1
    return cost


def analyze_variants(gates, num_qubits, csv_path=None, coupling_graph=None, distance_matrix=None):
    variants = generate_variants(gates)
    best_result = None
    rows = []

    for idx, variant in enumerate(variants):
        sched, depth = schedule_ilp(
            variant, num_qubits,
            coupling_graph=coupling_graph,
            distance_matrix=distance_matrix
        )
        if sched is None:
            continue
        equiv = verify_equivalence(gates, variant, num_qubits)
        if not equiv:
            continue

        rewritten = is_rewritten(gates, variant)
        rows.append({
            "variant_id": idx,
            "depth": depth,
            "equiv": True,
            "rewritten": rewritten,
        })

        swap_cost = estimate_swap_cost(variant, coupling_graph) if coupling_graph else 0

        if best_result is None or depth < best_result["depth"]:
            best_result = {
                "gates": variant,
                "sched": sched,
                "depth": depth,
                "variant_id": idx,
                "rewritten": rewritten,
                "swap_cost": swap_cost
            }


    # 输出 CSV 结果（可选）
    if csv_path:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["variant_id", "depth", "equiv", "rewritten"])
            writer.writeheader()
            writer.writerows(rows)

    # 打印 Top-K 统计
    print(f"\n📋 Found {len(rows)} valid rewrite variants")
    top_rows = sorted(rows, key=lambda r: r["depth"])[:100]
    for row in top_rows:
        tag = "🔁 Rewrite" if row["rewritten"] else "— Rewrite"
        print(f"  Variant {row['variant_id']:>3} | Depth: {row['depth']:>3} | ✅ Equiv | {tag}")

    if best_result:
        print(f"\n🥇 Best Variant = {best_result['variant_id']}, Depth = {best_result['depth']}, Rewritten = {best_result['rewritten']}")
    return best_result
