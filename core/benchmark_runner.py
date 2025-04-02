import os
from core.qasm_loader import load_qasm_file_as_gate_list as load_qasm_file
from core.rl_env import RewriteEnv, rule_hh_cancel, rule_cxcx_cancel, rule_swap_decompose
from core.q_agent import QAgent
from core.rl_discriminator import DiscriminatorAgent
from core.ilp_scheduler import schedule_ilp
from core.equivalence import verify_equivalence

BENCHMARK_PATH = "../circuits"
SAVE_QASM_DIR = "../results/rewrited_qasm"
os.makedirs(SAVE_QASM_DIR, exist_ok=True)

def write_gate_list_to_qasm(gate_list, file_path):
    with open(file_path, 'w') as f:
        f.write("OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[5];\n")
        for gate in gate_list:
            name = gate['name']
            qubits = gate['qubits']
            if name in ['h', 'x', 'z', 't']:
                f.write(f"{name} q[{qubits[0]}];\n")
            elif name == 'cx':
                f.write(f"cx q[{qubits[0]}],q[{qubits[1]}];\n")

def evaluate_with_discriminator(original_gates, rewrited_gates, num_qubits):
    sched1, depth1 = schedule_ilp(original_gates, num_qubits)
    sched2, depth2 = schedule_ilp(rewrited_gates, num_qubits)
    if sched1 is None or sched2 is None:
        return -10.0
    if not verify_equivalence(original_gates, rewrited_gates, num_qubits):
        return -5.0
    gate_diff = len(original_gates) - len(rewrited_gates)
    depth_diff = depth1 - depth2
    return gate_diff + 0.5 * depth_diff  # ✨ 新 reward 设计

def run_qasm_benchmark(qasm_filename, agent_cls=QAgent, n_episode=30):
    print(f"\n🚀 Running benchmark on {qasm_filename}...")
    full_path = os.path.join(BENCHMARK_PATH, qasm_filename)
    gates, num_qubits = load_qasm_file(full_path)

    rules = {
        'hh_cancel': rule_hh_cancel,
        'cxcx_cancel': rule_cxcx_cancel,
        'swap_decompose': rule_swap_decompose,
    }

    env = RewriteEnv(gates, rules)
    agent = agent_cls(env)
    disc = DiscriminatorAgent()

    best_reward = float('-inf')
    best_gate_list = None

    for ep in range(n_episode):
        obs = env.reset()
        total_reward = 0
        done = False
        step = 0
        state = agent.encode_state(obs)

        while not done:
            action_space = env.get_action_space()
            action = agent.select_action(state, action_space)
            pos, rule = action
            next_obs, _, done, _ = env.step(pos, rule)
            next_state = agent.encode_state(next_obs)

            reward = evaluate_with_discriminator(gates, next_obs, num_qubits)
            total_reward += reward

            max_next_q = max(agent.q_table[(next_state, a)] for a in action_space) if not done else 0.0
            old_q = agent.q_table[(state, action)]
            agent.q_table[(state, action)] += agent.alpha * (reward + agent.gamma * max_next_q - old_q)

            # 🔍 打印深度差异对比
            _, depth_orig = schedule_ilp(gates, num_qubits)
            _, depth_rew = schedule_ilp(next_obs, num_qubits)
            print(f"[Step {step}] orig_depth={depth_orig}, rew_depth={depth_rew}, reward={reward:.2f}")

            state = next_state
            step += 1

        print(f"Episode {ep:2d}: Total Reward = {total_reward:.2f}\n")

        if total_reward > best_reward:
            best_reward = total_reward
            best_gate_list = env.current_gate_list

    # Save best rewrited gate list
    if best_gate_list:
        out_path = os.path.join(SAVE_QASM_DIR, f"rewrited_{qasm_filename}")
        write_gate_list_to_qasm(best_gate_list, out_path)
        print(f"✅ Saved best rewrited QASM to {out_path}")

if __name__ == '__main__':
    run_qasm_benchmark("ghz3.qasm")
    run_qasm_benchmark("qft3.qasm")
