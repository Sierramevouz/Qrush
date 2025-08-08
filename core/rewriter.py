# core/rewriter.py

import networkx as nx
from typing import Dict, List
from circuit_graph import build_graph_from_gate_list


def get_param_binding(lhs_graph: nx.DiGraph, match: Dict[int, int], full_graph: nx.DiGraph) -> Dict[str, float]:
    """
    从匹配区域中提取参数绑定：将 LHS 中每个 param 如 'P4' 绑定到 full_graph 中对应 gate 的真实值
    """
    binding = {}
    for pat_node_id, tgt_node_id in match.items():
        pat_node = lhs_graph.nodes[pat_node_id]
        tgt_node = full_graph.nodes[tgt_node_id]
        if pat_node["gate"] == tgt_node["gate"] and pat_node.get("params") and tgt_node.get("params"):
            for param_name, param_val in zip(pat_node["params"], tgt_node["params"]):
                binding[param_name] = param_val  # e.g., {'P4': 1.57}
    return binding


def apply_param_binding(rhs_gate_list: List[Dict], param_binding: Dict[str, float]) -> List[Dict]:
    """
    将 RHS 中的符号参数替换为实际值
    """
    bound_rhs = []
    for gate in rhs_gate_list:
        new_gate = gate.copy()
        if gate.get("params"):
            bound_params = []
            for p in gate["params"]:
                val = param_binding.get(p, None)
                if isinstance(val, str):  # 忽略仍为符号的参数
                    bound_params.append(0.0)
                elif val is not None:
                    bound_params.append(float(val))
                else:
                    try:
                        bound_params.append(float(p))
                    except ValueError:
                        bound_params.append(0.0)
            new_gate["params"] = bound_params

        bound_rhs.append(new_gate)
    return bound_rhs


def apply_rule_at(
    target_graph: nx.DiGraph,
    match: Dict[int, int],
    rhs_gate_list: list
) -> nx.DiGraph:
    """
    在 target_graph 中将匹配的子图替换为 RHS 电路。
    - 自动绑定参数
    - 保留上下文边（前驱/后继连接）
    """
    G_new = target_graph.copy()
    nodes_to_remove = list(match.values())

    # === 1. 收集上下文边 ===
    predecessors = set()
    successors = set()
    for nid in nodes_to_remove:
        predecessors.update(G_new.predecessors(nid))
        successors.update(G_new.successors(nid))
    predecessors -= set(nodes_to_remove)
    successors -= set(nodes_to_remove)

    # === 2. 提取参数绑定 ===
    lhs_subgraph = target_graph.subgraph(nodes_to_remove)
    param_binding = get_param_binding(lhs_subgraph, {k: match[k] for k in match}, target_graph)

    # === 3. 删除旧节点 ===
    G_new.remove_nodes_from(nodes_to_remove)

    # === 4. 替换为 RHS 图（带参数）===
    bound_rhs = apply_param_binding(rhs_gate_list, param_binding)
    rhs_graph = build_graph_from_gate_list(bound_rhs)

    max_node_id = max(G_new.nodes) if G_new.nodes else -1
    rhs_id_mapping = {n: n + max_node_id + 1 for n in rhs_graph.nodes}

    rhs_entry_node = min(rhs_id_mapping.values())
    rhs_exit_node = max(rhs_id_mapping.values())

    for n, d in rhs_graph.nodes(data=True):
        G_new.add_node(rhs_id_mapping[n], **d)
    for u, v in rhs_graph.edges:
        G_new.add_edge(rhs_id_mapping[u], rhs_id_mapping[v])

    # === 5. 添加上下文连接 ===
    for p in predecessors:
        G_new.add_edge(p, rhs_entry_node)
    for s in successors:
        G_new.add_edge(rhs_exit_node, s)

    return G_new
