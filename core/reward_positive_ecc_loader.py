import json
from circuit_graph import build_graph_from_gate_list
from typing import List, Dict



class ECCRule:
    def __init__(self, lhs_gates: List[Dict], rhs_gates: List[Dict], name: str = ""):
        self.lhs_gates = lhs_gates
        self.rhs_gates = rhs_gates
        self.lhs_graph = build_graph_from_gate_list(lhs_gates)
        self.rhs_graph = build_graph_from_gate_list(rhs_gates)
        self.name = name

    def __repr__(self):
        return f"<ECCRule name={self.name}, lhs_len={len(self.lhs_gates)}, rhs_len={len(self.rhs_gates)}>"

def is_param_free(gates: List) -> bool:
    for gate in gates:
        if not isinstance(gate, list) or len(gate) < 1:
            continue
        if gate[0] == "add":
            return False
        if len(gate) >= 3 and gate[2]:  # gate[2] 是 output 列表
            for out in gate[2]:
                if isinstance(out, str) and out.startswith("P"):
                    return False
    return True


def load_positive_ecc_rules(json_path):
    """加载 RHS 更短且 RHS 不含参数的 ECC 规则"""
    with open(json_path, 'r') as f:
        ecc_json = json.load(f)

    raw_rules = ecc_json[1]
    rules = []

    for k, rule_variants in raw_rules.items():
        for i, variant in enumerate(rule_variants):
            lhs_gates = variant[1]
            rhs_gates = rule_variants[0][1]  # 使用第一个 RHS 变体
            if len(rhs_gates) < len(lhs_gates) and is_param_free(rhs_gates):
                rule = ECCRule(
                    name=f"{k}_v{i}",
                    lhs_gates=lhs_gates,
                    rhs_gates=rhs_gates
                )
                rules.append(rule)

    return rules

# 🧪 测试使用
if __name__ == "__main__":
    rules = load_positive_ecc_rules("../quartz/experiment/ecc_set/nam_ecc.json")
    print(f"✅ 筛选出 reward-positive ECC 规则数: {len(rules)}")
    for r in rules[:5]:
        print(f"- {r.name}: {len(r.lhs_gates)} → {len(r.rhs_gates)}")
