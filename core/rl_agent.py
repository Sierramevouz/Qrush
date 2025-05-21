
import random
from gnn_discriminator.score_interface import score_rule

class RandomAgent:
    """
    一个最简单的 baseline agent：从环境的 action_space 中随机选择一个动作。
    接入 GNN 判别器，使用 score_rule(lhs, rhs) 作为 reward。
    """
    def __init__(self, env):
        self.env = env

    def select_action(self):
        action_space = self.env.get_action_space()
        return random.choice(action_space)

    def run_episode(self, verbose=False):
        obs = self.env.reset()
        done = False
        total_reward = 0
        step = 0
        trace = []

        while not done:
            pos, rule_name = self.select_action()
            lhs_before = list(self.env.gate_list)  # 深拷贝避免被改动
            obs, _, done, info = self.env.step(pos, rule_name)
            rhs_after = list(self.env.gate_list)

            reward = score_rule(lhs_before, rhs_after)  # 来自 GNN 判别器
            trace.append((step, pos, rule_name, reward, info))

            if verbose:
                print(f"[Step {step}] Apply {rule_name} at {pos} | Reward: {reward:.4f} | Info: {info}")
            step += 1
            total_reward += reward

        return total_reward, trace