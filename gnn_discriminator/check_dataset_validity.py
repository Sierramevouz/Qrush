import json
from tqdm import tqdm
from robust_graph_utils import robust_convert_gate_list_to_graph

DATASET_PATH = "converted_ecc_rules_with_labels.jsonl"

def check_dataset(path, name):
    total = 0
    invalid_graph = 0
    invalid_label = 0
    label_counts = {0.0: 0, 1.0: 0, "other": 0}

    print(f"\n🔍 Checking {name} dataset...")
    with open(path, "r") as f:
        for line in tqdm(f, desc=f"Checking {name}"):
            total += 1
            try:
                rule = json.loads(line)
                label = rule.get("label", None)

                # ✅ 检查 label 是否为 0.0 或 1.0
                if label == 0.0:
                    label_counts[0.0] += 1
                elif label == 1.0:
                    label_counts[1.0] += 1
                else:
                    label_counts["other"] += 1
                    invalid_label += 1

                # ✅ 检查图是否可构建
                try:
                    robust_convert_gate_list_to_graph(rule["lhs"])
                    robust_convert_gate_list_to_graph(rule["rhs"])
                except Exception as e:
                    invalid_graph += 1

            except Exception as e:
                invalid_label += 1

    print(f"\n✅ 总样本: {total}")
    print(f"✅ Label 为 1.0 的样本: {label_counts[1.0]}")
    print(f"✅ Label 为 0.0 的样本: {label_counts[0.0]}")
    if label_counts["other"] > 0:
        print(f"❌ 非法 Label 样本: {label_counts['other']}")

    if invalid_graph > 0:
        print(f"❌ 图构建失败样本数: {invalid_graph}")
    else:
        print(f"✅ 所有图结构合法 ✅")

if __name__ == "__main__":
    check_dataset(DATASET_PATH, "训练数据（含正负样本）")
