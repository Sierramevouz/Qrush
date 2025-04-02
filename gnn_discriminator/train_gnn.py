import torch
import torch.nn as nn
import torch.optim as optim
from torch_geometric.loader import DataLoader
from gnn_discriminator import GNNRewriteDiscriminator
from data_utils import load_rule_graph_pairs

def make_labeled_dataset(pairs):
    dataset = []
    for lhs, rhs in pairs:
        lhs_len = lhs.num_nodes
        rhs_len = rhs.num_nodes
        label = 1 if rhs_len < lhs_len else 0
        dataset.append((lhs, rhs, torch.tensor(label, dtype=torch.float)))
    return dataset

class RulePairDataset(torch.utils.data.Dataset):
    def __init__(self, triples):
        self.triples = triples

    def __len__(self):
        return len(self.triples)

    def __getitem__(self, idx):
        return self.triples[idx]

def collate_fn(batch):
    lhs_list, rhs_list, labels = zip(*batch)
    return list(lhs_list), list(rhs_list), torch.tensor(labels)

def train():
    jsonl_path = "auto_rules_test.jsonl"
    pairs = load_rule_graph_pairs(jsonl_path)
    dataset = make_labeled_dataset(pairs)
    loader = DataLoader(RulePairDataset(dataset), batch_size=2, shuffle=True, follow_batch=['x'], collate_fn=collate_fn)

    model = GNNRewriteDiscriminator()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.BCEWithLogitsLoss()

    for epoch in range(10):
        model.train()
        total_loss = 0
        for lhs_batch, rhs_batch, labels in loader:
            lhs = lhs_batch[0].to(device)
            rhs = rhs_batch[0].to(device)
            label = labels[0].to(device)

            optimizer.zero_grad()
            outputs = model(lhs, rhs).squeeze()  # shape: [1] → scalar
            loss = criterion(outputs, label)  # 取出单个label
            print("🔍 Output:", outputs.item())
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"📘 Epoch {epoch+1}: Loss = {total_loss:.4f}")

    torch.save(model.state_dict(), "gnn_discriminator_weights.pt")
    print("✅ GNN Discriminator saved.")

if __name__ == "__main__":
    train()
