import json
import torch
from tqdm import tqdm
from score_rule import score_rule
from data_utils import build_graph_from_gate_list

# ==== 配置路径 & 筛选参数 ====
INPUT_PATH = "converted_ecc_rules_with_labels.jsonl"
OUTPUT_PATH = "high_score_rules.jsonl"
SCORE_THRESHOLD = 0.9
USE_LABEL_FILTER = True  # ✅ 只保留 label==1.0 的正样本（更可靠）

# ==== 模型参数 ====
model_path = "gnn_discriminator_weights.pt"
device = "cuda" if torch.cuda.is_available() else "cpu"


def is_valid_rule(rule):
    try:
        lhs_graph = build_graph_from_gate_list(rule["lhs"])
        rhs_graph = build_graph_from_gate_list(rule["rhs"])
        score = score_rule(lhs_graph, rhs_graph, model_path=model_path, device=device)
        if score >= SCORE_THRESHOLD:
            return True, score
        return False, score
    except Exception as e:
        print(f"[⚠️] Skip invalid rule: {e}")
        return False, -1.0


def main():
    with open(INPUT_PATH, "r") as fin, open(OUTPUT_PATH, "w") as fout:
        count_total = 0
        count_selected = 0

        for line in tqdm(fin, desc="🧪 Scanning rule dataset..."):
            try:
                rule = json.loads(line)
                if USE_LABEL_FILTER and rule.get("label", 0.0) != 1.0:
                    continue

                is_valid, score = is_valid_rule(rule)
                if is_valid:
                    rule["gnn_score"] = score
                    fout.write(json.dumps(rule) + "\n")
                    count_selected += 1
                count_total += 1
            except:
                continue

        print(f"\n📊 Total scanned: {count_total}")
        print(f"✅ Selected with score ≥ {SCORE_THRESHOLD}: {count_selected}")
        print(f"📁 Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
