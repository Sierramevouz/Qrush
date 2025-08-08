from core.ilp_scheduler import schedule_ilp, safe
from core.rewrite_rules import apply_rewrite_once, hash_gate_list
from core.equivalence import verify_equivalence

# 多步 rewrite 搜索（BFS + beam search）
def bfs_rewrite_search(gates, num_qubits=3, max_depth=3, beam_width=5):
    visited = set()
    beam = [{"gates": gates, "depth": 0, "sched": None, "score": float("inf")}]
    visited.add(hash_gate_list(gates))
    best_result = None

    for level in range(max_depth):
        candidates = []
        for item in beam:
            curr = item["gates"]
            children = apply_rewrite_once(curr)
            for child in children:
                h = hash_gate_list(child)
                if h in visited:
                    continue
                visited.add(h)
                sched, depth = schedule_ilp(child, num_qubits)
                if sched is None:
                    continue
                candidates.append({
                    "gates": child,
                    "depth": level + 1,
                    "sched": sched,
                    "score": depth
                })
        candidates.sort(key=lambda x: x["score"])
        beam = candidates[:beam_width]
        if beam:
            best = beam[0]
            if best_result is None or best["score"] < best_result["score"]:
                best_result = best

    return best_result

