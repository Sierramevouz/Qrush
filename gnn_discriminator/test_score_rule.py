import torch
import random
from collections import Counter
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader

from gnn_discriminator import GNNRewriteDiscriminator
from data_utils import load_rule_graph_pairs

# ✅ Gate 编码映射（与构图器保持一致）
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
    "rz": 10  # ✅ 支持 rz 参数门
}


def make_rz(params: list[float]) -> Data:
    """
    构造一个只有 rz(θ) 参数门的序列图。
    每个参数门为一个节点，顺序连接。
    """
    node_attrs = []
    edge_index = []
    for i, theta in enumerate(params):
        node_attrs.append([GATE_NAME_TO_ID["rz"], 1])  # gate_id=10, is_param=1
        if i > 0:
            edge_index.append([i - 1, i])
    if not node_attrs:
        node_attrs = [[0, 0]]
        edge_index = [[0, 0]]
    x = torch.tensor(node_attrs, dtype=torch.long)
    edge_index = torch.tensor(edge_index or [[0, 0]], dtype=torch.long).t().contiguous()
    return Data(x=x, edge_index=edge_index)


def main():
    jsonl_path = "converted_ecc_rules_with_labels.jsonl"
    pairs = load_rule_graph_pairs(jsonl_path)

    # ✅ 标签统计
    labels = [label.item() for _, _, label in pairs]
    counter = Counter(labels)
    print("\n📊 Label Distribution in ECC Rule Dataset:")
    for k in sorted(counter.keys()):
        print(f"  Label {k:.1f} → {counter[k]} samples")

    positives = [(lhs, rhs) for lhs, rhs, label in pairs if label == 1.0]
    negatives = [(lhs, rhs) for lhs, rhs, label in pairs if label == 0.0]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n🖥️  Using device: {device}")

    model = GNNRewriteDiscriminator(
        num_gate_types=11,
        embedding_dim=16,
        hidden_dim=32,
        num_layers=2,
        pooling='mean'
    ).to(device)

    model.load_state_dict(torch.load("gnn_discriminator_weights.pt", map_location=device))
    model.eval()

    print(f"\n📦 Loaded {len(pairs)} total rule pairs ({len(positives)} positives, {len(negatives)} negatives)")

    print("\n✅ 正例得分（应高）：")
    for i in range(5):
        lhs, rhs = random.choice(positives)
        with torch.no_grad():
            score = model(lhs.to(device), rhs.to(device)).sigmoid().item()
        print(f"[Good Pair #{i+1}] Score = {score:.4f}")

    print("\n❌ 负例得分（应低）：")
    for i in range(5):
        lhs, rhs = random.choice(negatives)
        with torch.no_grad():
            score = model(lhs.to(device), rhs.to(device)).sigmoid().item()
        print(f"[Bad Pair #{i+1}] Score = {score:.4f}")

    # ✅ 参数合并能力测试（rz(a) + rz(b) ≈ rz(a+b)）
    print("\n🔬 参数合并能力评估（rz(θ1)+rz(θ2) ≈ rz(θ1+θ2)）：")

    rz_seq = make_rz([0.3, 0.5])
    rz_merge = make_rz([0.8])

    print(f"rz_seq x: {rz_seq.x}")
    print(f"rz_seq edge_index: {rz_seq.edge_index}")
    print(f"rz_merge x: {rz_merge.x}")
    print(f"rz_merge edge_index: {rz_merge.edge_index}")

    with torch.no_grad():
        score = model(rz_seq.to(device), rz_merge.to(device)).sigmoid().item()
    print(f"[rz(0.3)+rz(0.5)] vs rz(0.8) → Score = {score:.4f}")


if __name__ == "__main__":
    main()
