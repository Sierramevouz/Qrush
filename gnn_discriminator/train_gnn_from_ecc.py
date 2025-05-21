from pathlib import Path
Path("train_gnn_from_ecc_with_negatives.py").write_text('''\
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
    label_batch = torch.tensor(labels, dtype=torch.float32).squeeze()
    return lhs_batch, rhs_batch, label_batch

def train():
    jsonl_path = "converted_ecc_rules_with_negatives.jsonl"
    if not os.path.exists(jsonl_path):
        print(f"❌ File not found: {jsonl_path}")
        return

    print("📥 Loading positive + negative ECC rule graph pairs...")
    pairs = load_rule_graph_pairs(jsonl_path)
    if len(pairs) == 0:
        print("❌ No valid data found.")
        return

    dataset = [(lhs, rhs, label) for lhs, rhs, label in pairs]
    loader = DataLoader(dataset, batch_size=32, shuffle=True, collate_fn=collate_fn)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = GNNRewriteDiscriminator(
        num_gate_types=10,
        embedding_dim=16,
        hidden_dim=32,
        num_layers=2,
        pooling='mean'
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.BCEWithLogitsLoss()

    print("🚀 Starting training on ECC rule pairs (with negatives)...")
    model.train()
    for epoch in range(1, 11):
        total_loss = 0
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
    print("✅ GNN Discriminator retrained and saved to gnn_discriminator_weights.pt")

if __name__ == "__main__":
    train()
''')
