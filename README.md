
# 🔧 QRANE: Quantum Rewrite And Scheduling Engine

A modular framework for **quantum circuit rewrite + ILP-based scheduling**, equipped with beam search, unitary equivalence verification, swap cost modeling, and hardware-aware optimization.

## 🚀 Overview

QRANE is a research-oriented toolkit for **automated optimization of quantum circuits**. It supports:

- ✅ Multi-step circuit rewrite with beam search
- ✅ ILP scheduling under **hardware topology constraints**
- ✅ Analysis of rewrite variants with unitary verification
- ✅ Swap cost estimation and Gantt chart visualization
- ✅ CLI interface with flexible `--mode` and `--coupling` control

---

## 🧱 Project Structure

```
quantum_rewriter_project/
├── circuits/                 # 存放 QASM benchmark 电路
│   ├── qft3.qasm
│   └── ghz3.qasm
├── core/                    # 核心功能模块
│   ├── __init__.py
│   ├── bfs_search.py        # ✅ [预留] Beam Search 重写逻辑（当前为空）
│   ├── equivalence.py       # ✅ 单位矩阵等价性验证
│   ├── gantt_plot.py        # ✅ Gantt 调度可视化工具
│   ├── ilp_scheduler.py     # ✅ ILP 调度器（支持 SWAP 成本 + 拓扑约束）
│   ├── qasm_loader.py       # ✅ QASM 解析为 gate 列表
│   ├── rewrite_graph.py     # ✅ 多步 rewrite chain 搜索（BFS/Beam Search）
│   ├── rewrite_rules.py     # ✅ 重写规则定义与 apply 工具
│   ├── rule_miner.py        # ✅ [预留] Rewrite Rule 自动挖掘模块（当前为空）
│   ├── topology.py          # ✅ 拓扑建模 + 距离矩阵计算
│   └── variant_analysis.py  # ✅ 重写等价变体 + ILP 调度分析
├── results/                 # 输出调度图与报告
│   ├── qft3_variant_report.csv
│   └── qft3_best_gantt.png
├── config.py                # ✅ 全局配置文件（拓扑选择、调度参数等）
├── main.py                  # ✅ 主入口，支持多种 mode 与拓扑选择
└── README.md                # ✅ 项目文档

```

---

## ⚙️ Features Implemented

### ✅ Circuit Input + Rewrite

- Load `.qasm` files as gate sequences
- Support basic gate set: `h`, `cx`, `t`, `tdg`, `rz`
- Beam search for **multi-step rewrite exploration** (configurable depth/width)

### ✅ ILP-based Scheduling

- ILP formulation with minimum depth objective
- Avoid gate conflicts via qubit usage constraints
- Modular `safe()` helper to handle cvxpy values robustly

### ✅ Hardware-Aware Optimization

- 🧠 Load hardware topology from `config.py` or CLI `--coupling`
- 🔗 Build coupling graph and compute **qubit distance matrix**
- 🌀 Penalize non-adjacent 2-qubit `CX` gates via `swap_cost`
- Estimate total swap cost for each variant during scheduling

### ✅ Evaluation Tools

- ✅ Unitary equivalence verification with `qiskit.quantum_info`
- 📝 Save rewrite variant reports to CSV
- 📊 Gantt chart rendering (PNG) with clear gate-timeline view

---

## 🧪 Example Run

```bash
python3 main.py --qasm circuits/qft3.qasm --mode beam --coupling ibmq_tokyo_7
```

### CLI Parameters

| Flag           | Description                                           |
|----------------|-------------------------------------------------------|
| `--qasm`       | Path to QASM file                                     |
| `--mode`       | `beam` (default) or `full` for variant analysis       |
| `--coupling`   | Topology ID from `config.py` (e.g., `fully_connected`, `ibmq_tokyo_7`, `grid_3x3`) |

---

## 🔬 Current Progress Summary

### ✅ Finished

- [x] QASM loader + gate parser
- [x] Basic rewrite rules + multi-step search
- [x] BFS + beam search on rewrite graph
- [x] ILP scheduling for minimal depth
- [x] Penalty modeling for swap cost (via topology distance)
- [x] Topology loading & CLI `--coupling` support
- [x] Equivalence verification
- [x] Gantt chart + SWAP count output
- [x] Mode switch: `full` (variant enumeration) vs `beam` (large-scale)

### 📌 Current Output Example

```
🥇 Best Variant = 79, Depth = 73, Rewritten = True
🔀 Estimated SWAP Cost (non-adjacent CX): 64.0
✅ Verified Unitary Equivalence
📊 Gantt chart saved to results/qft3_best_gantt.png
```

---

## 🔭 Phase 2: Upcoming Work

| Task | Description |
|------|-------------|
| 🧩 **Rewrite Rule Auto-Mining** | Automatically learn candidate rules from circuit patterns |
| 🌀 **Parametric Rewrite** | Generalize rules like `RZ(θ1) + RZ(θ2) → RZ(θ1+θ2)` |
| 🔁 **RL/ML Integration** | Use reinforcement learning to guide rewrite + scheduling decisions |
| ⚖️ **Topology-Aware Rewrite Rules** | Discard rules that violate physical topology |
| 🧠 **Symbolic Rewrite Checking** | Integrate Z3 or SMT solvers for safe equivalence verification |
| 📊 **Benchmark Evaluation Suite** | Add QESO, Quarl, QGO-style baseline comparisons |

---

## ✨ Vision
