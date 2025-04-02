class DiscriminatorAgent:
    """
    裁判智能体：评估 rewrited 电路是否有效，给予正/负奖励。
    可用于多智能体博弈中的 reward shaping。
    """
    def __init__(self, baseline_gate_count=None, reward_positive=1.0, reward_negative=-1.0):
        self.baseline_gate_count = baseline_gate_count  # 可选：初始化时设定一个参照门数
        self.reward_positive = reward_positive
        self.reward_negative = reward_negative

    def evaluate(self, original_gate_list, rewrited_gate_list) -> float:
        """
        评估 rewrited 电路是否值得奖励：
        - 如果 rewrited gate 数量减少，则给正奖励
        - 否则给予负奖励
        可扩展为接入等价性验证、调度深度比较等复杂评估
        """
        original_len = len(original_gate_list)
        rewrited_len = len(rewrited_gate_list)

        if self.baseline_gate_count is not None:
            base = self.baseline_gate_count
        else:
            base = original_len

        if rewrited_len < base:
            return self.reward_positive
        else:
            return self.reward_negative

    def update_baseline(self, new_gate_list):
        self.baseline_gate_count = len(new_gate_list)
