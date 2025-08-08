import random
import math
from collections import defaultdict

class QAgent:
    """
    基于 tabular Q-learning 的智能体，可使用 softmax 或 ε-greedy 策略选择动作。
    状态以 gate_list 的摘要形式编码为 hashable key。
    """
    def __init__(self, env, alpha=0.1, gamma=0.95, epsilon=0.1, use_softmax=False, temperature=1.0):
        self.env = env
        self.q_table = defaultdict(float)  # key: (state_str, action), value: Q-value
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.use_softmax = use_softmax
        self.temperature = temperature

    def encode_state(self, gate_list):
        # 简单状态编码方式：只取 gate 类型作为状态 key（可以更复杂）
        return tuple(g['name'] for g in gate_list)

    def select_action(self, state, actions):
        if self.use_softmax:
            return self.select_softmax_action(state, actions)
        elif random.random() < self.epsilon:
            return random.choice(actions)
        else:
            return self.select_greedy_action(state, actions)

    def select_greedy_action(self, state, actions):
        q_values = [self.q_table[(state, a)] for a in actions]
        max_q = max(q_values)
        best_actions = [a for a, q in zip(actions, q_values) if q == max_q]
        return random.choice(best_actions)

    def select_softmax_action(self, state, actions):
        q_values = [self.q_table[(state, a)] for a in actions]
        max_q = max(q_values)
        exp_q = [math.exp((q - max_q) / self.temperature) for q in q_values]  # 稳定版本
        sum_exp_q = sum(exp_q)
        probs = [v / sum_exp_q for v in exp_q]
        return random.choices(actions, weights=probs, k=1)[0]

    def run_episode(self, verbose=False):
        state = self.encode_state(self.env.reset())
        done = False
        total_reward = 0
        trace = []
        step = 0

        while not done:
            actions = self.env.get_action_space()
            action = self.select_action(state, actions)
            pos, rule = action
            next_obs, reward, done, info = self.env.step(pos, rule)
            next_state = self.encode_state(next_obs)
            total_reward += reward

            # Q-learning 更新
            future_q = max(self.q_table[(next_state, a)] for a in self.env.get_action_space()) if not done else 0.0
            old_q = self.q_table[(state, action)]
            self.q_table[(state, action)] += self.alpha * (reward + self.gamma * future_q - old_q)

            if verbose:
                print(f"[Step {step}] Action: {action} | Reward: {reward:.2f} | Next State: {next_state}")

            trace.append((step, pos, rule, reward, info))
            state = next_state
            step += 1

        return total_reward, trace
