# circuit_graph.py

import networkx as nx
from typing import List, Dict

def build_graph_from_gate_list(gates) -> nx.DiGraph:
    G = nx.DiGraph()

    for idx, gate in enumerate(gates):
        if isinstance(gate, dict):
            # 原有的 dict 格式
            node_attr = {
                "id": idx,
                "gate": gate["gate"],
                "qubits": gate.get("qubits", []),
                "params": gate.get("params", [])
            }
        elif isinstance(gate, list):
            # Quartz 的 list 格式：["rz", ["Q0"], ["Q0", "P4"]]
            node_attr = {
                "id": idx,
                "gate": gate[0],
                "qubits": gate[1],
                "params": gate[2] if len(gate) > 2 else []
            }
        else:
            raise ValueError(f"Unsupported gate format: {gate}")

        G.add_node(idx, **node_attr)

    # 加边（默认按顺序连）
    for i in range(len(gates) - 1):
        G.add_edge(i, i + 1)

    return G
