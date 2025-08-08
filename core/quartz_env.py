import os
import logging
from typing import Optional, List, Tuple, Dict, Any

import torch
# 确保你的环境已经安装了 torch_geometric
from torch_geometric.data import Data
import quartz  # Quartz Python binding
import numpy as np

class QuartzRLRewriteEnv:
    """
    工业级强化学习环境：基于Quartz原生Graph/ECC/Pattern接口，支持RL和超大动作空间。
    适用于Quarl、PPO、多agent等大规模RL实验。
    【已为新版 Quartz API 全面重构 - 最终版】
    """

    def __init__(
        self,
        qasm_path: str,
        ecc_path: str,
        gate_set: List[str],
        max_steps: int = 20,
        reward_metric: str = "gate_count",
        log_dir: Optional[str] = None,
        verbose: bool = False,
    ):
        self.qasm_path = qasm_path
        self.ecc_path = ecc_path
        self.gate_set_str = gate_set
        self.max_steps = max_steps
        self.reward_metric = reward_metric
        self.verbose = verbose
        self.logger = self._build_logger(log_dir)

        # -------------------- 【最终修正区域】 --------------------

        # 1. 准备 gate_set 为整数列表
        try:
            # get_gate_type_from_str() 直接返回整数
            gate_set_as_ints = [quartz.get_gate_type_from_str(s) for s in self.gate_set_str]
        except Exception as e:
            self.logger.error(f"Failed to convert gate set strings to integers: {e}")
            raise

        # 2. 使用我们通过所有错误信息最终确定的正确方式来创建 Context
        try:
            # 【关键修改】: 使用 'filename' 关键字参数, 而不是 'ecc_file'
            self.ctx = quartz.QuartzContext(
                gate_set=gate_set_as_ints,
                filename=self.ecc_path
            )
            self.logger.info("Successfully created QuartzContext with 'gate_set' and 'filename' arguments.")
            
            self.qasm_parser = quartz.PyQASMParser(context=self.ctx)
            self.logger.info("PyQASMParser initialized.")

        except Exception as e:
            self.logger.error(f"Failed to create QuartzContext/PyQASMParser: {e}")
            raise
        
        # -------------------- 【最终修正区域结束】 --------------------

        self.current_graph: Optional[quartz.PyGraph] = None
        self.init_graph: Optional[quartz.PyGraph] = None
        self.reset()

    def _build_logger(self, log_dir: Optional[str]):
        logger = logging.getLogger(f"QuartzEnv-{id(self)}")
        logger.setLevel(logging.INFO)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            fh = logging.FileHandler(os.path.join(log_dir, "env.log"))
            fh.setLevel(logging.INFO)
            logger.addHandler(fh)
        return logger

    def reset(self) -> Optional[quartz.PyGraph]:
        """重置环境，加载初始QASM，初始化Graph状态。"""
        try:
            circuit_seq = self.qasm_parser.load_qasm(filename=self.qasm_path)
            self.init_graph = quartz.PyGraph(context=self.ctx, circuit_seq=circuit_seq)
            self.current_graph = self.init_graph.clone()
            self._step_count = 0
            self._history = []
            self._last_reward = None
            self.logger.info(f"Environment reset. Initial graph gate count: {self.init_graph.gate_count}")
            return self.current_graph
        except Exception as e:
            self.logger.error(f"Reset failed: {e}")
            raise

    def get_action_space(self) -> Tuple[List[int], Dict[int, List[int]]]:
        nodes = self.current_graph.get_all_nodes()
        node_indices = [node.id for node in nodes]
        
        action_space = {}
        for node_id in node_indices:
            action_space[node_id] = self.get_applicable_transformations(node_id)
            
        return node_indices, action_space
    
    def get_applicable_transformations(self, node_id: int) -> List[int]:
        """获取一个节点上所有可用的变换规则ID"""
        try:
            node = self.current_graph.get_node_from_id(id=node_id)
            available_xfers = self.current_graph.available_xfers(context=self.ctx, node=node)
            return [xfer.id for xfer in available_xfers]
        except Exception as e:
            self.logger.error(f"Get applicable transformations for node {node_id} failed: {e}")
            return []

    def step(self, node_id: int, xfer_id: int) -> Tuple[Any, float, bool, Dict[str, Any]]:
        """执行一个动作 (在指定节点上应用指定变换)"""
        info = {}
        prev_graph = self.current_graph.clone()
        try:
            xfer = self.ctx.get_xfer_from_id(id=xfer_id)
            node = self.current_graph.get_node_from_id(id=node_id)
            new_graph = self.current_graph.apply_xfer(xfer=xfer, node=node, eliminate_rotation=False)

            if new_graph is None:
                info["apply_failed"] = True
                reward = -1.0 
                done = False
                return self.current_graph, reward, done, info

            self.current_graph = new_graph
            self._step_count += 1
            reward = self._compute_reward(prev_graph, self.current_graph)
            done = self._step_count >= self.max_steps
            self._history.append((node_id, xfer_id))
            
            info["history"] = self._history.copy()
            self._last_reward = reward
            
            return self.current_graph, reward, done, info
        except Exception as e:
            self.logger.error(f"Step failed with node_id={node_id}, xfer_id={xfer_id}: {e}")
            info["exception"] = str(e)
            return self.current_graph, -10.0, True, info

    def _compute_reward(self, prev_graph, curr_graph) -> float:
        if self.reward_metric == "gate_count":
            return float(prev_graph.gate_count - curr_graph.gate_count)
        elif self.reward_metric == "depth":
            return float(prev_graph.depth - curr_graph.depth)
        return 0.0

    def get_pyg_data(self) -> Data:
        """将当前的 Quartz PyGraph 转换为 PyTorch Geometric 的 Data 对象。"""
        nodes = self.current_graph.get_all_nodes()
        num_gates = len(nodes)
        
        supported_gate_enums = self.ctx.get_supported_gates()
        type2id = {gate_type: i for i, gate_type in enumerate(supported_gate_enums)}
        num_gate_types = len(type2id)

        features = []
        for node in nodes:
            gate_type_idx = type2id.get(node.gate.tp, -1)
            one_hot_type = torch.zeros(num_gate_types)
            if gate_type_idx != -1:
                one_hot_type[gate_type_idx] = 1
            
            features.append(one_hot_type)

        if not features:
            x = torch.empty(0, num_gate_types, dtype=torch.float)
        else:
            x = torch.stack(features)

        edge_list = self.current_graph.get_all_edges()
        if not edge_list:
            edge_index = torch.tensor([[0], [0]], dtype=torch.long) if num_gates > 0 else torch.empty(2, 0, dtype=torch.long)
        else:
            src_nodes = [edge[0] for edge in edge_list]
            dst_nodes = [edge[1] for edge in edge_list]
            edge_index = torch.tensor([src_nodes, dst_nodes], dtype=torch.long)

        return Data(x=x, edge_index=edge_index)

    def render(self, out_path: Optional[str] = None):
        qasm_str = self.current_graph.to_qasm_str()
        print(qasm_str)
        if out_path:
            with open(out_path, "w") as f:
                f.write(qasm_str)
        return qasm_str

    def export_history(self) -> List[Tuple[int, int]]:
        return self._history.copy()

    def info(self) -> Dict[str, Any]:
        return {
            "current_steps": self._step_count,
            "last_reward": self._last_reward,
            "action_history": self._history.copy(),
            "gate_count": self.current_graph.gate_count,
            "depth": self.current_graph.depth,
        }