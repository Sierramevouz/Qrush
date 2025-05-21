import json

# 正例文件（原始 ECC 等价规则）
with open("../converted_ecc_rules.jsonl") as f_pos:
    positives = [json.loads(line) | {"label": 1.0} for line in f_pos]

# 负例文件（由脚本生成的不等价规则）
with open("converted_ecc_rules_with_negatives.jsonl") as f_neg:
    negatives = []
    for line in f_neg:
        try:
            item = json.loads(line)
            if item.get("label") == 0:
                negatives.append(item)
        except:
            continue

print(f"📊 正例数量: {len(positives)}")
print(f"📊 负例数量: {len(negatives)}")

# 合并并保存为新文件
output_path = "converted_ecc_rules_with_labels.jsonl"
with open(output_path, "w") as f:
    for item in positives + negatives:
        f.write(json.dumps(item) + "\n")

print(f"✅ 合并完成，写入 {output_path}")
