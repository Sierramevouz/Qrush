import argparse
import os
from core.qasm_loader import load_qasm_file_as_gate_list
from core.variant_analysis import analyze_variants
from core.gantt_plot import draw_gantt
from config import MAX_REWRITE_DEPTH, BEAM_WIDTH, ENABLE_EQUIVALENCE_CHECK
from core.topology import AVAILABLE_TOPOLOGIES, build_coupling_graph, compute_distance_matrix
from qiskit import QuantumCircuit, transpile

def run_pipeline(qasm_path, coupling_name, use_parallel=True):
    print("🔁 Loading circuit:", qasm_path)
    gates, num_qubits = load_qasm_file_as_gate_list(qasm_path)

    # === 拓扑结构加载 ===
    if coupling_name not in AVAILABLE_TOPOLOGIES:
        print(f"❌ Unknown coupling: {coupling_name}")
        print("Available options:", list(AVAILABLE_TOPOLOGIES.keys()))
        return
    coupling_edges = AVAILABLE_TOPOLOGIES[coupling_name]
    coupling_graph = build_coupling_graph(coupling_edges)
    distance_matrix = compute_distance_matrix(coupling_graph)
    print(f"🔗 Using hardware topology '{coupling_name}' with {len(coupling_edges)} edges.")

    # === Qiskit Baseline
    print("\n📏 Running Qiskit transpiler baseline...")
    qc = QuantumCircuit(num_qubits)
    for g, qlist in gates:
        if g == "h": qc.h(qlist[0])
        elif g == "cx": qc.cx(qlist[0], qlist[1])
        elif g == "t": qc.t(qlist[0])
        elif g == "tdg": qc.tdg(qlist[0])
        elif g == "rz": qc.rz(3.1415 * 0.25, qlist[0])  # placeholder
    depth_qiskit_0 = transpile(qc, optimization_level=0).depth()
    depth_qiskit_3 = transpile(qc, optimization_level=3).depth()
    print(f"✅ Qiskit depth (level=0): {depth_qiskit_0}")
    print(f"✅ Qiskit depth (level=3): {depth_qiskit_3}")

    # === Rewrite + ILP 调度 + 评估 ===
    circuit_name = os.path.splitext(os.path.basename(qasm_path))[0]
    report_csv_path = f"results/{circuit_name}_variant_report.csv"
    print(f"\n🔍 Running rewrite variant analysis (depth={MAX_REWRITE_DEPTH}, beam={BEAM_WIDTH})...")
    result = analyze_variants(gates, num_qubits, csv_path=report_csv_path,
                              coupling_graph=coupling_graph,
                              distance_matrix=distance_matrix,
                              use_parallel=use_parallel)

    if result is None:
        print("❌ No valid equivalent rewrite variant found.")
        return

    print(f"\n✅ Best rewrite schedule depth = {result['depth']}")
    print(f"🔀 Estimated SWAP Cost (non-adjacent CX): {result['swap_cost']}")
    for i in sorted(result["sched"], key=lambda k: result["sched"][k]):
        g = result["gates"][i]
        print(f"  t={result['sched'][i]}: {g[0].upper()} q{g[1]}")

    if ENABLE_EQUIVALENCE_CHECK:
        print("\n🧪 Verifying unitary equivalence...")
        from core.equivalence import verify_equivalence
        eq = verify_equivalence(gates, result["gates"], num_qubits)
        print("✅ Verified!" if eq else "❌ NOT equivalent!")

    # Draw Gantt Chart
    print("\n📊 Drawing Gantt chart for best schedule...")
    draw_gantt(result["sched"], result["gates"], num_qubits,
               title=f"{circuit_name} - Best ILP Schedule",
               filename=f"results/{circuit_name}_best_gantt.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--qasm", type=str, required=True, help="Path to .qasm file")
    parser.add_argument("--coupling", type=str, default="ibmq_tokyo_7", help="Hardware topology")
    parser.add_argument("--no-parallel", action="store_true", help="Disable multiprocessing")
    args = parser.parse_args()

    run_pipeline(args.qasm, args.coupling, use_parallel=not args.no_parallel)
