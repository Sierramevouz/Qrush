# === Rewrite Rule Set (can be extended) ===
REWRITE_RULES = [
    {"pattern": ["h", "h"], "type": "cancel"},
    {"pattern": ["cx", "cx"], "type": "cancel"},
]

# 判断两个门是否可 rewrite（根据 pattern 匹配）
def is_rewritable(g1, g2):
    return g1[0] == g2[0] and g1[1] == g2[1] and any(
        rule["pattern"] == [g1[0], g2[0]] for rule in REWRITE_RULES
    )

# === 生成所有 1-step rewrite 变体 ===
def generate_variants(gates):
    from itertools import combinations
    variants = [gates]
    for i, j in combinations(range(len(gates)), 2):
        if is_rewritable(gates[i], gates[j]):
            new_gates = [g for k, g in enumerate(gates) if k != i and k != j]
            variants.append(new_gates)
    return variants

def is_rewritten(original, variant):
    """判断是否经过了 rewrite（即是否发生了 gate 数量变化或顺序变化）"""
    return original != variant
# === 生成所有长度为 1~3 的门序列（pattern），用于候选重写规则挖掘 ===
def all_gate_patterns(max_len=3):
    from itertools import product

    gate_set = ["h", "cx", "swap", "t", "tdg", "rz"]
    patterns = []

    for length in range(1, max_len + 1):
        for seq in product(gate_set, repeat=length):
            pattern = []
            for gate in seq:
                if gate == "h":
                    pattern.append({"name": "h", "qubits": [0]})
                elif gate == "cx":
                    pattern.append({"name": "cx", "qubits": [0, 1]})
                elif gate == "swap":
                    pattern.append({"name": "swap", "qubits": [0, 1]})
                elif gate in {"t", "tdg", "rz"}:
                    pattern.append({"name": gate, "qubits": [0]})
            patterns.append(pattern)

    return patterns
