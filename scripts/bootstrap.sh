#!/usr/bin/env bash
set -euo pipefail
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/env.sh"
cd "$ARCHIVE_PROJECT_ROOT"
CONDA_BIN="${CONDA_EXE:-$(command -v conda || true)}"
if [[ -z "$CONDA_BIN" ]]; then
  echo 'Conda executable missing. Install Miniforge into .tools/miniforge, then set CONDA_EXE.' >&2
  exit 1
fi
CONDA_PYTHON_BIN="$(dirname -- "$CONDA_BIN")/python"
# Disable Conda's configuration search before importing the CLI: no home/system
# configuration is loaded. Environment options in env.sh still apply.
_isolated_conda() {
  "$CONDA_PYTHON_BIN" -I -B -c 'import conda.base.constants as c; c.SEARCH_PATH=(); from conda.cli.main import main; raise SystemExit(main())' "$@"
}
if [[ ! -x .conda-env/bin/python ]]; then
  if [[ -f locks/python-conda-linux-64.txt ]]; then
    _isolated_conda --no-plugins create --yes --no-default-packages --prefix "$ARCHIVE_PROJECT_ROOT/.conda-env" --file locks/python-conda-linux-64.txt
  else
    _isolated_conda --no-plugins create --yes --no-default-packages --override-channels -c conda-forge --prefix "$ARCHIVE_PROJECT_ROOT/.conda-env" python=3.12 pip
  fi
fi
if [[ ! -x .conda-env/bin/pdftoppm ]]; then
  # Formal source-page rendering belongs to this prefix, never a system install.
  _isolated_conda --no-plugins install --yes --freeze-installed --override-channels -c conda-forge --prefix "$ARCHIVE_PROJECT_ROOT/.conda-env" poppler
fi
if [[ -f locks/python-pip.txt ]]; then
  .conda-env/bin/python -m pip install -r locks/python-pip.txt
  .conda-env/bin/python -m pip install --no-deps --no-build-isolation -e .
else
  .conda-env/bin/python -m pip install -e '.[test]'
fi
_isolated_conda --no-plugins list --prefix "$ARCHIVE_PROJECT_ROOT/.conda-env" --explicit > locks/python-conda-linux-64.txt
.conda-env/bin/python scripts/check-python-locks.py --freeze-installed > locks/python-pip.txt
.conda-env/bin/python scripts/check-python-locks.py
.conda-env/bin/python -c 'import sys; print("Conda Python:", sys.executable)'
