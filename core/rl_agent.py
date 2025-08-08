import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from .gnn_gate_encoder import GateGNNEncoder

class GateSelector(nn.Module):
    def __init__(self, emb_dim):
        super().__init__()
        self.gate_head = nn.Linear(emb_dim, 1)
    def forward(self, gate_emb):
        logits = self.gate_head(gate_emb).squeeze(-1)   # [num_gates]
        probs = F.softmax(logits, dim=0)
        return logits, probs

class TransformationSelector(nn.Module):
    def __init__(self, emb_dim, max_rules=32):
        super().__init__()
        # max_rules: 最大支持的rule种类数（可据ECC集动态调整）
        self.rule_head = nn.Linear(emb_dim, max_rules)
        self.max_rules = max_rules
    def forward(self, gate_emb, rule_mask=None):
        logits = self.rule_head(gate_emb)  # [max_rules]
        if rule_mask is not None:
            # mask掉不可用rule（置极小）
            mask = torch.zeros_like(logits) - 1e9
            mask[rule_mask] = 0
            logits = logits + mask
        probs = F.softmax(logits, dim=-1)
        return logits, probs

class QuarlAgent(nn.Module):
    """
    双头策略: (1) GateSelector (GNN+MLP)  (2) TransformationSelector (MLP/MLP+掩码)
    完全兼容QuartzRLRewriteEnv, 支持RL/PPO扩展
    """
    def __init__(self, env, hidden_dim=64, emb_dim=32, num_layers=2, max_rules=32, device='cpu'):
        super().__init__()
        self.env = env
        self.device = device
        pyg_data = env.get_pyg_data()
        in_dim = pyg_data.x.shape[1]

        # ---- 网络结构 ----
        self.encoder = GateGNNEncoder(in_dim, hidden_dim, emb_dim, num_layers).to(device)
        self.gate_selector = GateSelector(emb_dim).to(device)
        self.trans_selector = TransformationSelector(emb_dim, max_rules).to(device)

        # ---- 优化器 ----
        self.optimizer = torch.optim.Adam(
            list(self.encoder.parameters()) +
            list(self.gate_selector.parameters()) +
            list(self.trans_selector.parameters()),
            lr=1e-3
        )

    def select_action(self, pyg_data):
        self.encoder.eval()
        self.gate_selector.eval()
        self.trans_selector.eval()

        x = pyg_data.x.to(self.device)
        edge_index = pyg_data.edge_index.to(self.device)
        gate_emb = self.encoder(x, edge_index)      # [num_gates, emb_dim]

        # ---- 1. 选择 gate ----
        gate_logits, gate_probs = self.gate_selector(gate_emb)
        probs_np = gate_probs.detach().cpu().numpy()
        gate_idx = np.random.choice(len(probs_np), p=probs_np)

        # ---- 2. 选择 transformation(rule) ----
        # 用选中的 gate 的 embedding
        chosen_emb = gate_emb[gate_idx]
        possible_rule_ids = self.env.get_applicable_transformations(gate_idx)
        if not possible_rule_ids:
            return gate_idx, None, None, None  # 直接终止
        # 构造rule mask: 长度=max_rules, 只允许 possible_rule_ids
        rule_mask = torch.zeros(self.trans_selector.max_rules, dtype=torch.bool)
        rule_mask[possible_rule_ids] = True
        rule_logits, rule_probs = self.trans_selector(chosen_emb, rule_mask=rule_mask)
        rule_probs_np = rule_probs.detach().cpu().numpy()
        # softmax后可能数值极小、全0（mask全1e-9），保险起见fallback随机
        if np.sum(rule_probs_np) <= 0 or np.any(np.isnan(rule_probs_np)):
            rule_idx = np.random.choice(possible_rule_ids)
        else:
            rule_idx = np.random.choice(self.trans_selector.max_rules, p=rule_probs_np)
            if rule_idx not in possible_rule_ids:
                rule_idx = np.random.choice(possible_rule_ids)
        return gate_idx, rule_idx, gate_logits.detach().cpu().numpy(), rule_logits.detach().cpu().numpy()

    def run_episode(self, verbose=False):
        self.env.reset()
        done = False
        total_reward = 0
        step_count = 0

        while not done:
            pyg_data = self.env.get_pyg_data()
            gate_idx, rule_idx, gate_logits, rule_logits = self.select_action(pyg_data)
            if rule_idx is None:
                if verbose:
                    print(f"Step {step_count+1}: No available rule for gate {gate_idx}, episode ends.")
                break
            _, reward, done, info = self.env.step(gate_idx, rule_idx)
            total_reward += reward
            step_count += 1
            if verbose:
                print(f"Step {step_count}: gate={gate_idx}, rule={rule_idx}, reward={reward}, done={done}")
        return total_reward

    def update(self, batch):
        # 留给PPO/REINFORCE扩展
        pass

