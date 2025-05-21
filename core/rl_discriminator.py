import sys
import os
from typing import List, Dict, Tuple

# ✅ 确保能 import gnn_discriminator/score_rule.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "gnn_discriminator")))

from score_rule import score_rule  # ✅ 正确引用
from data_utils import build_graph_from_gate_list  # 同理你可以移入 score_rule.py 或 data_utils.py 中


class GNNDiscriminatorAgent:
    def __init__(self, model_path: str, device=None):
        self.model_path = model_path
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")

    def evaluate(self, lhs_gate_list: List[Dict], rhs_gate_list: List[Dict]) -> float:
        lhs_graph = build_graph_from_gate_list(lhs_gate_list)
        rhs_graph = build_graph_from_gate_list(rhs_gate_list)
        return score_rule(lhs_graph, rhs_graph, model_path=self.model_path, device=self.device)

    def update_baseline(self, new_gate_list):
        self.baseline_gate_count = len(new_gate_list)


class GNNDiscriminatorAgent:
    """
    使用 GNN 判别器评估 rewrited 电路中应用的 rewrite 子结构 lhs → rhs 是否合理。
    """
    def __init__(self, model_path: str, device=None):
        self.model_path = model_path
        self.device = device

    def evaluate(self, original_gate_list: List[Dict], rewrited_gate_list: List[Dict]) -> float:
        print("🧠 [DEBUG] GNNDiscriminatorAgent.evaluate() called")
        lhs, rhs = self.extract_lhs_rhs_from_diff(original_gate_list, rewrited_gate_list)

        if not lhs or not rhs:
            print("⚠️ [GNN] Empty LHS or RHS after diff extraction, fallback -1.0")
            return -1.0

        try:
            print(f"📐 [GNN] Scoring LHS→RHS with model: {self.model_path}")

            lhs_graph = build_graph_from_gate_list(lhs)
            rhs_graph = build_graph_from_gate_list(rhs)

            # ✅ 打印图结构信息
            print(f"[Graph] LHS nodes: {lhs_graph.x.shape}, edges: {lhs_graph.edge_index.shape}")
            print(f"[Graph] RHS nodes: {rhs_graph.x.shape}, edges: {rhs_graph.edge_index.shape}")

            score = score_rule(lhs_graph, rhs_graph, model_path=self.model_path, device=self.device)
            print(f"✅ [GNN] score_rule = {score:.4f}")
            return float(score)

        except Exception as e:
            print(f"❌ [GNNDiscriminatorAgent] scoring failed: {e}")
            return -1.0

    @staticmethod
    def extract_lhs_rhs_from_diff(old: List[Dict], new: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        提取 old 和 new gate list 的最小差异区间作为 rewrite 的 lhs / rhs。
        """
        min_len = min(len(old), len(new))
        start = 0
        while start < min_len and old[start] == new[start]:
            start += 1

        end_old = len(old) - 1
        end_new = len(new) - 1
        while end_old >= start and end_new >= start and old[end_old] == new[end_new]:
            end_old -= 1
            end_new -= 1

        lhs = old[start:end_old + 1]
        rhs = new[start:end_new + 1]

        print(f"[DIFF] ⬅️ LHS size: {len(lhs)} | ➡️ RHS size: {len(rhs)} | Δ range: [{start}, {end_old}]")
        return lhs, rhs
