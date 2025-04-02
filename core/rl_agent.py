import random

class RandomAgent:
    """
    一个最简单的 baseline agent：从环境的 action_space 中随机选择一个动作。
    可用于测试 RewriteEnv 流程是否通畅。
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
            pos, rule = self.select_action()
            obs, reward, done, info = self.env.step(pos, rule)
            trace.append((step, pos, rule, reward, info))
            if verbose:
                print(f"[Step {step}] Apply {rule} at {pos} | Reward: {reward:.2f} | Info: {info}")
            step += 1
        total_reward += reward

        return total_reward, trace
