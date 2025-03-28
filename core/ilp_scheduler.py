import cvxpy as cp
import numpy as np
from core.topology import build_coupling_graph, compute_distance_matrix

def safe(val):
    if val is None:
        return -999
    if isinstance(val, np.ndarray):
        return int(round(val.item()))
    return int(round(val))

# === 核心调度器：支持拓扑约束与 SWAP cost 惩罚
def schedule_ilp(gates, num_qubits=3, coupling_graph=None, distance_matrix=None, weight_swap=1.0):
    n = len(gates)
    t = [cp.Variable(integer=True) for _ in range(n)]
    t_max = cp.Variable(integer=True)
    swap_penalties = []
    constraints = []

    # ✅ 动态构造拓扑图和距离矩阵（如未提供）
    if coupling_graph is not None:
        from core.topology import build_coupling_graph, compute_distance_matrix
        if isinstance(coupling_graph, list):  # 是边列表才构图
            G = build_coupling_graph(coupling_graph)
            distance_matrix = compute_distance_matrix(G)

    last_on_qubit = {}
    for i, (gate, qlist) in enumerate(gates):
        for q in qlist:
            if q in last_on_qubit:
                constraints.append(t[i] - t[last_on_qubit[q]] >= 1)
            last_on_qubit[q] = i
        constraints.append(t[i] >= 0)
        constraints.append(t_max >= t[i])

        # ✅ swap cost 惩罚（仅对两比特门）
        if distance_matrix and gate == "cx" and len(qlist) == 2:
            q1, q2 = qlist
            if q1 in distance_matrix and q2 in distance_matrix[q1]:
                dist = distance_matrix[q1][q2]
                if dist > 1:
                    swap_penalties.append(dist - 1)

    # 优化目标：深度 + 加权 swap 成本
    total_swap_cost = cp.Constant(sum(swap_penalties))
    prob = cp.Problem(cp.Minimize(t_max + weight_swap * total_swap_cost), constraints)

    try:
        prob.solve()
    except:
        return None, float("inf")

    if prob.status not in ["optimal", "optimal_inaccurate"]:
        return None, float("inf")

    schedule = {i: safe(t[i].value) for i in range(n)}
    return schedule, safe(t_max.value)
