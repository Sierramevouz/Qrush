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
    t = [cp.Variable(integer=True) for _ in range(n)]     # 每个门的执行时刻
    t_max = cp.Variable(integer=True)                     # 最大深度变量
    swap_penalties = []                                   # swap cost 累计

    constraints = []
    last_on_qubit = {}

    for i, (gate, qlist) in enumerate(gates):
        # 基本调度约束：同 qubit 门不能重叠
        for q in qlist:
            if q in last_on_qubit:
                constraints.append(t[i] - t[last_on_qubit[q]] >= 1)
            last_on_qubit[q] = i

        constraints.append(t[i] >= 0)
        constraints.append(t_max >= t[i])

        # === Swap 惩罚项：非物理相邻的 CX 引入距离惩罚
        if gate == "cx" and distance_matrix:
            q1, q2 = qlist
            dist = distance_matrix[q1][q2]
            if dist > 1:
                swap_penalties.append(dist - 1)

    # === 优化目标：最小化 depth + 加权 swap cost
    total_swap_cost = cp.Constant(sum(swap_penalties))
    objective = cp.Minimize(t_max + weight_swap * total_swap_cost)

    prob = cp.Problem(objective, constraints)
    try:
        prob.solve()
    except:
        return None, float("inf")

    if prob.status not in ["optimal", "optimal_inaccurate"]:
        return None, float("inf")

    schedule = {i: safe(t[i].value) for i in range(n)}
    return schedule, safe(t_max.value)
