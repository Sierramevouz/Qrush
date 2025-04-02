import json
import os
import itertools
import time
import multiprocessing as mp
from tqdm import tqdm
import random

from rewrite_rules import is_rewritten
from ilp_scheduler import schedule_ilp
from equivalence import verify_equivalence

OUT_PATH = "auto_rules_partial.jsonl"

# ==== 生成多样性增强的 gate pattern ====
def all_gate_patterns(max_len=3, num_qubits=4):
    from itertools import product

    gate_set = ["h", "cx", "swap", "t", "tdg", "rz"]
    patterns = []

    for length in range(1, max_len + 1):
        for seq in product(gate_set, repeat=length):
            pattern = []
            for gate in seq:
                if gate in {"h", "t", "tdg", "rz"}:
                    q = random.randint(0, num_qubits - 1)
                    pattern.append({"name": gate, "qubits": [q]})
                elif gate in {"cx", "swap"}:
                    q1, q2 = random.sample(range(num_qubits), 2)
                    pattern.append({"name": gate, "qubits": [q1, q2]})
            patterns.append(pattern)
    return patterns

def write_rule(rule):
    with open(OUT_PATH, "a") as f:
        f.write(json.dumps(rule) + "\n")

def _verify_and_generate_rule(args):
    lhs, rhs, num_qubits = args
    try:
        if not verify_equivalence(lhs, rhs, num_qubits):
            return None
        sched_lhs, depth_lhs = schedule_ilp(lhs, num_qubits)
        sched_rhs, depth_rhs = schedule_ilp(rhs, num_qubits)
        if sched_lhs is None or sched_rhs is None:
            return None

        print(f"✅ Equiv pair found | Depth(lhs) = {depth_lhs}, Depth(rhs) = {depth_rhs}")

        return {
            "lhs": lhs,
            "rhs": rhs,
            "depth_reduction": depth_lhs - depth_rhs
        }

    except Exception as e:
        return None
    return None

def generate_pattern_pairs():
    patterns = all_gate_patterns()
    args_list = []
    for lhs, rhs in itertools.combinations(patterns, 2):
        all_qubits = [q for g in lhs + rhs for q in g.get("qubits", [])]
        num_qubits = max(all_qubits, default=0) + 1
        args_list.append((lhs, rhs, num_qubits))
    return args_list

if __name__ == "__main__":
    start = time.time()

    if os.path.exists(OUT_PATH):
        os.remove(OUT_PATH)

    args_list = generate_pattern_pairs()
    total = len(args_list)
    print(f"🚀 Total pattern pairs: {total}")
    print(f"🧵 Launching {mp.cpu_count()} CPU cores...")

    manager = mp.Manager()
    rule_count = manager.Value("i", 0)

    def callback(result):
        if result is not None:
            write_rule(result)
            with rule_count.get_lock():
                rule_count.value += 1
            print(f"💾 Saved rule #{rule_count.value}")

    with mp.Pool(mp.cpu_count()) as pool:
        for args in tqdm(args_list, desc="🔍 Verifying pattern pairs"):
            pool.apply_async(_verify_and_generate_rule, args=(args,), callback=callback)
        pool.close()
        pool.join()

    print(f"\n📦 Total rules saved: {rule_count.value}")
    print(f"⏱️  Elapsed time: {time.time() - start:.2f} seconds")
