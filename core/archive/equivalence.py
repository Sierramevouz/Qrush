from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

# ✅ 将 gate 列表转换为 Qiskit 电路
def gates_to_circuit(gates, num_qubits):
    qc = QuantumCircuit(num_qubits)
    for gate, qubits in gates:
        if gate == "h":
            qc.h(qubits[0])
        elif gate == "cx":
            qc.cx(qubits[0], qubits[1])
        elif gate == "t":
            qc.t(qubits[0])
        elif gate == "tdg":
            qc.tdg(qubits[0])
        # 其他门可以扩展
    return qc

# ✅ 核心：判断两个 gate list 是否语义等价（unitary matrix 相同）
def verify_equivalence(original_gates, transformed_gates, num_qubits):
    try:
        orig = gates_to_circuit(original_gates, num_qubits)
        trans = gates_to_circuit(transformed_gates, num_qubits)
        return Operator(orig).equiv(Operator(trans))
    except:
        return False
