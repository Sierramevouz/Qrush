import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv, global_mean_pool

from torch_geometric.data import Data

class GNNRewriteDiscriminator(nn.Module):
    def __init__(self, num_gate_types=11, embedding_dim=16, hidden_dim=32, num_layers=2, pooling='mean'):
        super().__init__()
        self.embedding = nn.Embedding(num_gate_types, embedding_dim)
        self.convs = nn.ModuleList()
        self.pooling = pooling

        for i in range(num_layers):
            in_dim = embedding_dim if i == 0 else hidden_dim
            self.convs.append(GCNConv(in_dim, hidden_dim))

        self.out_layer = nn.Linear(hidden_dim * 2, 1)

    def forward(self, lhs: Data, rhs: Data):
        lhs_x = self.embedding(lhs.x[:, 0].long())
        rhs_x = self.embedding(rhs.x[:, 0].long())

        for conv in self.convs:
            lhs_x = conv(lhs_x, lhs.edge_index).relu()
            rhs_x = conv(rhs_x, rhs.edge_index).relu()

        lhs_vec = global_mean_pool(lhs_x, lhs.batch)
        rhs_vec = global_mean_pool(rhs_x, rhs.batch)

        combined = torch.cat([lhs_vec, rhs_vec], dim=1)
        return self.out_layer(combined)


def score_rule(lhs_graph, rhs_graph, model_path="gnn_discriminator_weights.pt", device="cuda"):
    device = torch.device(device if torch.cuda.is_available() else "cpu")
    model = GNNRewriteDiscriminator().to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    with torch.no_grad():
        score = model(lhs_graph.to(device), rhs_graph.to(device)).sigmoid().item()
    return score
