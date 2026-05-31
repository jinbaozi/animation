#!/bin/bash
# 编排师触发脚本
# 用法:
#   ./orchestrate.sh --project=项目名 --novel=小说.txt
#   ./orchestrate.sh --project=项目名 --watch  # 目录监测模式

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认值
PROJECT=""
NOVEL=""
WATCH_MODE=false
PHASE=""
RETRY_COUNT=3
RETRY_DELAY=5

# 解析参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --project=*)
      PROJECT="${1#*=}"
      shift
      ;;
    --novel=*)
      NOVEL="${1#*=}"
      shift
      ;;
    --watch)
      WATCH_MODE=true
      shift
      ;;
    --phase=*)
      PHASE="${1#*=}"
      shift
      ;;
    --help)
      echo "编排师自动化脚本"
      echo ""
      echo "用法:"
      echo "  ./orchestrate.sh --project=项目名 --novel=小说.txt"
      echo "  ./orchestrate.sh --project=项目名 --watch"
      echo "  ./orchestrate.sh --project=项目名 --phase=0"
      echo ""
      echo "参数:"
      echo "  --project=NAME    项目名称（必需）"
      echo "  --novel=PATH      小说文件路径"
      echo "  --watch          启用目录监测模式"
      echo "  --phase=PHASE    指定从哪个Phase开始"
      exit 0
      ;;
    *)
      echo "未知参数: $1"
      exit 1
      ;;
  esac
done

# 验证必需参数
if [ -z "$PROJECT" ]; then
  echo -e "${RED}错误: 缺少 --project 参数${NC}"
  echo "用法: ./orchestrate.sh --project=项目名 --novel=小说.txt"
  exit 1
fi

# 项目目录
PROJECT_DIR="output/$PROJECT"
INPUT_DIR="input/$PROJECT"

# 检查Claude Code是否可用
check_claude() {
  if ! command -v claude &> /dev/null; then
    echo -e "${RED}错误: Claude Code CLI 未安装或不在PATH中${NC}"
    echo "请安装Claude Code: https://claude.ai/code"
    exit 1
  fi
}

# 打印横幅
print_banner() {
  echo -e "${BLUE}============================================${NC}"
  echo -e "${BLUE}     AI 编排师 - 自动化工作流${NC}"
  echo -e "${BLUE}============================================${NC}"
  echo ""
}

# 打印状态
print_status() {
  echo -e "${GREEN}[$1]${NC} $2"
}

print_info() {
  echo -e "${YELLOW}[INFO]${NC} $1"
}

print_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# 执行Claude Code命令（带重试）
run_claude() {
  local TASK="$1"
  local PHASE_NAME="$2"
  local ATTEMPT=1

  while [ $ATTEMPT -le $RETRY_COUNT ]; do
    echo -e "${YELLOW}[RETRY $ATTEMPT/$RETRY_COUNT]${NC} 执行 $PHASE_NAME..."

    if claude -p "$TASK" 2>&1; then
      echo -e "${GREEN}[SUCCESS]${NC} $PHASE_NAME 执行成功"
      return 0
    else
      if [ $ATTEMPT -lt $RETRY_COUNT ]; then
        local DELAY=$((RETRY_DELAY * 2 ** (ATTEMPT - 1)))
        echo -e "${YELLOW}[RETRY]${NC} $PHASE_NAME 失败，${DELAY}秒后重试..."
        sleep $DELAY
      fi
      ATTEMPT=$((ATTEMPT + 1))
    fi
  done

  echo -e "${RED}[FAILED]${NC} $PHASE_NAME 执行失败（已重试 $RETRY_COUNT 次）"
  return 1
}

