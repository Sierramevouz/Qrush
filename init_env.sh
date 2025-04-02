#!/bin/bash

echo "🚀 正在初始化 QRush 项目环境..."

# 设置 PYTHONPATH 指向项目根目录，确保 core 模块能被找到
export PYTHONPATH="/home/mayiming/qrane_project/quantum_rewriter_project:$PYTHONPATH"
echo "✅ PYTHONPATH 已设置为：$PYTHONPATH"

echo "✅ 初始化完成！你现在可以运行如下命令："
echo ""
echo "    PYTHONPATH=/home/mayiming/qrane_project/quantum_rewriter_project python test/test_env.py"
echo ""
echo "或者运行本脚本："
echo ""
echo "    source init_env.sh && python test/test_env.py"
