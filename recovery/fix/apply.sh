#!/bin/bash
# Apply the performance fix onto recovery/reconstructed. Revert with revert.sh.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/reconstructed"
patch -p1 < "$ROOT/fix/wlm-perf-fix.patch"
patch -p1 < "$ROOT/fix/benchmark-single-instance.patch"
echo "applied. rebuild with: $ROOT/reconstructed/build.sh"
