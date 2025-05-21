import json
import random
import os
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

POSITIVE_FILE = "../converted_ecc_rules.jsonl"
OUTPUT_FILE = "converted_ecc_rules_with_negatives.jsonl"
NEGATIVE_SAMPLE_RATIO = 1.0  # 负例比例
NUM_WORKERS = 40             # ✅ 使用 CPU 的核数

def load_positive_rules(jsonl_path):
    rules = []
    with open(jsonl_path, 'r') as f:
        for line in f:
            obj = json.loads(line)
            if 'lhs' in obj and 'rhs' in obj:
                rules.append(obj)
    return rules

def generate_neg_batch(lhs_pool, rhs_pool, pos_set, num_samples, seed):
    random.seed(seed)
    local_neg = []
    for _ in range(num_samples):
        lhs = random.choice(lhs_pool)
        rhs = random.choice(rhs_pool)
        key = json.dumps({"lhs": lhs, "rhs": rhs})
        if key in pos_set:
            continue
        local_neg.append({
            "lhs": lhs,
            "rhs": rhs,
            "label": 0.0
        })
    return local_neg

def main():
    if not os.path.exists(POSITIVE_FILE):
        print(f"❌ File not found: {POSITIVE_FILE}")
        return

    print(f"📥 Loading positive rules from {POSITIVE_FILE} ...")
    positive_rules = load_positive_rules(POSITIVE_FILE)
    print(f"✅ Loaded {len(positive_rules)} positive rules")

    lhs_pool = [r['lhs'] for r in positive_rules]
    rhs_pool = [r['rhs'] for r in positive_rules]
    pos_set = set(json.dumps({"lhs": r["lhs"], "rhs": r["rhs"]}) for r in positive_rules)

    num_negatives = int(len(positive_rules) * NEGATIVE_SAMPLE_RATIO)
    batch_size = num_negatives // NUM_WORKERS

    print(f"⚙️  Generating {num_negatives} negatives using {NUM_WORKERS} workers...")

    negative_rules = []
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = []
        for i in range(NUM_WORKERS):
            futures.append(executor.submit(
                generate_neg_batch,
                lhs_pool, rhs_pool, pos_set, batch_size, seed=i
            ))

        for f in tqdm(as_completed(futures), total=len(futures)):
            negative_rules.extend(f.result())

    print(f"✅ Generated {len(negative_rules)} negative rules")

    all_rules = positive_rules + negative_rules
    random.shuffle(all_rules)

    with open(OUTPUT_FILE, 'w') as f:
        for rule in all_rules:
            json.dump(rule, f)
            f.write("\n")

    print(f"✅ Output saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
