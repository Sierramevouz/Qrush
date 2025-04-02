import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv, global_mean_pool

class GNNRewriteDiscriminator(nn.Module):
    def __init__(self, in_channels=16, hidden_channels=32):
        super().__init__()
        self.embedding = nn.Embedding(10, in_channels)  # 10种门类型
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.pool = global_mean_pool
        self.fc = nn.Sequential(
            nn.Linear(hidden_channels * 2, hidden_channels),
            nn.ReLU(),
            nn.Linear(hidden_channels, 1)
        )

    def forward(self, lhs_data: Data, rhs_data: Data):
        x_lhs = self.embedding(lhs_data.x.view(-1).long())
        h_lhs = self.conv1(x_lhs, lhs_data.edge_index)
        h_lhs = F.relu(self.conv2(h_lhs, lhs_data.edge_index))
        h_lhs = self.pool(h_lhs, lhs_data.batch)

        x_rhs = self.embedding(rhs_data.x.view(-1).long())
        h_rhs = self.conv1(x_rhs, rhs_data.edge_index)
        h_rhs = F.relu(self.conv2(h_rhs, rhs_data.edge_index))
        h_rhs = self.pool(h_rhs, rhs_data.batch)

        h_combined = torch.cat([h_lhs, h_rhs], dim=1)
        return self.fc(h_combined).squeeze(1)  # 输出 raw logits
