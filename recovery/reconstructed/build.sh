#!/bin/bash
# Build the behavior-equivalent reconstruction (JDK 8 bytecode).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-$ROOT/build/classes}"
mkdir -p "$OUT"
mapfile -t sources < <(find "$ROOT/src/main/java" -name '*.java' | sort)
javac -source 1.8 -target 1.8 -encoding UTF-8 -cp "$ROOT/lib-mysql-connector.jar" -d "$OUT" "${sources[@]}"
echo "classes: $OUT"
