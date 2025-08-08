import sys
import os
import traceback

# --- 1. 设置正确的 Python 搜索路径 ---
# 我们需要两个路径：
# a) Quartz 包本身的路径
# b) 你的项目代码的根路径 (为了能找到 'core' 模块)
QUARTZ_PYTHON_PATH = '/workspace/quartz/python'
PROJECT_ROOT_PATH = '/workspace'

# 将它们添加到 sys.path 的最前面，确保最高优先级
sys.path.insert(0, QUARTZ_PYTHON_PATH)
sys.path.insert(0, PROJECT_ROOT_PATH)

print("--- Python Path Configured ---")
print(sys.path)
print("----------------------------")

# --- 2. 尝试导入并运行你的主程序 ---
print("Attempting to import and run test_rl_quartz.py...")
try:
    # 导入你的主脚本。如果你的脚本是直接执行代码的，
    # 那么导入它就会运行它。
    # 如果你的代码在 if __name__ == "__main__": 块中，
    # 我们需要找到并调用它的主函数。
    from core import test_rl_quartz

    # 假设你的 test_rl_quartz.py 有一个 main() 函数
    if hasattr(test_rl_quartz, 'main'):
        print("Found main() function, executing...")
        test_rl_quartz.main()
    else:
        print("No main() function found in test_rl_quartz.py. Script logic should run on import.")

except Exception as e:
    print("\n!!! An error occurred while running the script: !!!")
    traceback.print_exc()

print("\n--- Launcher script finished. ---")
