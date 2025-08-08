# core/Rl_agent.py

import torch
import torch.nn as nn
import torch.nn.functional as F
from gnn_gate_encoder import GateGNNEncoder as GNNGateEncoder



class RLAgent(nn.Module):
    def __init__(self, node_feat_dim, emb_dim, num_rules):
        super().__init__()
        self.encoder = GNNGateEncoder(node_feat_dim, 64, emb_dim)
        self.gate_selector = nn.Linear(emb_dim, 1)          # [N, 1]
        self.rule_selector = nn.Linear(emb_dim, num_rules)  # [N, R]

    def forward(self, data):
        node_embeddings = self.encoder(data.x, data.edge_index)  # shape: [N, D]

        gate_logits = self.gate_selector(node_embeddings).squeeze(-1)  # [N]
        rule_logits = self.rule_selector(node_embeddings)              # [N, R]

        # softmax over gates and rules
        gate_probs = F.softmax(gate_logits, dim=0)
        gate_dist = torch.distributions.Categorical(gate_probs)
        gate_idx = gate_dist.sample()
        gate_logprob = gate_dist.log_prob(gate_idx)

        rule_probs = F.softmax(rule_logits[gate_idx], dim=0)
        rule_dist = torch.distributions.Categorical(rule_probs)
        rule_idx = rule_dist.sample()
        rule_logprob = rule_dist.log_prob(rule_idx)

        return (int(gate_idx.item()), int(rule_idx.item())), gate_logprob + rule_logprob
