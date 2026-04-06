#!/bin/bash
# 审核智能体触发脚本
# 用法: ./audit-agent.sh --phase=final --input=output/{项目名}/ --output=review/{项目名}-audit-{日期}.md

set -e

# 默认值
PHASE="final"
INPUT=""
OUTPUT=""

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

# 验证必需参数
if [ -z "$INPUT" ]; then
  echo "错误: 缺少 --input 参数"
  echo "用法: ./audit-agent.sh --phase=final --input=output/{项目名}/ --output=review/{项目名}-audit-{日期}.md"
  exit 1
fi

if [ -z "$OUTPUT" ]; then
  echo "错误: 缺少 --output 参数"
  echo "用法: ./audit-agent.sh --phase=final --input=output/{项目名}/ --output=review/{项目名}-audit-{日期}.md"
  exit 1
fi

# 验证输入目录
if [ ! -d "$INPUT" ]; then
  echo "错误: 输入目录不存在: $INPUT"
  exit 1
fi

# 创建输出目录
mkdir -p "$(dirname "$OUTPUT")"

# 从输入路径提取项目名
PROJECT_NAME=$(basename "$INPUT")
INPUT_DIR="$(cd "$(dirname "$INPUT")" && pwd)"
OUTPUT_DIR="$(cd "$(dirname "$OUTPUT")" && pwd)"
OUTPUT_FILE="$(basename "$OUTPUT")"

echo "============================================"
echo "AI审核智能体启动"
echo "============================================"
echo "项目名: $PROJECT_NAME"
echo "输入目录: $INPUT_DIR"
echo "输出文件: $OUTPUT_DIR/$OUTPUT_FILE"
echo "审核阶段: $PHASE"
echo "============================================"

# 构建审核任务提示词
AUDIT_TASK="## 审核任务

执行AI审核智能体任务：

**项目名**: $PROJECT_NAME
**输入目录**: $INPUT_DIR
**输出文件**: $OUTPUT_DIR/$OUTPUT_FILE
**审核阶段**: $PHASE

### 任务要求

1. 加载主编排器: agents/audit-agent.md
2. 按执行流程执行审核:
   - Phase 1: 产物收集（读取 $INPUT_DIR 下所有产物）
   - Phase 2: 规则引擎预检（8维度并行）
   - Phase 3: LLM细审
   - Phase 4: 报告汇总

3. 产物清单（按需加载）:
   - 剧本.md → agents/audit/dimensions/04-narrative-logic.md
   - 基础分镜执行表.md → agents/audit/dimensions/04-narrative-logic.md
   - 增强分镜执行表.md → agents/audit/dimensions/03-action-coherence.md, 05-expression-precision.md, 06-dialogue-interaction.md, 07-cinematography.md
   - 序列衔接与继承表.md → agents/audit/dimensions/03-action-coherence.md
   - 人物清单.md → agents/audit/dimensions/01-character-consistency.md
   - 人物四视图Prompt包.md → agents/audit/dimensions/01-character-consistency.md, 08-world-building.md
   - 场景清单.md → agents/audit/dimensions/02-scene-consistency.md
   - 场景资产卡.md → agents/audit/dimensions/02-scene-consistency.md
   - VideoPrompt包.md → agents/audit/dimensions/01-character-consistency.md, 02-scene-consistency.md, 03-action-coherence.md, 05-expression-precision.md, 06-dialogue-interaction.md, 07-cinematography.md, 08-world-building.md

4. 加载规则引擎: agents/audit/rules/audit-rules.md
5. 加载评分计算表: agents/audit/templates/score-sheet.md
6. 生成审核报告并保存到: $OUTPUT_DIR/$OUTPUT_FILE

### 输出要求

生成的报告必须包含:
1. 执行摘要
2. 评分汇总（8维度，每维度0-10分）
3. 问题清单（P0/P1/P2分级）
4. 维度详细分析
5. 修复优先级建议
6. 附录

请开始执行审核任务。"

# 检查Claude Code是否可用
if ! command -v claude &> /dev/null; then
  echo "错误: Claude Code CLI 未安装或不在PATH中"
  echo "请安装Claude Code: https://claude.ai/code"
  exit 1
fi

# 执行审核
echo "开始执行审核..."
echo ""

# 使用Claude Code执行审核任务
claude -p "$AUDIT_TASK" --output-format stream 2>&1

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo ""
  echo "============================================"
  echo "审核完成！"
  echo "报告已保存到: $OUTPUT_DIR/$OUTPUT_FILE"
  echo "============================================"
else
  echo ""
  echo "============================================"
  echo "审核执行失败，退出码: $EXIT_CODE"
  echo "============================================"
  exit $EXIT_CODE
fi
