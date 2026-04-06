#!/bin/bash
# 审核智能体触发脚本
# 用法: ./audit-agent.sh --phase=final --input=output/{项目名}/ --output=review/{项目名}-audit-{日期}.md

set -e

# 解析参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --phase=*)
      PHASE="${1#*=}"
      shift
      ;;
    --input=*)
      INPUT="${1#*=}"
      shift
      ;;
    --output=*)
      OUTPUT="${1#*=}"
      shift
      ;;
    *)
      echo "未知参数: $1"
      exit 1
      ;;
  esac
done

# 验证输入目录
if [ ! -d "$INPUT" ]; then
  echo "错误: 输入目录不存在: $INPUT"
  exit 1
fi

# 创建输出目录
mkdir -p "$(dirname "$OUTPUT")"

# 执行审核
echo "开始审核..."
echo "输入: $INPUT"
echo "输出: $OUTPUT"

# TODO: 调用审核智能体
# 实际执行时调用 Claude Code 并传入 audit-agent.md

echo "审核完成"