import copy
from typing import List, Dict, Tuple

# === ✅ 自动加载 mined_rewrite_rules 中的所有函数 ===
def auto_load_mined_rules():
    import importlib.util
    import os

    # 动态导入 gnn_discriminator/mined_rewrite_rules.py
    base_path = os.path.dirname(os.path.dirname(__file__))  # 到 quantum_rewriter_project/
    mined_path = os.path.join(base_path, "gnn_discriminator", "mined_rewrite_rules.py")

    spec = importlib.util.spec_from_file_location("mined_rewrite_rules", mined_path)
    mined_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mined_module)

    # 收集所有以 rule_ 开头的函数
    rule_funcs = {
        name: func
        for name, func in vars(mined_module).items()
        if callable(func) and name.startswith("rule_")
    }

    print(f"✅ Loaded {len(rule_funcs)} auto-mined rules from mined_rewrite_rules.py")
    return rule_funcs


class RewriteEnv:
    """
    强化学习环境：给定一个初始电路（gate list），允许 agent 对 gate 应用 rewrite rule，输出 rewrited gate list。
    每一步可以由 agent 决定是否对某个位置的 gate 应用某个 rule。
    环境将维护当前电路状态，并在必要时计算调度性能作为 reward。
    """

    def __init__(self, gate_list: List[Dict], rewrite_rules: Dict[str, callable], discriminator=None):
        self.original_gate_list = copy.deepcopy(gate_list)
        self.rewrite_rules = rewrite_rules
        self.discriminator = discriminator
        self.reset()

    def reset(self):
        self.current_gate_list = copy.deepcopy(self.original_gate_list)
        self.step_count = 0
        self.rewrite_trace = []
        return self._get_obs()

    def _get_obs(self) -> List[Dict]:
        return self.current_gate_list

    def step(self, position: int, rule_name: str) -> Tuple[List[Dict], float, bool, Dict]:
        self.step_count += 1
        info = {}
        info['before'] = copy.deepcopy(self.current_gate_list)

        if rule_name not in self.rewrite_rules:
            raise ValueError(f"Unknown rewrite rule: {rule_name}")

        try:
            new_gates = self.rewrite_rules[rule_name](self.current_gate_list, position)
            # === ✅ Debug 输出中间 gate list ===
            for i, g in enumerate(new_gates):
                if isinstance(g, dict) and g.get("name") == "rz" and ("params" not in g or not g["params"]):
                    print(f"[⚠️ Debug] Step {self.step_count} → Rule '{rule_name}' produced invalid rz gate at pos {i}: {g}")

            self.current_gate_list = new_gates
            self.rewrite_trace.append((position, rule_name))
        except Exception as e:
            info['error'] = str(e)

        info['after'] = copy.deepcopy(self.current_gate_list)
        done = self.step_count >= 10
        reward = self.compute_reward() if done else 0.0
        return self._get_obs(), reward, done, info

    def compute_reward(self) -> float:
        if self.discriminator is not None:
            return self.discriminator.evaluate(self.original_gate_list, self.current_gate_list)

        from variant_analysis import evaluate_gate_list
        result = evaluate_gate_list(self.current_gate_list)
        reward = - (result['depth'] + 0.5 * result['swap_count'])
        return reward

    def get_action_space(self) -> List[Tuple[int, str]]:
        actions = []
        for pos in range(len(self.current_gate_list)):
            for rule in self.rewrite_rules:
                actions.append((pos, rule))
        return actions


# === ✅ 内置的简单 rewrite rule（人工规则） ===

def rule_hh_cancel(gates: List[Dict], pos: int) -> List[Dict]:
    if pos + 1 >= len(gates):
        return gates
    g1, g2 = gates[pos], gates[pos + 1]
    if g1['name'] == 'h' and g2['name'] == 'h' and g1['qubits'] == g2['qubits']:
        return gates[:pos] + gates[pos+2:]
    return gates

def rule_cxcx_cancel(gates: List[Dict], pos: int) -> List[Dict]:
    if pos + 1 >= len(gates):
        return gates
    g1, g2 = gates[pos], gates[pos + 1]
    if g1['name'] == 'cx' and g2['name'] == 'cx' and g1['qubits'] == g2['qubits']:
        return gates[:pos] + gates[pos+2:]
    return gates

def rule_swap_decompose(gates: List[Dict], pos: int) -> List[Dict]:
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
