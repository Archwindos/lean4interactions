#!/usr/bin/env bash
# Open the checked-in reader snapshot; no build or installation is needed.
set -u
PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1

for candidate in "$PROJECT_DIR/.conda-env/bin/python" "$PROJECT_DIR/.venv/bin/python" python3 python; do
  if "$candidate" -I -B -c 'import sys; sys.exit(sys.version_info < (3, 8))' >/dev/null 2>&1; then
    exec "$candidate" -I -B "$PROJECT_DIR/scripts/start-reader.py" "$@"
  fi
done

printf '%s\n' '未找到可用的 Python 3.8+。请安装 Python 3，或使用项目内的 Python 环境。' >&2
exit 1
