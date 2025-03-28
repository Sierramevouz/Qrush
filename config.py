# === Global Configuration Parameters ===

# --- Search Parameters ---
MAX_REWRITE_DEPTH = 3     # BFS 拓展最大深度
BEAM_WIDTH = 5            # 每一层保留 top-K 候选

# --- Gate Set ---
SUPPORTED_GATES = ["h", "cx", "t", "tdg", "rz"]  # 支持的基础门类型

# --- Gantt 图颜色配置 ---
GATE_COLORS = ["skyblue", "orange", "green", "red", "purple", "gray"]

# --- 是否启用等价验证 ---
ENABLE_EQUIVALENCE_CHECK = True


# === Coupling Graph Topologies ===

# 全连接（所有 qubit 互连）
FULLY_CONNECTED = [(i, j) for i in range(7) for j in range(7) if i != j]

# IBMQ Tokyo 拓扑（7 qubit 示例）
IBMQ_TOKYO_7 = [
    (0, 1), (1, 2), (1, 3), (3, 4),
    (4, 5), (5, 6)
]

# 线性链（Linear）
LINEAR_7 = [(i, i+1) for i in range(6)]

# 3x3 网格拓扑（Grid）
GRID_3x3 = [
    (0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8),
    (0, 3), (3, 6), (1, 4), (4, 7), (2, 5), (5, 8)
]

# ✅ 当前启用拓扑（调度器中会读取此配置）
COUPLING_GRAPH = IBMQ_TOKYO_7