# Phase 0: 品控合规官
run_phase0() {
  print_status "Phase 0" "品控合规官 - 合规预审"

  # 检查输入
  if [ ! -d "$INPUT_DIR" ]; then
    mkdir -p "$INPUT_DIR"
    print_error "请将小说文件放入: $INPUT_DIR/"
    print_info "等待小说文件..."
    return 1
  fi

  local NOVEL_FILE=$(find "$INPUT_DIR" -maxdepth 1 -name "*.txt" -o -name "*.md" | head -1)
  if [ -z "$NOVEL_FILE" ]; then
    print_error "在 $INPUT_DIR/ 中未找到小说文件"
    return 1
  fi

  print_info "找到小说: $NOVEL_FILE"

  # 创建G0/Phase 0输出目录
  mkdir -p "$PROJECT_DIR/00-项目配置"
  mkdir -p "$PROJECT_DIR/01-Phase0-合规预审"

  # 获取小说文件内容（用于Claude Code任务）
  local NOVEL_CONTENT=$(cat "$NOVEL_FILE")

  # 构建Claude Code任务
  local CLAUDE_TASK="## Phase 0 任务：品控合规官

执行品控合规官任务：

**项目名**: $PROJECT
**小说文件**: $NOVEL_FILE
**项目配置输出**: $PROJECT_DIR/00-项目配置/project-manifest.md
**输出目录**: $PROJECT_DIR/01-Phase0-合规预审

### 任务要求

1. 加载中间表示规范: rules/中间表示规范.md
2. 先生成或更新 project manifest: templates/output/project-manifest模板.md
3. 加载品控合规官角色定义: agents/orchestrator/phases/Phase0/Phase0-主索引.md
4. **【强制】先执行 Step0-图谱查询.md**：通过 mcp_config.json 连接 graphify MCP server，查询合规规则（禁用词正则、禁止行为清单、生成前8项自检、平台合规规则），记录 source_location 溯源
5. 加载执行步骤:
   - Step1-接收解析.md
   - Step2-合规审核.md
   - Step3-评分标准.md
   - Step4-问题分类.md
   - Step5-生成报告.md
6. 加载质量标准: Phase0-质量标准.md
7. 读取小说文件内容
8. 执行合规预审
9. 生成合规预审报告到: $PROJECT_DIR/01-Phase0-合规预审/合规预审报告.md

### 小说内容

$NOVEL_CONTENT

### 输出要求

报告必须包含:
1. 合规通过/驳回判定
2. 问题清单（如有）
3. 修改建议（如有）
4. 评分（0-10）
5. 交付范围：VideoPrompt包 + 人物资产卡 + 场景资产卡

请开始执行。"

  run_claude "$CLAUDE_TASK" "Phase 0"
  return $?
}

# Phase 1: 内容总导演
run_phase1() {
  print_status "Phase 1" "内容总导演 - 剧本改编与分镜"

  mkdir -p "$PROJECT_DIR/02-Phase1-剧本分镜"

  # 检查Phase 0报告是否存在
  if [ ! -f "$PROJECT_DIR/01-Phase0-合规预审/合规预审报告.md" ]; then
    print_error "Phase 0 报告不存在，请先执行 Phase 0"
    return 1
  fi

  # 获取Phase 0报告内容
  local PHASE0_REPORT=$(cat "$PROJECT_DIR/01-Phase0-合规预审/合规预审报告.md")

  # 获取原始小说内容
  local NOVEL_FILE=$(find "$INPUT_DIR" -maxdepth 1 -name "*.txt" -o -name "*.md" | head -1)
  local NOVEL_CONTENT=$(cat "$NOVEL_FILE")

  local CLAUDE_TASK="## Phase 1 任务：内容总导演

执行内容总导演任务：

**项目名**: $PROJECT
**Phase 0 报告**: $PROJECT_DIR/01-Phase0-合规预审/合规预审报告.md
**输出目录**: $PROJECT_DIR/02-Phase1-剧本分镜

### 任务要求

1. 加载内容总导演角色定义: agents/orchestrator/phases/Phase1/Phase1-主索引.md
2. **【强制】先执行 Step0-图谱查询.md**：通过 mcp_config.json 连接 graphify MCP server，查询八场景类型、场景模板索引、审美偏好规则、风格一致性规则，记录 source_location 溯源
3. 加载执行步骤:
   - Step1-接收准备.md
   - Step2-剧本改编.md
   - Step3-分镜设计.md
4. 加载质量标准: Phase1-质量标准.md
5. 读取合规预审报告确认通过
6. 读取原始小说
7. 执行剧本改编和分镜设计
8. 生成产出物到 $PROJECT_DIR/02-Phase1-剧本分镜/:
   - StoryIR.md
   - 剧本.md
   - 基础分镜执行表.md
   - 人物清单.md
   - 场景清单.md

### Phase 0 合规预审报告

$PHASE0_REPORT

### 原始小说内容

$NOVEL_CONTENT

### 输出要求

产出物必须:
1. 符合所选风格规范
2. 包含完整的角色和场景清单
3. 分镜数量符合公式: target_shots ≈ ceil(total_word_count / 80)

请开始执行。"

  run_claude "$CLAUDE_TASK" "Phase 1"
  return $?
}

