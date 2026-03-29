# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

This repository contains two distinct parts:

1. **Markdown documentation** (directories `01-输入处理/` through `10-MPV测试/`): A Chinese-language knowledge base for "长文小说转AI漫剧 Prompt生成系统". Pure documentation, no executable code.

2. **autoresearch** (from [karpathy/autoresearch](https://github.com/karpathy/autoresearch)): An autonomous LLM pretraining research system. Uses Python + PyTorch on a single NVIDIA GPU. The AI agent modifies `train.py` and runs 5-minute training experiments in a loop.

### autoresearch setup

- **Package manager**: [uv](https://docs.astral.sh/uv/) — install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Python**: 3.10+ (`.python-version` pinned to 3.10, `uv` manages this automatically)
- **Dependencies**: `uv sync` installs everything (PyTorch with CUDA 12.8, kernels, tiktoken, etc.)
- **Data prep**: `uv run prepare.py` downloads training data shards and trains a BPE tokenizer (one-time, ~2 min). Data cached in `~/.cache/autoresearch/`.
- **Training**: `uv run train.py` — requires an NVIDIA GPU (H100 recommended). Runs for a fixed 5-minute time budget.

### Key files

| File | Purpose | Editable? |
|------|---------|-----------|
| `prepare.py` | Data download, tokenizer training, evaluation harness | **No** (read-only) |
| `train.py` | GPT model, optimizer, training loop | **Yes** (agent modifies this) |
| `program.md` | Agent instructions / "skill file" | **Yes** (human edits this) |
| `analysis.ipynb` | Notebook for analyzing `results.tsv` | Optional |

### Running experiments

See `program.md` for the full experiment loop protocol. Key points:
- The agent creates a branch `autoresearch/<tag>`, runs experiments, keeps improvements, discards failures
- Results are logged to `results.tsv` (tab-separated, NOT committed to git)
- Metric: `val_bpb` (validation bits per byte) — lower is better

### Important caveats

- **NVIDIA GPU required**: `train.py` fails immediately without a CUDA-capable GPU. The Cloud VM does not have a GPU — training can only run on GPU-equipped machines.
- **Do NOT modify `prepare.py`**: It contains fixed constants and the evaluation harness.
- All Markdown documentation uses Chinese (Simplified) file names — ensure UTF-8 handling.

### Markdown linting

Run `markdownlint-cli2 "**/*.md"` to lint Markdown files. Expect many pre-existing style warnings.
