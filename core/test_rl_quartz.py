from reward_positive_ecc_loader import load_positive_ecc_rules
from rl_env import RewriteEnv

# ✅ 使用真正含有优化规则的 ECC 文件
rules = load_positive_ecc_rules("../quartz/experiment/ecc_set/nam_ecc.json")


# ✅ 使用其中一条规则的 LHS 构造初始电路（更容易 rewrited）
init_gate_list = rules[0].lhs_gates
env = RewriteEnv(initial_gate_list=init_gate_list, ecc_rules=rules)

# ✅ 运行多个 episode，观察 reward 是否大于 0
for episode in range(10):
    obs = env.reset()
    actions = env.get_applicable_actions()
    print(f"[Episode {episode}] 可用动作数: {len(actions)}")

    if not actions:
        print("❌ 无 rewrited 动作，跳过")
        continue

    # 选择第一个 rewrited 动作执行
    gate_id, rule_id, match = actions[0]
    print(f"[Episode {episode}] 执行 rule {rule_id} at gate {gate_id}")
    obs, reward, done, _ = env.step((gate_id, rule_id, match))

    print(f"[Episode {episode}] 🎯 reward: {reward}\n")