# Phase 1.5: 镜头序列设计师
run_phase1_5() {
  print_status "Phase 1.5" "镜头序列设计师 - 镜头序列设计"

  mkdir -p "$PROJECT_DIR/03-Phase1.5-镜头序列"

  # 检查Phase 1产出是否存在
  if [ ! -f "$PROJECT_DIR/02-Phase1-剧本分镜/基础分镜执行表.md" ]; then
    print_error "Phase 1 产出不存在，请先执行 Phase 1"
    return 1
  fi

  # 获取Phase 1产出内容
  local STORYBOARD=$(cat "$PROJECT_DIR/02-Phase1-剧本分镜/基础分镜执行表.md")
  local SCRIPT=$(cat "$PROJECT_DIR/02-Phase1-剧本分镜/剧本.md")
  local CHARACTERS=$(cat "$PROJECT_DIR/02-Phase1-剧本分镜/人物清单.md")
  local SCENES=$(cat "$PROJECT_DIR/02-Phase1-剧本分镜/场景清单.md")

  local CLAUDE_TASK="## Phase 1.5 任务：镜头序列设计师

执行镜头序列设计师任务：

**项目名**: $PROJECT
**Phase 1 产出**: $PROJECT_DIR/02-Phase1-剧本分镜/
**输出目录**: $PROJECT_DIR/03-Phase1.5-镜头序列

### 任务要求

1. 加载镜头序列设计师角色定义: agents/orchestrator/phases/Phase1.5/Phase1.5-主索引.md
2. **【强制】先执行 Step0-图谱查询.md**：通过 mcp_config.json 连接 graphify MCP server，查询镜头运动规则、场景切换规则、序列衔接规则，记录 source_location 溯源
3. 加载执行步骤:
   - Step1-镜头序列设计.md
   - Step2-序列衔接表.md
4. 加载质量标准: Phase1.5-质量标准.md
5. 读取 Phase 1 产出
6. 设计增强分镜序列
7. 生成产出物到 $PROJECT_DIR/03-Phase1.5-镜头序列/:
   - ShotIR.md
   - 增强分镜执行表.md
   - 序列衔接与继承表.md

### Phase 1 产出

**基础分镜执行表.md**:
$STORYBOARD

**剧本.md**:
$SCRIPT

**人物清单.md**:
$CHARACTERS

**场景清单.md**:
$SCENES

请开始执行。"

  run_claude "$CLAUDE_TASK" "Phase 1.5"
  return $?
}

