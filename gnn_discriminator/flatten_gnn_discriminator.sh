#!/bin/bash

# 进入当前脚本所在目录
cd "$(dirname "$0")"

echo "📂 开始释放 data 文件夹下的所有内容..."

if [ -d "data" ]; then
  # 将 data/ 中所有文件移动到当前目录
  mv data/* .

  # 删除空的 data 文件夹
  rmdir data

  echo "✅ 已成功将 data/ 内容移至当前目录，并删除 data 文件夹。"
else
  echo "⚠️ 未找到 data 文件夹，无需操作。"
fi
