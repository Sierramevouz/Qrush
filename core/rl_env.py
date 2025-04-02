import copy
from typing import List, Dict, Tuple

class RewriteEnv:
    """
    强化学习环境：给定一个初始电路（gate list），允许 agent 对 gate 应用 rewrite rule，输出 rewrited gate list。
    每一步可以由 agent 决定是否对某个位置的 gate 应用某个 rule。
    环境将维护当前电路状态，并在必要时计算调度性能作为 reward。
    """

    def __init__(self, gate_list: List[Dict], rewrite_rules: Dict[str, callable]):
        self.original_gate_list = copy.deepcopy(gate_list)  # 初始电路
        self.rewrite_rules = rewrite_rules  # 可用重写规则（rule_name -> 函数）
        self.reset()

    def reset(self):
        self.current_gate_list = copy.deepcopy(self.original_gate_list)
        self.step_count = 0
        self.rewrite_trace = []  # 记录每步的 rewrite 操作
        return self._get_obs()

    def _get_obs(self) -> List[Dict]:
        """返回当前电路状态（即门列表），每个门是一个 dict: {name: 'cx', qubits: [0,1], ...}"""
        return self.current_gate_list

    def step(self, position: int, rule_name: str) -> Tuple[List[Dict], float, bool, Dict]:
        """
        agent 在 position 处应用 rule_name 所指定的 rewrite rule
        返回：obs, reward, done, info
        """
        self.step_count += 1
        info = {}

        if rule_name not in self.rewrite_rules:
            raise ValueError(f"Unknown rewrite rule: {rule_name}")

        try:
            new_gates = self.rewrite_rules[rule_name](self.current_gate_list, position)
            self.current_gate_list = new_gates
            self.rewrite_trace.append((position, rule_name))
        except Exception as e:
            info['error'] = str(e)

        done = self.step_count >= 10  # 限制最多 rewrite 10 次，可改为更智能的判断
        reward = self.compute_reward() if done else 0.0
        return self._get_obs(), reward, done, info

    def compute_reward(self) -> float:
        """
        调用已有的 ILP 调度器（或调度统计分析）模块，获得当前 rewrited gate list 的调度深度/swap 总数作为 reward。
        注意：需要你将你的 variant_analysis.py 中的评估函数 hook 进来。
        """
        from variant_analysis import evaluate_gate_list  # ← 本地导入，不要用 core.xxx

        result = evaluate_gate_list(self.current_gate_list)
        # 假设 result 返回 dict: {'depth': int, 'swap_count': int, 'gate_count': int}

        reward = - (result['depth'] + 0.5 * result['swap_count'])  # 可调权重
        return reward

    def get_action_space(self) -> List[Tuple[int, str]]:
        """
        返回所有合法动作（用于 baseline agent 或策略训练）：
        每个动作是 (position, rule_name)
        """
        actions = []
        for pos in range(len(self.current_gate_list)):
            for rule in self.rewrite_rules:
                actions.append((pos, rule))
        return actions


# === 以下是简单的 rewrite rule 实现 ===

def rule_hh_cancel(gates: List[Dict], pos: int) -> List[Dict]:
    """H-H cancellation: 如果 pos 和 pos+1 都是 H，且作用在同一个 qubit 上，可删除两者"""
    if pos + 1 >= len(gates):
        return gates
    g1, g2 = gates[pos], gates[pos + 1]
    if g1['name'] == 'h' and g2['name'] == 'h' and g1['qubits'] == g2['qubits']:
        return gates[:pos] + gates[pos+2:]  # 删除两者
    return gates

def rule_cxcx_cancel(gates: List[Dict], pos: int) -> List[Dict]:
    """CX-CX cancellation: 两个连续 CX，控制和目标相同，可删除"""
    if pos + 1 >= len(gates):
        return gates
    g1, g2 = gates[pos], gates[pos + 1]
    if g1['name'] == 'cx' and g2['name'] == 'cx' and g1['qubits'] == g2['qubits']:
        return gates[:pos] + gates[pos+2:]
    return gates

def rule_swap_decompose(gates: List[Dict], pos: int) -> List[Dict]:
    """将一个 SWAP 门替换为三层 CX 门"""
    if pos >= len(gates):
        return gates
    g = gates[pos]
    if g['name'] == 'swap':
        q0, q1 = g['qubits']
        new = [
            {'name': 'cx', 'qubits': [q0, q1]},
            {'name': 'cx', 'qubits': [q1, q0]},
            {'name': 'cx', 'qubits': [q0, q1]},
        ]
        return gates[:pos] + new + gates[pos+1:]
    return gates
