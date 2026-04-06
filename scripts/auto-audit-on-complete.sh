#!/bin/bash
# 自动审核触发脚本
# 监控Phase 2b完成标志文件，自动触发审核

set -e

PROJECT_NAME="${1:-demo}"
OUTPUT_DIR="output/${PROJECT_NAME}"
REVIEW_DIR="review"

# 等待Phase 2b完成
echo "等待 Phase 2b 完成..."
while [ ! -f "${OUTPUT_DIR}/phase2b-complete.flag" ]; do
    sleep 5
done

echo "检测到 Phase 2b 完成，开始审核..."

# 创建审核报告目录
mkdir -p "${REVIEW_DIR}"

# 生成审核报告文件名
DATE=$(date +%Y-%m-%d)
REPORT_FILE="${REVIEW_DIR}/${PROJECT_NAME}-audit-${DATE}.md"

# 调用审核脚本
./scripts/audit-agent.sh \
    --phase=final \
    --input="${OUTPUT_DIR}/" \
    --output="${REPORT_FILE}"

echo "审核完成，报告：${REPORT_FILE}"
