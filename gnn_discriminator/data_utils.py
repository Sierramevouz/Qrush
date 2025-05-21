import json
import torch
from torch_geometric.data import Data
from tqdm import tqdm

# ✅ Gate embedding 映射
GATE_NAME_TO_ID = {
    "h": 0, "x": 1, "y": 2, "z": 3, "cx": 4,
    "cz": 5, "swap": 6, "t": 7, "tdg": 8,
    "ccx": 9, "rz": 10  # ✅ rz 参数门支持
}


def extract_gate_type_and_param(gate):
    """
    ✅ 支持 ECC 格式（list）和 RL 格式（dict）
    - ECC: ["rz", ["Q0"], ["Q0", "P1"]] → θ = 1.0
    - RL:  {"name": "rz", "param": 0.5}
    """
    if isinstance(gate, dict):
        gate_name = gate.get("name", "").lower()
        param = gate.get("param", 0.0)
        gate_id = GATE_NAME_TO_ID.get(gate_name, -1)
        return gate_id, float(param)

    if isinstance(gate, list):
        gate_name = gate[0].lower()
        gate_id = GATE_NAME_TO_ID.get(gate_name, -1)

        # rz gate with symbolic parameter P1
        if gate_name == "rz" and len(gate) >= 3 and isinstance(gate[2], list):
            for p in gate[2]:
                if isinstance(p, str) and p.startswith("P"):
                    try:
                        return gate_id, float(p[1:])
                    except:
                        return gate_id, 0.0
        return gate_id, 0.0

    return 0, 0.0  # fallback


def build_graph_from_gate_list(gate_list):
    """
    ✅ 将 gate_list 转为 PyG 图，节点为 [gate_id, param]，边为线性连接
    """
    node_attrs = []
    edge_index = []
    last_valid_node = None

    for gate in gate_list:
        gate_id, param = extract_gate_type_and_param(gate)
        if gate_id == -1:
            continue
        node_attrs.append([gate_id, param])

        current_idx = len(node_attrs) - 1
        if last_valid_node is not None:
            edge_index.append([last_valid_node, current_idx])
        last_valid_node = current_idx

    if not node_attrs:
        node_attrs = [[0, 0.0]]
    if not edge_index:
        edge_index = [[0, 0]]

    x = torch.tensor(node_attrs, dtype=torch.float32).view(-1, 2)
    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    batch = torch.zeros(x.size(0), dtype=torch.long)

    if edge_index.max().item() >= x.size(0):
        raise ValueError(f"Invalid edge index: {edge_index.tolist()} > x.size(0)={x.size(0)}")

    return Data(x=x, edge_index=edge_index, batch=batch)


def load_rule_graph_pairs(jsonl_path):
    """
    ✅ 从 jsonl 文件中加载 lhs/rhs gate list 样本，并构造为图对 + 标签
    """
    pairs = []
    with open(jsonl_path, "r") as f:
        for line in tqdm(f, desc=f"🔄 Parsing {jsonl_path.split('/')[-1]}"):
            try:
                rule = json.loads(line)
                lhs_graph = build_graph_from_gate_list(rule["lhs"])
                rhs_graph = build_graph_from_gate_list(rule["rhs"])
                label = torch.tensor([float(rule.get("label", 1.0))])
                pairs.append((lhs_graph, rhs_graph, label))
            except Exception:
                continue
    return pairs
