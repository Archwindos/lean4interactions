#!/usr/bin/env bash
# Install the fixed Linux x86_64 toolchain/dependencies inside this project.
set -euo pipefail
lean_project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source "$lean_project_root/scripts/env.sh"
export MATHLIB_NO_CACHE_ON_UPDATE=1
mkdir -p "$lean_project_root/.tools" "$lean_project_root/.tmp"
cd "$lean_project_root"
if [[ ! -x .tools/lean-4.24.0-linux/bin/lean ]]; then
  curl -fL --retry 2 https://github.com/leanprover/lean4/releases/download/v4.24.0/lean-4.24.0-linux.tar.zst -o .tmp/lean-4.24.0-linux.tar.zst
  python - <<'PY'
import hashlib,json
from pathlib import Path
lock=json.loads(Path('locks/lean-dependencies.json').read_text())
expected=next(d['sha256'] for d in lock['downloads'] if d['filename']=='lean-4.24.0-linux.tar.zst')
actual=hashlib.sha256(Path('.tmp/lean-4.24.0-linux.tar.zst').read_bytes()).hexdigest()
if actual != expected:
    raise SystemExit('Lean binary archive checksum mismatch')
PY
  tar --zstd -xf .tmp/lean-4.24.0-linux.tar.zst -C .tools
fi
if [[ ! -e .tools/lean ]]; then ln -s lean-4.24.0-linux .tools/lean; fi
if [[ ! -d .tools/mathlib4-4.24.0/.git ]]; then
  git clone --depth 1 --branch v4.24.0 https://github.com/leanprover-community/mathlib4.git .tools/mathlib4-4.24.0
fi
lean_mathlib_rev="$(git -C .tools/mathlib4-4.24.0 rev-parse HEAD)"
[[ "$lean_mathlib_rev" == f897ebcf72cd16f89ab4577d0c826cd14afaafc7 ]] || { echo 'mathlib revision mismatch' >&2; exit 1; }
cd .tools/mathlib4-4.24.0
lake exe cache get Mathlib/Data/Real/Basic.lean Mathlib/Algebra/BigOperators/Group/Finset/Powerset.lean Mathlib/Tactic.lean
cd "$lean_project_root"
for lean_package in lean/HarsanyiLib lean/PaperProofs examples/library-consumer; do
  mkdir -p "$lean_package/.lake/packages"
  for lean_dep in "$lean_project_root"/.tools/mathlib4-4.24.0/.lake/packages/*; do
    lean_dest="$lean_package/.lake/packages/$(basename "$lean_dep")"
    if [[ ! -e "$lean_dest" ]]; then ln -s "$lean_dep" "$lean_dest"; fi
  done
  if [[ ! -e "$lean_package/.lake/packages/mathlib" ]]; then
    ln -s "$lean_project_root/.tools/mathlib4-4.24.0" "$lean_package/.lake/packages/mathlib"
  fi
done
lean --version
echo 'Installed. Run scripts/verify-lean.sh for builds and axiom audits.'
