from qiskit import QuantumCircuit

def from_qiskit_to_gate_list(qc: QuantumCircuit):
    gate_list = []
    for inst, qargs, _ in qc.data:
        name = inst.name
        qubits = [q._index for q in qargs]
        if name in {"h", "cx", "t", "tdg", "rz"}:
            gate_list.append({"name": name, "qubits": qubits})  # ✅ 返回字典格式
    return gate_list, qc.num_qubits


def load_qasm_file_as_gate_list(path):
    qc = QuantumCircuit.from_qasm_file(path)
    return from_qiskit_to_gate_list(qc)
