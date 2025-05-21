from gnn_discriminator.model.gnn_discriminator import score_rule
from gnn_discriminator.utils.data_utils import build_graph_from_gate_list

# 一个标准的 H-H → I 的重写对
lhs = [
    {"name": "h", "qubits": [0]},
    {"name": "h", "qubits": [0]},
]
rhs = []  # H-H 抵消了

# 构造图
lhs_graph = build_graph_from_gate_list(lhs)
rhs_graph = build_graph_from_gate_list(rhs)

# 调用 GNN 打分
score = score_rule(lhs_graph, rhs_graph, model_path="gnn_discriminator/gnn_discriminator_weights.pt")
print("✅ GNN score for H-H → I:", score)
