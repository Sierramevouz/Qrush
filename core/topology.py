import networkx as nx
from networkx import floyd_warshall

# 🧠 Topology Presets (内置多个结构)
AVAILABLE_TOPOLOGIES = {
    "line": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)],
    "ibmq_tokyo_7": [(0, 1), (1, 2), (1, 3), (3, 4), (4, 5), (5, 6)],
    "fully_connected": [(i, j) for i in range(7) for j in range(7) if i != j],
    "grid_3x3": [
        (0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8),
        (0, 3), (3, 6), (1, 4), (4, 7), (2, 5), (5, 8)
    ],
}

# === 构建拓扑图（用于 swap cost + qubit mapping）
def build_coupling_graph(edge_list):
    G = nx.Graph()
    G.add_edges_from(edge_list)
    return G

# === 使用 Floyd-Warshall 计算任意两 qubit 之间的距离
def compute_distance_matrix(coupling_graph):
    return dict(floyd_warshall(coupling_graph))

# === 打印距离矩阵（调试用）
def print_distance_matrix(distances):
    print("🧮 Qubit Distance Matrix:")
    for q1 in sorted(distances):
        row = "  q{}: ".format(q1)
        for q2 in sorted(distances[q1]):
            row += "{:3} ".format(int(distances[q1][q2]))
        print(row)
