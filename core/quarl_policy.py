import torch.nn as nn
from .gnn_gate_encoder import GateGNNEncoder, GateSelector

class QuarlGatePolicy(nn.Module):
    def __init__(self, in_dim, hidden_dim, emb_dim, num_layers=2):
        super().__init__()
        self.encoder = GateGNNEncoder(in_dim, hidden_dim, emb_dim, num_layers)
        self.selector = GateSelector(emb_dim)
    
    def forward(self, data):
        # data: PyG Data, data.x=[num_gates, in_dim], data.edge_index=[2, num_edges]
        gate_emb = self.encoder(data.x, data.edge_index)
        logits, probs = self.selector(gate_emb)
        return logits, probs, gate_emb
