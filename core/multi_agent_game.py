import os
import sys
import json
import random
from datetime import datetime
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import CouplingMap, InstructionDurations

# 添加路径支持
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "gnn_discriminator")))

from rl_env import (
    RewriteEnv,
    rule_hh_cancel,
    rule_cxcx_cancel,
    rule_swap_decompose,
    auto_load_mined_rules,
)
from q_agent import QAgent
from rl_discriminator import GNNDiscriminatorAgent
from qasm_loader import load_qasm_file_as_gate_list

# === ✅ 电路调度深度辅助函数 ===
IBMQ_TORONTO_COUPLING = CouplingMap(couplinglist=[
    [0, 1], [1, 2], [2, 3], [3, 4],
    [2, 5], [5, 6], [6, 7], [7, 8], [8, 9],
    [5, 10], [10, 11], [11, 12], [12, 13], [13, 14],
    [10, 15], [15, 16], [16, 17], [17, 18], [18, 19]
])

DEFAULT_DURATIONS = InstructionDurations([
    ("h", [0], 1),
    ("x", [0], 1),
    ("rz", [0], 1),
    ("rx", [0], 1),
    ("ry", [0], 1),
    ("cx", [0, 1], 7)
])

def gate_list_to_qiskit_circuit(gate_list):
    qubits_set = set()
    for gate in gate_list:
        if isinstance(gate, dict):
            qubits_set.update(gate.get("qubits", []))
        elif isinstance(gate, tuple):
            qubits_set.update(gate[1:])
    num_qubits = max(qubits_set) + 1 if qubits_set else 1
    qc = QuantumCircuit(num_qubits)

    for gate in gate_list:
        if isinstance(gate, dict):
            name = gate["name"]
            qubits = gate.get("qubits", [])
            params = gate.get("params", [])
        else:
            name, *qubits = gate
            params = []

        if name in {"rz", "rx", "ry"}:
            if len(params) >= 1 and len(qubits) >= 1:
                try:
                    getattr(qc, name)(params[0], qubits[0])
                except Exception as e:
                    print(f"\u26a0\ufe0f QuantumCircuit.{name}({params[0]}, {qubits[0]}) 失败: {e}")
                continue
            else:
                print(f"\u26a0\ufe0f 无效参数门：{gate}")
                continue

        try:
            getattr(qc, name)(*params, *qubits)
        except Exception as e:
            print(f"\u26a0\ufe0f QuantumCircuit.{name}({params}, {qubits}) 失败: {e}")
            continue
    return qc

def get_schedule_depth(gate_list, coupling_map="toronto"):
    try:
        qc = gate_list_to_qiskit_circuit(gate_list)
        if coupling_map == "toronto" and qc.num_qubits <= 20:
            cmap = IBMQ_TORONTO_COUPLING
        else:
            cmap = CouplingMap.from_full(qc.num_qubits)
        transpiled = transpile(
            qc,
            optimization_level=1,
            coupling_map=cmap,
            scheduling_method="alap",
            instruction_durations=DEFAULT_DURATIONS
        )
        return transpiled.depth()
    except Exception as e:
        print(f"[\u26a0\ufe0f] 调度失败：{e}")
        return None

# === ✅ 加载一个 QASM 电路（用于调试） ===
circuit_dir = "../circuits"
all_qasm_paths = [os.path.join(circuit_dir, f) for f in os.listdir(circuit_dir) if f.endswith(".qasm")]
random.shuffle(all_qasm_paths)

# === ✅ 加载 rewrite rule 和 GNN 判别器 ===
rules = {
    'hh_cancel': rule_hh_cancel,
    'cxcx_cancel': rule_cxcx_cancel,
    'swap_decompose': rule_swap_decompose,
    **auto_load_mined_rules(),
}
discriminator = GNNDiscriminatorAgent(model_path="gnn_discriminator/gnn_discriminator_weights.pt")

# === ✅ 只跑一个电路（便于调试） ===
reward_trace = []
all_traces = []

qasm_path = all_qasm_paths[0]
gate_list, _ = load_qasm_file_as_gate_list(qasm_path)
env = RewriteEnv(gate_list, rewrite_rules=rules, discriminator=discriminator)
agent = QAgent(env, use_softmax=True, temperature=1.0)

obs = env.reset()
state = agent.encode_state(obs)
total_reward = 0
trace = []
done = False

while not done:
    actions = env.get_action_space()
    action = agent.select_action(state, actions)
    pos, rule = action

    next_obs, _, done, info = env.step(pos, rule)
    next_state = agent.encode_state(next_obs)

    lhs = info.get("before", obs)
    rhs = info.get("after", next_obs)

    gnn_reward = discriminator.evaluate(lhs, rhs)
    depth_before = get_schedule_depth(lhs)
    depth_after = get_schedule_depth(rhs)
    if depth_before is not None and depth_after is not None:
        depth_reward = depth_before - depth_after
    else:
        depth_reward = 0

    reward = gnn_reward + 0.1 * depth_reward
    total_reward += reward

    future_q = max(agent.q_table.get((next_state, a), 0.0) for a in actions) if not done else 0.0
    old_q = agent.q_table.get((state, action), 0.0)
    agent.q_table[(state, action)] = old_q + agent.alpha * (reward + agent.gamma * future_q - old_q)

    trace.append({
        "pos": pos,
        "rule": rule,
        "gnn_reward": gnn_reward,
        "depth_reward": depth_reward,
        "total": reward,
        "depth_before": depth_before,
        "depth_after": depth_after
    })
    state = next_state

    print(f"[Debug] Action: ({pos}, '{rule}') | GNN={gnn_reward:.2f}, Depth∆={depth_reward}, Reward={reward:.2f}")

reward_trace.append(total_reward)
all_traces.append(trace)

# === ✅ 保存结果 ===
save_dir = "results"
os.makedirs(save_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
save_path = os.path.join(save_dir, f"rl_gnn_depth_debug_{timestamp}.json")

result = {
    "reward_trace": reward_trace,
    "traces": all_traces,
    "qasm_path": qasm_path
}
with open(save_path, "w") as f:
    json.dump(result, f, indent=2)
print(f"\n📦 Saved debug result to {save_path}")
