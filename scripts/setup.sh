#!/bin/bash
set -euo pipefail

VENV_DIR="${1:-.venv}"

# 1) Pick a Python 3 interpreter (prefer 'python3', then 'python' if it's 3.x)
PYTHON_BIN=""
for cmd in python3 python; do
  if command -v "$cmd" >/dev/null 2>&1; then
    if "$cmd" -c 'import sys; raise SystemExit(0 if sys.version_info.major==3 else 1)'; then
      PYTHON_BIN="$cmd"
      break
    fi
  fi
done

if [[ -z "${PYTHON_BIN}" ]]; then
  echo "Error: Python 3 not found. Please install Python 3.10+." >&2
  exit 1
fi

FOUND_VER="$("$PYTHON_BIN" -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')"

if ! "$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)'; then
  echo "Error: Need Python >= 3.10; found $FOUND_VER." >&2
  echo "If you have multiple Python versions installed, point PYTHON_BIN in this script to the right one." >&2
  exit 1
fi

FOUND_VER="$("$PYTHON_BIN" -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')"

if "$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info[1] < 11 else 1)'; then
  echo "Warning: Python $FOUND_VER < 3.11 detected. Some typing features might not work and may need to be removed to run the stencil. " >&2
fi

if ! "$PYTHON_BIN" -c 'import importlib.util,sys; raise SystemExit(0 if importlib.util.find_spec("venv") else 1)'; then
  echo "Error: The 'venv' module is missing. Install it before running this script" >&2
  exit 1
fi

if [[ -d "$VENV_DIR" ]]; then
  echo "Note: $VENV_DIR already exists; leaving it untouched."
else
  "$PYTHON_BIN" -m venv "$VENV_DIR"
  echo "Created virtual environment at: $VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip >/dev/null

"$VENV_DIR/bin/python" -m pip install -e . >/dev/null
echo "Installed dependencies from pyproject.toml"

echo "Using interpreter: $("$PYTHON_BIN" --version)"
echo "To activate: source \"$VENV_DIR/bin/activate\""
echo "To deactivate: deactivate\""