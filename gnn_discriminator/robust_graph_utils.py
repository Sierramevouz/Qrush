import torch
from torch_geometric.data import Data

# ✅ 支持参数门
GATE_NAME_TO_ID = {
    "h": 0,
    "x": 1,
    "y": 2,
    "z": 3,
    "cx": 4,
    "cz": 5,
    "swap": 6,
    "t": 7,
    "tdg": 8,
    "ccx": 9,
    "rz": 10  # ✅ rz 支持参数
}

def extract_gate_type_and_theta(gate):
    """
    提取 gate type id 和参数值（如 rz(theta)）
    """
    if isinstance(gate, list):
        gate_name = gate[0].lower()
        gate_type = GATE_NAME_TO_ID.get(gate_name, 0)

        # rz gate: ["rz", ["Q0"], ["Q0", "P1"]]
        if gate_name == "rz" and len(gate) >= 3 and isinstance(gate[2], list):
            params = gate[2]
            for p in params:
                if isinstance(p, str) and p.startswith("P"):
                    try:
                        theta = float(p[1:])  # P0 → 0.0
                        return gate_type, theta
                    except:
                        return gate_type, 0.0
        return gate_type, 0.0

    return GATE_NAME_TO_ID.get("h", 0), 0.0

def robust_convert_gate_list_to_graph(gate_list):
    """
    将 gate list 转换为 PyG 的 Data 图对象（健壮版本）
    支持参数 rz(theta)，跳过 add，并确保至少 1 个 node 和有效 edge_index
    """
    node_feats = []
    edge_index = []

    last_valid_idx = None
    for i, gate in enumerate(gate_list):
        if isinstance(gate, list) and gate[0].lower() == "add":
            continue  # 跳过 add 但不影响拓扑顺序

        gate_type, theta = extract_gate_type_and_theta(gate)
        node_feats.append([gate_type, theta])

        if last_valid_idx is not None:
            edge_index.append([last_valid_idx, len(node_feats) - 1])
        last_valid_idx = len(node_feats) - 1

    if not node_feats:
        node_feats = [[0, 0.0]]
    if not edge_index:
        edge_index = [[0, 0]]

    x = torch.tensor(node_feats, dtype=torch.float32)  # [N, 2]
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()  # [2, E]

    if edge_index.shape[1] == 0 or edge_index.max().item() >= x.size(0):
        raise ValueError("Invalid edge index")

    return Data(x=x, edge_index=edge_index)
