import os
import json

# 路径配置
input_dir = "./reswite_rule_set"  # 替换为你的实际路径
output_path = "./converted_ecc_rules.jsonl"

converted_rules = []

for fname in os.listdir(input_dir):
    if not fname.endswith(".json"):
        continue

    file_path = os.path.join(input_dir, fname)
    try:
        with open(file_path, "r") as f:
            raw_data = json.load(f)

        # ECC 结构是一个 list，其中第2项为 dict（规则集合）
        if isinstance(raw_data, list) and len(raw_data) == 2 and isinstance(raw_data[1], dict):
            rule_dict = raw_data[1]
            for rule_group in rule_dict.values():
                if len(rule_group) < 2:
                    continue  # 至少需要一对 lhs 和 rhs
                try:
                    lhs = rule_group[0][1]
                    rhs = rule_group[1][1]
                    converted_rules.append({
                        "lhs": lhs,
                        "rhs": rhs,
                        "depth_reduction": 0  # 可后续改成估算值
                    })
                except Exception as e:
                    print(f"❌ Error parsing rule in {fname}: {e}")
    except Exception as e:
        print(f"❌ Failed to load {fname}: {e}")

# 写入 .jsonl 文件
with open(output_path, "w") as out:
    for rule in converted_rules:
        out.write(json.dumps(rule) + "\n")

print(f"✅ Converted {len(converted_rules)} rules to: {output_path}")
