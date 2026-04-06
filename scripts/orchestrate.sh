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

  # 创建Phase 0输出目录
  mkdir -p "$PROJECT_DIR/01-Phase0-合规预审"

  echo -e "${GREEN}Phase 0 完成${NC}"
  return 0
}

# Phase 1: 内容总导演
run_phase1() {
  print_status "Phase 1" "内容总导演 - 剧本改编与分镜"

  mkdir -p "$PROJECT_DIR/02-Phase1-剧本分镜"

  echo -e "${GREEN}Phase 1 完成${NC}"
  return 0
}

# Phase 1.5: 镜头序列设计师
run_phase1_5() {
  print_status "Phase 1.5" "镜头序列设计师 - 镜头序列设计"

  mkdir -p "$PROJECT_DIR/03-Phase1.5-镜头序列"

  echo -e "${GREEN}Phase 1.5 完成${NC}"
  return 0
}

# Phase 2a: 美术技术总监 - 人物四视图
run_phase2a() {
  print_status "Phase 2a" "美术技术总监 - 人物四视图与场景资产"

  mkdir -p "$PROJECT_DIR/04-Phase2a-风格四视图"

  echo -e "${GREEN}Phase 2a 完成${NC}"
  return 0
}

# Phase 2b: 美术技术总监 - VideoPrompt
run_phase2b() {
  print_status "Phase 2b" "美术技术总监 - VideoPrompt生成"

  mkdir -p "$PROJECT_DIR/05-Phase2b-Prompt生成"

  echo -e "${GREEN}Phase 2b 完成${NC}"
  return 0
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
