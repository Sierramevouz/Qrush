# gnn_discriminator/score_interface.py
import torch
from gnn_discriminator import GNNRewriteDiscriminator

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载预训练 GNN 判别器
model = GNNRewriteDiscriminator()
model.load_state_dict(torch.load("gnn_discriminator_weights.pt", map_location=device))
model.to(device)
model.eval()

@torch.no_grad()
def score_rule(lhs_graph, rhs_graph) -> float:
    lhs_graph = lhs_graph.to(device)
    rhs_graph = rhs_graph.to(device)
    output = model(lhs_graph, rhs_graph)
    return output.item()
