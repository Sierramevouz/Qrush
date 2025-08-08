# core/matcher.py

import networkx as nx
from typing import List, Dict

def find_matches(target_graph: nx.DiGraph, pattern_graph: nx.DiGraph) -> List[Dict[int, int]]:
    """
    在 target_graph 中查找所有与 pattern_graph 同构的子图匹配。
    返回所有匹配的节点映射列表：List[Dict[pattern_node -> target_node]]
    """

    def node_match(n1, n2):
        return n1["gate"] == n2["gate"] and n1.get("qubits", []) == n2.get("qubits", [])

    matcher = nx.algorithms.isomorphism.DiGraphMatcher(
        target_graph,
        pattern_graph,
        node_match=node_match
    )
    matches = [mapping for mapping in matcher.subgraph_isomorphisms_iter()]
    return matches