# Phase 2a: 美术技术总监 - 人物四视图
run_phase2a() {
  print_status "Phase 2a" "美术技术总监 - 人物四视图与场景资产"

  mkdir -p "$PROJECT_DIR/04-Phase2a-四视图"

  # 检查Phase 1.5产出是否存在
  if [ ! -f "$PROJECT_DIR/03-Phase1.5-镜头序列/增强分镜执行表.md" ]; then
    print_error "Phase 1.5 产出不存在，请先执行 Phase 1.5"
    return 1
  fi

  # 获取所有必要内容
  local CHARACTER_LIST=$(cat "$PROJECT_DIR/02-Phase1-剧本分镜/人物清单.md")
  local SCENE_LIST=$(cat "$PROJECT_DIR/02-Phase1-剧本分镜/场景清单.md")
  local STORYBOARD=$(cat "$PROJECT_DIR/03-Phase1.5-镜头序列/增强分镜执行表.md")

  local CLAUDE_TASK="## Phase 2a 任务：美术技术总监（人物四视图）

执行美术技术总监 Phase 2a 任务：

**项目名**: $PROJECT
**Phase 1.5 产出**: $PROJECT_DIR/03-Phase1.5-镜头序列/
**Phase 1 产出**: $PROJECT_DIR/02-Phase1-剧本分镜/
**输出目录**: $PROJECT_DIR/04-Phase2a-四视图

### 任务要求

1. 加载美术技术总监角色定义: agents/orchestrator/phases/Phase2a/Phase2a-主索引.md
2. **【强制】先执行 Step0-图谱查询.md**：通过 mcp_config.json 连接 graphify MCP server，查询人物四视图格式、风格一致性规则、人物一致性控制、禁止词正则，记录 source_location 溯源
3. 加载执行步骤:
   - Step1-人物分析.md
   - Step2-四视图生成.md
   - Step3-场景资产卡.md
4. 加载质量标准: Phase2a/Phase2a-质量标准.md
5. 读取人物清单.md 和场景清单.md
6. 读取增强分镜执行表.md
7. 生成 VisualAnchorIR、人物资产卡、人物四视图Prompt包和场景资产卡
8. 生成产出物到 $PROJECT_DIR/04-Phase2a-四视图/:
   - VisualAnchorIR.md
   - 人物资产卡.md
   - 人物四视图Prompt包.md
   - 场景资产卡.md

### 风格规范

必须遵循 rules/风格一致性.md 中的风格规则。
禁止词正则: (?i)(影视|电影|摄像|胶片|摄影|古风写实|写实CG|游戏CG|影视质感|影视级|电影级)

### 输入内容

**人物清单.md**:
$CHARACTER_LIST

**场景清单.md**:
$SCENE_LIST

**增强分镜执行表.md**:
$STORYBOARD

请开始执行。"

  run_claude "$CLAUDE_TASK" "Phase 2a"
  return $?
}

# Phase 2b: 美术技术总监 - VideoPrompt
run_phase2b() {
  print_status "Phase 2b" "美术技术总监 - VideoPrompt生成"

  mkdir -p "$PROJECT_DIR/05-Phase2b-Prompt"

  # 检查Phase 2a产出是否存在
  if [ ! -f "$PROJECT_DIR/04-Phase2a-四视图/人物资产卡.md" ]; then
    print_error "Phase 2a 产出不存在，请先执行 Phase 2a"
    return 1
  fi

  # 获取所有必要内容
  local VISUAL_IR=$(cat "$PROJECT_DIR/04-Phase2a-四视图/VisualAnchorIR.md")
  local CHARACTER_ASSETS=$(cat "$PROJECT_DIR/04-Phase2a-四视图/人物资产卡.md")
  local CHAR_PROMPTS=$(cat "$PROJECT_DIR/04-Phase2a-四视图/人物四视图Prompt包.md")
  local SCENE_ASSETS=$(cat "$PROJECT_DIR/04-Phase2a-四视图/场景资产卡.md")
  local SHOT_IR=$(cat "$PROJECT_DIR/03-Phase1.5-镜头序列/ShotIR.md")
  local STORYBOARD=$(cat "$PROJECT_DIR/03-Phase1.5-镜头序列/增强分镜执行表.md")

  local CLAUDE_TASK="## Phase 2b 任务：美术技术总监（VideoPrompt）

执行美术技术总监 Phase 2b 任务：

**项目名**: $PROJECT
**Phase 2a 产出**: $PROJECT_DIR/04-Phase2a-四视图/
**输出目录**: $PROJECT_DIR/05-Phase2b-Prompt

### 任务要求

1. 加载美术技术总监角色定义: agents/orchestrator/phases/Phase2b/Phase2b-主索引.md
2. **【强制】先执行 Step0-图谱查询.md**：通过 mcp_config.json 连接 graphify MCP server，查询VideoPrompt格式、双轨生成规则、禁止行为清单、Negative Prompt写法，记录 source_location 溯源
3. 加载执行步骤:
   - Step1-接收准备.md
   - Step2-时间分段.md
   - Step3-VideoPrompt生成.md
4. 加载双轨生成规则: Phase2b/双轨生成规则.md
5. 加载质量标准: Phase2b/Phase2b-质量标准.md
6. 读取 VisualAnchorIR.md、人物资产卡.md、人物四视图Prompt包.md 和 场景资产卡.md
7. 读取 ShotIR.md 和增强分镜执行表.md
8. 先生成 PromptExportIR.md，再从 PromptExportIR 导出 VideoPrompt包
9. 生成产出物到 $PROJECT_DIR/05-Phase2b-Prompt/:
   - PromptExportIR.md
   - VideoPrompt包-中文版.md
   - VideoPrompt包-英文版.md

### 关键格式要求

每个时间戳段必须包含:
- [0:00-0:03] 格式（冒号+4位数字，Seedance 2.0要求）
- 镜头：[景别]+[运镜方式]+[运动速度]
- 动作：[具体物理动作描述，使用现在时态]

具体时间戳格式以 project-manifest.md 中的 tool profile 为准，不得让工具格式覆盖 PromptExportIR 字段契约。

### 输入内容

**VisualAnchorIR.md**:
$VISUAL_IR

**人物资产卡.md**:
$CHARACTER_ASSETS

**人物四视图Prompt包.md**:
$CHAR_PROMPTS

**场景资产卡.md**:
$SCENE_ASSETS

**增强分镜执行表.md**:
$STORYBOARD

**ShotIR.md**:
$SHOT_IR

请开始执行。"

  run_claude "$CLAUDE_TASK" "Phase 2b"
  return $?
}

