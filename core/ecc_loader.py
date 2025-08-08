# ecc_loader.py

import json
from typing import List, Dict, Tuple
from circuit_graph import build_graph_from_gate_list

class ECCRule:
    def __init__(self, lhs_gates: List[Dict], rhs_gates: List[Dict], name: str = ""):
        self.lhs_gates = lhs_gates
        self.rhs_gates = rhs_gates
        self.lhs_graph = build_graph_from_gate_list(lhs_gates)
        self.rhs_graph = build_graph_from_gate_list(rhs_gates)
        self.name = name

    def __repr__(self):
        return f"<ECCRule name={self.name}, lhs_len={len(self.lhs_gates)}, rhs_len={len(self.rhs_gates)}>"

def parse_gate(raw_gate: List) -> Dict:
    gate_name, inputs, outputs = raw_gate
    qubits = [int(q[1:]) for q in inputs if q.startswith("Q")]
    params = [p for p in outputs if p.startswith("P")] if outputs else []
    return {
        "gate": gate_name,
        "qubits": qubits,
        "params": params if params else None
    }

def load_ecc_from_json(path: str) -> List[ECCRule]:
    with open(path, "r") as f:
        data = json.load(f)

    rule_list = []
    ecc_dict = data[1]  # skip metadata, take rules

    for idx, (key, variants) in enumerate(ecc_dict.items()):
        if len(variants) < 2:
            continue  # need at least lhs + rhs

        lhs_variants = variants[:-1]
        rhs_variant = variants[-1][1]  # only use gate seq

        for i, (meta, lhs_seq) in enumerate(lhs_variants):
            lhs_gates = [parse_gate(g) for g in lhs_seq]
            rhs_gates = [parse_gate(g) for g in rhs_variant]
            rule = ECCRule(lhs_gates, rhs_gates, name=f"{key}_v{i}")
            rule_list.append(rule)

    return rule_list
