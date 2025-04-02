import os
import json
from collections import Counter
from core.qasm_loader import load_qasm_file_as_gate_list

# 提取连续子串（sliding window）
def extract_patterns(gate_list, window_sizes=(2, 3, 4)):
    patterns = []
    for w in window_sizes:
        for i in range(len(gate_list) - w + 1):
            sub = gate_list[i:i+w]
            patterns.append(json.dumps(sub))  # 转为字符串方便计数
    return patterns


def load_all_qasm_circuits(qasm_dir="../circuits"):
    circuits = []
    for fname in os.listdir(qasm_dir):
        if fname.endswith(".qasm"):
            path = os.path.join(qasm_dir, fname)
            gate_list, _ = load_qasm_file_as_gate_list(path)
            circuits.append((fname, gate_list))
    return circuits


def extract_frequent_patterns(min_freq=2):
    circuits = load_all_qasm_circuits()
    pattern_counter = Counter()

    for fname, gate_list in circuits:
        patterns = extract_patterns(gate_list)
        pattern_counter.update(patterns)

    # 过滤高频 pattern
    frequent = [
        {"pattern": json.loads(p), "count": c}
        for p, c in pattern_counter.items()
        if c >= min_freq
    ]
    return sorted(frequent, key=lambda x: -x["count"])


def save_patterns(frequent_patterns, path="extracted_rules.json"):
    with open(path, "w") as f:
        json.dump(frequent_patterns, f, indent=2)
    print(f"✅ Saved {len(frequent_patterns)} frequent patterns to {path}")


if __name__ == '__main__':
    print("🔍 Extracting frequent gate patterns from benchmark QASM files...")
    patterns = extract_frequent_patterns(min_freq=2)
    save_patterns(patterns)
