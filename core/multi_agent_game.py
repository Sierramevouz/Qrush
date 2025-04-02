import sys
import os
import json
import matplotlib.pyplot as plt
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rl_env import RewriteEnv, rule_hh_cancel, rule_cxcx_cancel, rule_swap_decompose
from q_agent import QAgent
from rl_discriminator import DiscriminatorAgent


def plot_rewards(rewards, save_path=None):
    plt.figure(figsize=(8, 5))
    plt.plot(rewards, label='Reward (Discriminator-Adjusted)')
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.title('Multi-Agent RL Reward')
    plt.legend()
    plt.grid(True)
    if save_path:
        plt.savefig(save_path)
    plt.show()


def save_results(rewards, traces, output_dir="results"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_path = os.path.join(output_dir, f"rl_multiagent_result_{timestamp}.json")
    json.dump({"rewards": rewards, "traces": traces}, open(result_path, "w"), indent=2)
    print(f"📦 Saved reward + trace results to {result_path}")


def run_multiagent_rl(env, rewrite_agent, discriminator, n_episodes=50, verbose=False):
    rewards = []
    traces = []
    original_gates = env.original_gate_list

    for ep in range(n_episodes):
        obs = env.reset()
        state = rewrite_agent.encode_state(obs)
        done = False
        total_reward = 0
        trace = []
        step = 0

        while not done:
            actions = env.get_action_space()
            action = rewrite_agent.select_action(state, actions)
            pos, rule = action
            next_obs, _, done, info = env.step(pos, rule)
            next_state = rewrite_agent.encode_state(next_obs)

            # 由 Discriminator 判断最终奖励
            disc_reward = discriminator.evaluate(original_gates, next_obs)
            total_reward += disc_reward

            # Q-learning update
            future_q = max(rewrite_agent.q_table[(next_state, a)] for a in env.get_action_space()) if not done else 0.0
            old_q = rewrite_agent.q_table[(state, action)]
            rewrite_agent.q_table[(state, action)] += rewrite_agent.alpha * (
                disc_reward + rewrite_agent.gamma * future_q - old_q)

            if verbose:
                print(f"[Step {step}] Action: {action} | DiscReward: {disc_reward:.2f}")

            trace.append((step, pos, rule, disc_reward, info))
            state = next_state
            step += 1

        rewards.append(total_reward)
        traces.append(trace)

    return rewards, traces


if __name__ == '__main__':
    gate_list = [
        {'name': 'h', 'qubits': [0]},
        {'name': 'h', 'qubits': [0]},
        {'name': 'cx', 'qubits': [1, 2]},
        {'name': 'cx', 'qubits': [1, 2]},
        {'name': 'swap', 'qubits': [2, 3]},
    ]
    rules = {
        'hh_cancel': rule_hh_cancel,
        'cxcx_cancel': rule_cxcx_cancel,
        'swap_decompose': rule_swap_decompose,
    }

    env = RewriteEnv(gate_list, rules)
    rewrite_agent = QAgent(env, use_softmax=True, temperature=1.0)
    discriminator = DiscriminatorAgent()

    rewards, traces = run_multiagent_rl(env, rewrite_agent, discriminator, n_episodes=50, verbose=False)
    print(f"✅ Finished multi-agent training. Avg Reward = {sum(rewards)/len(rewards):.2f}")
    save_results(rewards, traces)
    plot_rewards(rewards)