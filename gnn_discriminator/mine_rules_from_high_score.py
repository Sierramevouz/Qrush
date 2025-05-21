import json
import hashlib
from collections import Counter, defaultdict
from tqdm import tqdm

INPUT_FILE = "high_score_rules.jsonl"
OUTPUT_FILE = "mined_rewrite_rules.py"
TOP_K = 30  # 提取前 K 个高频 rewrite pattern


def list_gate_to_dict(gate_list):
    """
    修复 gate 结构解析，保留 qubits 和 params。
    原格式：["rz", ["Q0"], ["Q0", "P1"]] → {"name": "rz", "qubits": [0], "params": ["P1"]}
    """
    converted = []
    for gate in gate_list:
        if isinstance(gate, list) and len(gate) >= 3:
            name = gate[0].lower()

            q_args = [q for q in gate[1] if isinstance(q, str) and q.startswith("Q")]
            p_args = [p for p in gate[2] if isinstance(p, str) and p.startswith("P")]

            qubits = [int(q[1:]) for q in q_args]
            params = [p for p in p_args]

            gate_dict = {"name": name, "qubits": qubits}
            if params:
                gate_dict["params"] = params  # ✅ 保留参数
            converted.append(gate_dict)
    return converted


def hash_gate_list(gates):
    """
    对 gate list 做结构性哈希，便于识别重复 rewrite pattern
    """
    gate_strs = [f"{g.get('name')}:{','.join(map(str, g.get('qubits', [])))}" for g in gates]
    return hashlib.md5("|".join(gate_strs).encode()).hexdigest()


def main():
    print(f"📥 Loading high score rules from {INPUT_FILE}...")
    pattern_counter = Counter()
    pattern_examples = defaultdict(list)

    with open(INPUT_FILE, "r") as f:
        for line in tqdm(f, desc="🔍 Scanning rules"):
            rule = json.loads(line)
            lhs_raw, rhs_raw = rule["lhs"], rule["rhs"]
            lhs = list_gate_to_dict(lhs_raw)
            rhs = list_gate_to_dict(rhs_raw)

            lhs_hash = hash_gate_list(lhs)
            rhs_hash = hash_gate_list(rhs)
            key = f"{lhs_hash}→{rhs_hash}"
            pattern_counter[key] += 1
            if len(pattern_examples[key]) < 1:
                pattern_examples[key] = (lhs, rhs)

    top_patterns = pattern_counter.most_common(TOP_K)

    print(f"✅ Top {TOP_K} rules selected. Saving to {OUTPUT_FILE}...")

    with open(OUTPUT_FILE, "w") as fout:
        fout.write("# ✅ Auto-mined rewrite rules from high-score GNN pairs\n")
        fout.write("from typing import List, Dict\n\n")

        for idx, (key, count) in enumerate(top_patterns):
            rule_name = f"rule_{idx:03d}"
            lhs, rhs = pattern_examples[key]

            fout.write(f"def {rule_name}(gates: List[Dict], pos: int) -> List[Dict]:\n")
            fout.write(f"    \"\"\"Auto-mined rule #{idx+1} | support count = {count}\"\"\"\n")
            fout.write(f"    pattern = {json.dumps(lhs, indent=4)}\n")
            fout.write(f"    replacement = {json.dumps(rhs, indent=4)}\n")
            fout.write("    if gates[pos:pos+len(pattern)] == pattern:\n")
            fout.write("        return gates[:pos] + replacement + gates[pos+len(pattern):]\n")
            fout.write("    return gates\n\n")

    print("✅ Done! You can now `import mined_rewrite_rules` and use them in RL env.")


if __name__ == "__main__":
    main()
