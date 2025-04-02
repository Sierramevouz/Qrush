import sys
import os
import matplotlib.pyplot as plt
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rl_env import RewriteEnv, rule_hh_cancel, rule_cxcx_cancel, rule_swap_decompose
from q_agent import QAgent  # 使用 Q-learning 智能体


def plot_rewards(rewards, save_path=None):
    plt.figure(figsize=(8, 5))
    plt.plot(rewards, label='Episode Reward')
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.title('QAgent Reward over Episodes')
    plt.legend()
    plt.grid(True)
    if save_path:
        plt.savefig(save_path)
    plt.show()


def run_multiple_episodes(agent_class, env, n_episodes=50, verbose=False):
    rewards = []
    all_traces = []
    agent = agent_class(env)

    for ep in range(n_episodes):
        reward, trace = agent.run_episode(verbose=verbose)
        rewards.append(reward)
        all_traces.append(trace)
        if verbose:
            print(f"Episode {ep}: Reward = {reward}\n")

    return rewards, all_traces


def save_results(rewards, traces, output_dir="results"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_path = os.path.join(output_dir, f"rl_qagent_result_{timestamp}.json")
    json.dump({"rewards": rewards, "traces": traces}, open(result_path, "w"), indent=2)
    print(f"📦 Saved reward + trace results to {result_path}")


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
    rewards, traces = run_multiple_episodes(QAgent, env, n_episodes=50, verbose=False)

    print(f"✅ Finished {len(rewards)} episodes. Avg Reward = {sum(rewards)/len(rewards):.2f}")
    save_results(rewards, traces)
    plot_rewards(rewards)
