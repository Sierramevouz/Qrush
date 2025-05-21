import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv, global_mean_pool, global_max_pool, global_add_pool

class GNNRewriteDiscriminator(nn.Module):
    def __init__(self,
                 num_gate_types=10,
                 embedding_dim=16,
                 hidden_dim=32,
                 num_layers=2,
                 pooling='mean'):
        super().__init__()
        self.gate_embedding = nn.Embedding(num_gate_types, embedding_dim)
        self.param_encoder = nn.Linear(1, embedding_dim)  # ✅ 编码参数 θ

        # 多层 GCN 构建
        self.convs = nn.ModuleList()
        self.convs.append(GCNConv(embedding_dim, hidden_dim))
        for _ in range(num_layers - 1):
            self.convs.append(GCNConv(hidden_dim, hidden_dim))

        # 池化策略
        if pooling == 'mean':
            self.pool = global_mean_pool
        elif pooling == 'max':
            self.pool = global_max_pool
        elif pooling == 'sum':
            self.pool = global_add_pool
        else:
            raise ValueError(f"Unsupported pooling method: {pooling}")

        # 输出层
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

    def encode(self, data: Data):
        gate_ids = data.x[:, 0].long()
        params = data.x[:, 1].unsqueeze(-1).float()

        gate_embed = self.gate_embedding(gate_ids)
        param_embed = self.param_encoder(params)

        x = gate_embed + param_embed  # ✅ 合并门类型和参数信息

        for conv in self.convs:
            x = F.relu(conv(x, data.edge_index))

        return self.pool(x, data.batch)

    def forward(self, lhs_data: Data, rhs_data: Data):
        h_lhs = self.encode(lhs_data)
        h_rhs = self.encode(rhs_data)
        h_combined = torch.cat([h_lhs, h_rhs], dim=1)
        return self.fc(h_combined)

# ✅ 判别函数接口不变
def score_rule(lhs_graph, rhs_graph, model_path="gnn_discriminator_weights.pt", device=None):
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = GNNRewriteDiscriminator(
        num_gate_types=11,
        embedding_dim=16,
        hidden_dim=32,
        num_layers=2,
        pooling='mean'
    ).to(device)

    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    lhs_graph = lhs_graph.to(device)
    rhs_graph = rhs_graph.to(device)

    with torch.no_grad():
        score = model(lhs_graph, rhs_graph).sigmoid().item()

    return score
