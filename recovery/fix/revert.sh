#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/reconstructed"
patch -R -p1 < "$ROOT/fix/benchmark-single-instance.patch"
patch -R -p1 < "$ROOT/fix/wlm-perf-fix.patch"
echo "reverted to behavior-equivalent sources"
