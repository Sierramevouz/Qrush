import torch
import torch.nn as nn
from torch_geometric.loader import DataLoader
from torch_geometric.data import Batch
from gnn_discriminator import GNNRewriteDiscriminator
from data_utils import load_rule_graph_pairs
import os

def collate_fn(batch):
    lhs_list, rhs_list, labels = zip(*batch)
    lhs_batch = Batch.from_data_list(lhs_list)
    rhs_batch = Batch.from_data_list(rhs_list)
    label_batch = torch.tensor(labels, dtype=torch.float32).unsqueeze(1)  # [B, 1]
    return lhs_batch, rhs_batch, label_batch

def train():
    jsonl_path = "converted_ecc_rules_with_labels.jsonl"
    if not os.path.exists(jsonl_path):
        print(f"❌ File not found: {jsonl_path}")
        return

    print("📥 Loading positive + negative ECC rule graph pairs...")
    try:
        pairs = load_rule_graph_pairs(jsonl_path)
    except Exception as e:
        print(f"❌ Failed to load dataset: {e}")
        return

    print(f"📊 Number of rule pairs loaded: {len(pairs)}")
    if len(pairs) == 0:
        print("❌ No valid data found.")
        return

    # ✅ 检查 gate_id 范围
    print("🧪 Checking gate id range in all rule pairs...")
    max_gate_id = 0
    for i, (lhs, rhs, label) in enumerate(pairs):
        lhs_max = lhs.x[:, 0].max().item()
        rhs_max = rhs.x[:, 0].max().item()
        if lhs_max > max_gate_id or rhs_max > max_gate_id:
            max_gate_id = max(lhs_max, rhs_max)
        if lhs_max >= 11 or rhs_max >= 11:
            print(f"⚠️  Illegal gate id in pair #{i}: lhs_max={lhs_max}, rhs_max={rhs_max}")
    print(f"✅ Maximum gate_id across dataset: {max_gate_id}")

    # ✅ 打印输入图结构维度
    print("🧪 Checking shape of lhs.x...")
    print("lhs.x.shape =", pairs[0][0].x.shape)

    # ✅ Sanity check 图是否能 Batch 包装
    print("🧪 Sanity checking all rule graph pairs before training...")
    for i, (lhs, rhs, label) in enumerate(pairs):
        try:
            _ = Batch.from_data_list([lhs])
            _ = Batch.from_data_list([rhs])
        except Exception as e:
            print(f"❌ Graph pair #{i} is invalid: {e}")
            print(lhs)
            return
    print("✅ All graph pairs passed Batch wrapping check.")

    dataset = [(lhs, rhs, label) for lhs, rhs, label in pairs]
    loader = DataLoader(dataset, batch_size=32, shuffle=True, collate_fn=collate_fn)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"🖥️  Using device: {device}")

    model = GNNRewriteDiscriminator(
        num_gate_types=11,  # ✅ 支持到 rz
        embedding_dim=16,
        hidden_dim=32,
        num_layers=2,
        pooling='mean'
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.BCEWithLogitsLoss()

    print("🚀 Starting training on ECC rule pairs...")
    model.train()
    for epoch in range(1, 11):
        total_loss = 0.0
        correct = 0
        total = 0
        for lhs_batch, rhs_batch, label_batch in loader:
            lhs_batch = lhs_batch.to(device)
            rhs_batch = rhs_batch.to(device)
            label_batch = label_batch.to(device)

            logits = model(lhs_batch, rhs_batch)
            loss = criterion(logits, label_batch)

            preds = (torch.sigmoid(logits) > 0.5).float()
            correct += (preds == label_batch).sum().item()
            total += label_batch.size(0)

            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            total_loss += loss.item()

        avg_loss = total_loss / len(loader)
        acc = correct / total
        print(f"[Epoch {epoch}] Loss: {avg_loss:.4f} | Acc: {acc:.4f}")

    torch.save(model.state_dict(), "gnn_discriminator_weights.pt")
    print("✅ Model saved: gnn_discriminator_weights.pt")

if __name__ == "__main__":
    train()
