#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$ROOT/.venv_demo"
PYFILES=("1. Physics Validation Tests.py" "3. Expected Numerical Results.py")

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
  "$VENV_DIR/bin/pip" install -r "$ROOT/requirements.txt"
fi

echo "Using python: $VENV_DIR/bin/python"
# run the quick mode of tests (must be supported by scripts)
"$VENV_DIR/bin/python" "${PYFILES[0]}" --quick --out-dir demo_output
"$VENV_DIR/bin/python" "${PYFILES[1]}" --quick --out-dir demo_output
echo "Demo complete. Output in demo_output/"
