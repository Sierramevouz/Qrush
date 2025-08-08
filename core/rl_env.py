# core/rl_env.py

import random
import networkx as nx
import torch
from torch_geometric.data import Data
from typing import List
from ecc_loader import ECCRule
from circuit_graph import build_graph_from_gate_list
from matcher import find_matches
from rewriter import apply_rule_at


class RewriteEnv:
    def __init__(self, initial_gate_list: List[dict], ecc_rules: List[ECCRule]):
        self.init_gate_list = initial_gate_list
        self.rules = ecc_rules
        self.reset()

    def reset(self):
        self.gate_list = self.init_gate_list.copy()
        self.graph = build_graph_from_gate_list(self.gate_list)
        self.cost = len(self.gate_list)
        return self.get_pyg_data()

    def get_pyg_data(self):
        x = []
        gate_type_map = {'x': 0, 'cx': 1, 'rz': 2, 'h': 3, 'add': 4}
        for _, d in self.graph.nodes(data=True):
            gate_id = gate_type_map.get(d['gate'], -1)
            qubits = d.get("qubits", [])
            q0 = qubits[0] if len(qubits) > 0 else -1
            q1 = qubits[1] if len(qubits) > 1 else -1
            param = d.get("params", [0.0])
            if isinstance(param, list) and len(param) > 0:
                try:
                    theta = float(param[0])
                except ValueError:
                    theta = 0.0  # 符号参数 P0/P1 等统一设为常数 0.0
            else:
                theta = 0.0
            x.append([gate_id, q0, q1, theta])

        x = torch.tensor(x, dtype=torch.float)
        edge_index = torch.tensor(list(self.graph.edges), dtype=torch.long).t().contiguous()
        if edge_index.numel() == 0:
            edge_index = torch.empty((2, 0), dtype=torch.long)
        return Data(x=x, edge_index=edge_index)

    def get_applicable_actions(self):
        actions = []
        for gate_node in self.graph.nodes:
            for rule_idx, rule in enumerate(self.rules):
                matches = find_matches(self.graph, rule.lhs_graph)
                for match in matches:
                    if gate_node in match.values():  # gate_node 被匹配到
                        actions.append((gate_node, rule_idx, match))
        return actions

    def step(self, action):
        gate_node, rule_idx, match = action
        rule = self.rules[rule_idx]
        new_graph = apply_rule_at(self.graph, match, rule.rhs_gates)

        # 计算 reward = old_gate_num - new_gate_num
        old_cost = len(self.graph.nodes)
        new_cost = len(new_graph.nodes)
        reward = old_cost - new_cost

        # 更新状态
        self.graph = new_graph
        self.gate_list = None  # 可忽略，主图已更新
        self.cost = new_cost

        done = False
        return self.get_pyg_data(), reward, done, {}

        print(f"[step] Attempting rule {rule_idx} at node {gate_node}")
        print(f"[step] nodes before: {old_cost}, after: {new_cost}, reward: {reward}")

