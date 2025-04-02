import json
import torch
from torch_geometric.data import Data

# ✅ Gate type mapping for embedding
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
    "ccx": 9  # Toffoli
}

def convert_gate_list_to_graph(gate_list):
    edge_index = []
    node_types = []

    for idx, gate in enumerate(gate_list):
        gate_name = gate["name"].lower()
        gate_type = GATE_NAME_TO_ID.get(gate_name, 0)
        node_types.append(gate_type)

        for j in range(idx):
            edge_index.append([j, idx])
            edge_index.append([idx, j])  # 双向连接

    if len(node_types) == 0:
        node_types = [0]  # 空图 fallback（用一个 dummy 节点）
        edge_index = []

    x = torch.tensor(node_types, dtype=torch.long)
    if edge_index:
        edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    else:
        edge_index = torch.empty((2, 0), dtype=torch.long)

    return Data(x=x, edge_index=edge_index)

def load_rule_graph_pairs(jsonl_path):
    pairs = []
    with open(jsonl_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            rule = json.loads(line)
            lhs_graph = convert_gate_list_to_graph(rule["lhs"])
            rhs_graph = convert_gate_list_to_graph(rule["rhs"])
            pairs.append((lhs_graph, rhs_graph))
    return pairs
