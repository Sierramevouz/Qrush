import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv

class GateGNNEncoder(nn.Module):
    def __init__(self, in_dim, hidden_dim, emb_dim, num_layers=2):
        super().__init__()
        self.convs = nn.ModuleList()
        self.convs.append(SAGEConv(in_dim, hidden_dim))
        for _ in range(num_layers-2):
            self.convs.append(SAGEConv(hidden_dim, hidden_dim))
        self.convs.append(SAGEConv(hidden_dim, emb_dim))
        self.act = nn.ReLU()
        
    def forward(self, x, edge_index):
        for conv in self.convs[:-1]:
            x = self.act(conv(x, edge_index))
        x = self.convs[-1](x, edge_index)
        return x    # [num_gates, emb_dim]

class GateSelector(nn.Module):
    def __init__(self, emb_dim):
        super().__init__()
        self.gate_head = nn.Linear(emb_dim, 1)

    def forward(self, gate_emb):
        logits = self.gate_head(gate_emb).squeeze(-1)   # [num_gates]
        probs = F.softmax(logits, dim=0)
        return logits, probs
