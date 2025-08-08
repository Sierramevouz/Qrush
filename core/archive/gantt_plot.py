import matplotlib.pyplot as plt
from core.ilp_scheduler import safe

def draw_gantt(schedule, gates, num_qubits=3, title="Schedule", filename="gantt.png"):
    fig, ax = plt.subplots(figsize=(10, 4))
    colors = ["skyblue", "orange", "green", "red", "purple", "gray"]
    
    for i, (gate, qubits) in enumerate(gates):
        t_i = safe(schedule.get(i, None))
        if t_i < 0:
            continue
        for q in qubits:
            ax.broken_barh([(t_i, 1)], (q * 1.2, 1),
                           facecolors=colors[i % len(colors)])
            ax.text(t_i + 0.1, q * 1.2 + 0.5, gate.upper(), fontsize=8)

    ax.set_xlabel("Time Step")
    ax.set_ylabel("Qubit")
    ax.set_title(title)
    ax.set_yticks([q * 1.2 + 0.5 for q in range(num_qubits)])
    ax.set_yticklabels([f"q[{q}]" for q in range(num_qubits)])
    ax.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
