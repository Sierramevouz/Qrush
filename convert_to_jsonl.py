import os
import json

# 设置 reswite_rule_set 文件夹路径（你可以根据实际情况修改）
rule_dir = "./reswite_rule_set"
output_path = "./converted_rules.jsonl"

count = 0
with open(output_path, "w") as outfile:
    for fname in os.listdir(rule_dir):
        if fname.endswith(".json"):
            full_path = os.path.join(rule_dir, fname)
            try:
                with open(full_path, "r") as f:
                    data = json.load(f)
                    if "lhs" in data and "rhs" in data:
                        json.dump(data, outfile)
                        outfile.write("\n")
                        count += 1
            except Exception as e:
                print(f"❌ Failed to parse {fname}: {e}")

print(f"✅ Done. Converted {count} valid rules into: {output_path}")