# 执行完整流程
run_full_pipeline() {
  print_banner

  echo -e "${YELLOW}项目:${NC} $PROJECT"
  echo -e "${YELLOW}模式:${NC} 完整流程"
  echo ""

  check_claude

  # Phase 0
  if ! run_phase0; then
    print_error "Phase 0 执行失败"
    exit 1
  fi

  # Phase 1
  if ! run_phase1; then
    print_error "Phase 1 执行失败"
    exit 1
  fi

  # Phase 1.5
  if ! run_phase1_5; then
    print_error "Phase 1.5 执行失败"
    exit 1
  fi

  # Phase 2a
  if ! run_phase2a; then
    print_error "Phase 2a 执行失败"
    exit 1
  fi

  # Phase 2b
  if ! run_phase2b; then
    print_error "Phase 2b 执行失败"
    exit 1
  fi

  echo ""
  echo -e "${GREEN}============================================${NC}"
  echo -e "${GREEN}     完整流程执行完成！${NC}"
  echo -e "${GREEN}============================================${NC}"
  echo ""
  echo "输出目录: $PROJECT_DIR/"
  echo ""
}

# 目录监测模式
run_watch_mode() {
  print_banner

  echo -e "${YELLOW}项目:${NC} $PROJECT"
  echo -e "${YELLOW}模式:${NC} 目录监测"
  echo ""
  echo -e "${YELLOW}监控目录:${NC} $INPUT_DIR/"
  echo ""
  echo "等待小说文件..."
  echo "按 Ctrl+C 退出"
  echo ""

  # 检查目录是否存在
  if [ ! -d "$INPUT_DIR" ]; then
    mkdir -p "$INPUT_DIR"
    print_info "已创建监控目录: $INPUT_DIR/"
  fi

  # 使用inotifywait (Linux) 或 fswatch (macOS)
  if command -v inotifywait &> /dev/null; then
    # Linux
    inotifywait -m -e create "$INPUT_DIR" 2>/dev/null | while read path action file; do
      if [[ "$file" == *.txt ]] || [[ "$file" == *.md ]]; then
        print_info "检测到新文件: $file"
        print_info "触发完整流程..."
        run_full_pipeline
      fi
    done
  elif command -v fswatch &> /dev/null; then
    # macOS
    fswatch -0 "$INPUT_DIR" | while read -d '' file; do
      if [[ "$file" == *.txt ]] || [[ "$file" == *.md ]]; then
        print_info "检测到新文件: $file"
        print_info "触发完整流程..."
        run_full_pipeline
      fi
    done
  else
    print_error "未找到 inotifywait (Linux) 或 fswatch (macOS)"
    print_info "安装方法:"
    echo "  Linux: sudo apt install inotify-tools"
    echo "  macOS: brew install fswatch"
    exit 1
  fi
}

# 主入口
main() {
  if [ "$WATCH_MODE" = true ]; then
    run_watch_mode
  else
    run_full_pipeline
  fi
}

main
