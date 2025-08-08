import sys
import os
import traceback

print("--- Quartz API Diagnostics and Launcher ---")

# --- 1. 设置正确的 Python 搜索路径 ---
# a) Quartz 包本身的路径
quartz_python_dir = '/workspace/quartz/python'
sys.path.insert(0, quartz_python_dir)

# b) 你的项目代码所在的根目录 (包含 'core' 目录)
# 【关键修正】: 将路径指向 core 目录的新位置
project_root_path = '/workspace/quartz/experiment/ppo-new'
sys.path.insert(0, project_root_path)

print("--- Python Path Configured ---")
print(sys.path)
print("----------------------------")

# --- 2. 尝试导入并运行你的主程序 ---
print("Attempting to import and run test_rl_quartz.py...")
try:
    # 现在 Python 应该能在 project_root_path 中找到 'core' 包
    from core import test_rl_quartz

    print("Import successful! Running script logic...")

    # 假设你的 test_rl_quartz.py 的主要逻辑是直接执行的，
    # 或者在一个 main() 函数中。
    # 如果有 main() 函数，最好在这里调用它。
    if hasattr(test_rl_quartz, 'main') and callable(test_rl_quartz.main):
        test_rl_quartz.main()
    else:
        # 如果没有 main()，导入模块本身就会执行其顶级代码
        pass

except Exception as e:
    print("\n!!! An error occurred while running the script: !!!")
    traceback.print_exc()

print("\n--- Launcher script finished. ---")